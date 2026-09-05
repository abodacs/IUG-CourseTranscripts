import json
import logging
import os
import sys
import time
import datetime
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from asgiref.sync import async_to_sync

try:
    from .transcript_integrity import atomic_json_write, assign_subtitles, content_hash
except ImportError:
    from transcript_integrity import atomic_json_write, assign_subtitles, content_hash


# Handle optional dependencies
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    print("Warning: google.generativeai not installed. Install with: pip install google-generativeai")
    GEMINI_AVAILABLE = False
    genai = None

# Handle imports for both direct execution and module import
try:
    from ..config import GEMINI_API_KEY
except ImportError:
    try:
        sys.path.append(str(Path(__file__).parent.parent))
        from config import GEMINI_API_KEY
    except ImportError:
        GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        if not GEMINI_API_KEY:
            print("Error: GEMINI_API_KEY not found. Please set it as an environment variable.")
            sys.exit(1)

# Configuration
class Config:
    """Enhanced configuration settings for resilient transcript processing."""
    
    # File processing
    MAX_TEXT_LENGTH = 30000  # Conservative limit for Gemini API
    CHUNK_OVERLAP = 200  # Overlap between chunks for context
    SUPPORTED_EXTENSIONS = ['.json', '.srt']
    OUTPUT_INDENT = 2
    CLEANING_VERSION = 'legacy-cleaning-integrity-1'  # Bump when prompt/model policy changes
    
    # API Rate Limits
    DAILY_CALL_LIMIT = 14400  # 14k calls per day
    CALLS_PER_MINUTE = 50     # 50 calls per minute
    TOKENS_PER_MINUTE = 15000 # 15k tokens per minute
    
    # Rate limiting windows
    MINUTE_WINDOW = 60        # 60 seconds
    TOKEN_ESTIMATION_RATIO = 4 # Rough tokens per character
    
    # Retry and backoff settings
    MIN_RETRY_DELAY = 60      # 1 minute minimum
    MAX_RETRY_DELAY = 86400   # 24 hours maximum
    BACKOFF_MULTIPLIER = 2    # Exponential backoff multiplier
    
    # State persistence
    STATE_FILE = '.transcript_processing_state.json'
    CHECKPOINT_FREQUENCY = 10  # Save state every N successful calls
    
    # Logging
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = 'transcript_processing_v2.log'
    
    @classmethod
    def setup_logging(cls):
        """Setup logging configuration."""
        logging.basicConfig(
            level=cls.LOG_LEVEL,
            format=cls.LOG_FORMAT,
            handlers=[
                logging.FileHandler(cls.LOG_FILE),
                logging.StreamHandler(sys.stdout)
            ]
        )

# Initialize configuration
logger = logging.getLogger(__name__)

class ProcessingState:
    """Manages persistent state for resilient processing."""
    
    def __init__(self, state_file: str = Config.STATE_FILE):
        self.state_file = Path(state_file)
        self.state = self._load_state()
        
    def _load_state(self) -> Dict[str, Any]:
        """Load processing state from disk."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                logger.info(f"Loaded processing state with {len(state.get('completed_items', []))} completed items")
                return state
            except (json.JSONDecodeError, IOError) as e:
                raise ValueError(f"Cannot read existing state; preserve it for recovery: {e}") from e
        
        return {
            'daily_call_count': 0,
            'last_reset_date': str(datetime.date.today()),
            'completed_items': [],
            'failed_items': [],
            'call_timestamps': [],
            'token_usage_timeline': [],
            'last_checkpoint': str(datetime.datetime.now())
        }
    
    def save_state(self):
        """Save current state to disk."""
        self.state['last_checkpoint'] = str(datetime.datetime.now())
        atomic_json_write(self.state_file, self.state)

    def completed_text(self, item_id, source_hash):
        record = self.state.get('completed_results', {}).get(item_id)
        if record is None:
            if self.is_completed(item_id):
                raise ValueError(f"Legacy completion lacks saved text; review required: {item_id}")
            return None
        if (record.get('source_hash') != source_hash
                or record.get('cleaning_version') != Config.CLEANING_VERSION):
            raise ValueError(f"Saved cleaning is stale; review required: {item_id}")
        text = record.get('text')
        if not isinstance(text, str) or not text.strip() or record.get('text_hash') != content_hash(text):
            raise ValueError(f"Saved cleaning is corrupt: {item_id}")
        return text

    def save_completed_text(self, item_id, source_hash, text):
        if not text.strip():
            raise ValueError("Cannot checkpoint empty cleaning")
        previous = json.loads(json.dumps(self.state))
        try:
            self.state.setdefault('completed_results', {})[item_id] = {
                'source_hash': source_hash,
                'cleaning_version': Config.CLEANING_VERSION,
                'text': text,
                'text_hash': content_hash(text),
            }
            self.mark_completed(item_id)
        except Exception:
            self.state = previous
            raise

    def reset_daily_quota_if_needed(self):
        """Reset daily call count if new day."""
        today = str(datetime.date.today())
        if self.state['last_reset_date'] != today:
            logger.info(f"New day detected, resetting daily quota. Previous count: {self.state['daily_call_count']}")
            self.state['daily_call_count'] = 0
            self.state['last_reset_date'] = today
            self.state['call_timestamps'] = []
            self.state['token_usage_timeline'] = []
            self.save_state()
    
    def can_make_call(self, estimated_tokens: int) -> Tuple[bool, str]:
        """Check if we can make an API call within all limits."""
        self.reset_daily_quota_if_needed()
        
        # Check daily limit
        if self.state['daily_call_count'] >= Config.DAILY_CALL_LIMIT:
            return False, f"Daily limit reached ({self.state['daily_call_count']}/{Config.DAILY_CALL_LIMIT})"
        
        now = time.time()
        minute_ago = now - Config.MINUTE_WINDOW
        # Clean old timestamps
        self.state['call_timestamps'] = [ts for ts in self.state['call_timestamps'] if ts > minute_ago]
        self.state['token_usage_timeline'] = [(ts, tokens) for ts, tokens in self.state['token_usage_timeline'] if ts > minute_ago]
        
        # Check calls per minute
        if len(self.state['call_timestamps']) >= Config.CALLS_PER_MINUTE:
            return False, f"Rate limit: {len(self.state['call_timestamps'])} calls in last minute"
        
        # Check tokens per minute
        tokens_in_last_minute = sum(tokens for _, tokens in self.state['token_usage_timeline'])

        if tokens_in_last_minute + estimated_tokens > Config.TOKENS_PER_MINUTE:
            return False, f"Token limit: {tokens_in_last_minute + estimated_tokens} tokens would exceed {Config.TOKENS_PER_MINUTE}/min"
        
        return True, "OK"
    
    def record_api_call(self, estimated_tokens: int):
        """Record a successful API call."""
        now = time.time()
        self.state['call_timestamps'].append(now)
        self.state['token_usage_timeline'].append((now, estimated_tokens))
        self.state['daily_call_count'] += 1
        
        if self.state['daily_call_count'] % Config.CHECKPOINT_FREQUENCY == 0:
            self.save_state()
    
    def mark_completed(self, item_id: str):
        """Mark an item as successfully completed."""
        if item_id not in self.state['completed_items']:
            self.state['completed_items'].append(item_id)
            
        # Remove from failed items if it was there
        self.state['failed_items'] = [item for item in self.state['failed_items'] if item['id'] != item_id]
        self.save_state()
    
    def mark_failed(self, item_id: str, error_msg: str, retry_after: Optional[float] = None):
        """Mark an item as failed with retry information."""
        # Remove existing entry for this item
        self.state['failed_items'] = [item for item in self.state['failed_items'] if item['id'] != item_id]
        
        # Add new failure record
        failure_record = {
            'id': item_id,
            'error': error_msg,
            'failed_at': str(datetime.datetime.now()),
            'retry_after': retry_after,
            'attempt_count': 1
        }
        
        # Increment attempt count if item was already failed
        for item in self.state['failed_items']:
            if item['id'] == item_id:
                failure_record['attempt_count'] = item.get('attempt_count', 1) + 1
                break
        
        self.state['failed_items'].append(failure_record)
        self.save_state()
    
    def is_completed(self, item_id: str) -> bool:
        """Check if item is already completed."""
        return item_id in self.state['completed_items']
    
    def get_failed_items_ready_for_retry(self) -> List[Dict[str, Any]]:
        """Get failed items that are ready for retry."""
        now = time.time()
        ready_items = []
        
        for item in self.state['failed_items']:
            if item.get('retry_after') is None or now >= item['retry_after']:
                ready_items.append(item)
        
        return ready_items

class RateLimiter:
    """Handles intelligent rate limiting and backoff."""
    
    def __init__(self, state: ProcessingState):
        self.state = state
    
    def wait_for_quota(self, estimated_tokens: int) -> bool:
        """Wait until we can make an API call. Returns False if should abort."""
        while True:
            can_call, reason = self.state.can_make_call(estimated_tokens)
            print(f"RateLimiter: can_call={can_call}, reason={reason}")
            if can_call:
                return True
            
            if "Daily limit reached" in reason:
                # Wait until tomorrow
                now = datetime.datetime.now()
                tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
                wait_seconds = (tomorrow - now).total_seconds()
                logger.info(f"Daily quota exhausted, waiting {wait_seconds/3600:.1f} hours until reset")
                time.sleep(min(wait_seconds, 3600))  # Sleep in 1-hour chunks
                continue
            
            elif "Rate limit" in reason:
                # Wait for rate limit to reset
                wait_time = Config.MINUTE_WINDOW + 10  # Extra buffer
                logger.info(f"Rate limit hit, waiting {wait_time} seconds")
                time.sleep(wait_time)
                continue
            
            elif "Token limit" in reason:
                # Wait for token window to reset
                wait_time = Config.MINUTE_WINDOW + 5
                logger.info(f"Token limit hit, waiting {wait_time} seconds")
                time.sleep(wait_time)
                continue
            
            else:
                logger.warning(f"Unknown quota issue: {reason}")
                time.sleep(60)
                continue

def estimate_tokens(text: str) -> int:
    """Estimate token count for text."""
    return len(text) // Config.TOKEN_ESTIMATION_RATIO

def chunk_text(text: str, max_tokens: int) -> List[str]:
    """Split text into chunks that fit within token limits."""
    if not text.strip():
        return [""]
    
    estimated_tokens = estimate_tokens(text)
    if estimated_tokens <= max_tokens:
        return [text]
    
    # Split by sentences first
    sentences = text.replace('.', '.|').replace('!', '!|').replace('?', '?|').split('|')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    chunks = []
    current_chunk = ""
    current_tokens = 0
    
    for sentence in sentences:
        sentence_tokens = estimate_tokens(sentence)
        
        # If single sentence is too big, split by words
        if sentence_tokens > max_tokens:
            words = sentence.split()
            for word in words:
                word_tokens = estimate_tokens(word + " ")
                if current_tokens + word_tokens > max_tokens and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = word + " "
                    current_tokens = word_tokens
                else:
                    current_chunk += word + " "
                    current_tokens += word_tokens
        else:
            if current_tokens + sentence_tokens > max_tokens and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
                current_tokens = sentence_tokens
            else:
                current_chunk += sentence + " "
                current_tokens += sentence_tokens
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks if chunks else [text]

def transform_transcript_with_gemini(raw_transcript_text: str, video_id: str, chapter_idx: int, 
                                       state: ProcessingState, rate_limiter: RateLimiter) -> str:
    """Enhanced transcript transformation with guaranteed success and resilience.
    
    Args:
        raw_transcript_text: Raw transcript text to clean
        video_id: Video ID for tracking
        chapter_idx: Chapter index for tracking
        state: Processing state manager
        rate_limiter: Rate limiter instance
        
    Returns:
        Cleaned transcript text - guaranteed to succeed or raise exception
        
    Raises:
        Exception: Only for truly unrecoverable errors (malformed input, etc.)
    """
    if not raw_transcript_text or not raw_transcript_text.strip():
        logger.warning(f"Empty transcript text for {video_id} chapter {chapter_idx}")
        return ""
    
    item_id = f"{video_id}_ch{chapter_idx}"
    
    source_hash = content_hash(raw_transcript_text)
    saved_text = state.completed_text(item_id, source_hash)
    if saved_text is not None:
        return saved_text
    if not GEMINI_AVAILABLE or not GEMINI_API_KEY:
        raise RuntimeError("Gemini configuration is required for new cleaning")
    genai.configure(api_key=GEMINI_API_KEY)

    # Chunk the text if necessary
    max_tokens_per_chunk = Config.TOKENS_PER_MINUTE // 2  # Conservative per-call limit
    chunks = chunk_text(raw_transcript_text, max_tokens_per_chunk)
    
    cleaned_chunks = []
    retry_delay = Config.MIN_RETRY_DELAY
    
    for chunk_idx, chunk in enumerate(chunks):
        chunk_item_id = f"{item_id}_chunk{chunk_idx}"
        estimated_tokens = estimate_tokens(chunk) * 2  # Input + output estimate
        
        while True:  # Infinite retry loop - never give up!
            try:
                # Wait for API quota availability
                if not rate_limiter.wait_for_quota(estimated_tokens):
                    logger.error(f"Rate limiter indicated abort for {chunk_item_id}")
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * Config.BACKOFF_MULTIPLIER, Config.MAX_RETRY_DELAY)
                    continue
                print(f"Processing {chunk} with estimated tokens: {estimated_tokens}")
                
                # Prepare the prompt
                prompt = f"""
Format and minimally clean the provided transcript. Your main goal is to structure the text into concise sentences and paragraphs.

Only remove distracting filler words (like "um," "ah") and obvious, repetitive phrases (n-grams). Preserve the original wording as much as possible. Do not rephrase sentences or change the core vocabulary. The output should be only the cleaned text.

Raw Text:
{chunk}
""".strip()
                # Make the API call
                logger.debug(f"Cleaning transcript chunk {chunk_idx+1}/{len(chunks)} for {item_id}")
                is_retry =  retry_delay != Config.MIN_RETRY_DELAY
                model_id =  'gemma-3-27b-it' if ( is_retry or estimated_tokens < 12000) else 'gemini-2.5-flash-lite' 
                model_id = 'gemini-2.5-flash' if estimated_tokens < 4000 else  'gemini-2.5-flash-lite'
                print(f"Using model {model_id} {estimated_tokens} for {chunk_item_id} (is_retry={is_retry})")
                model = genai.GenerativeModel(model_id)
                response = model.generate_content(prompt,
                    safety_settings={
                        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                        'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                })
                response_text = response.text
                print(f"Gemini response for {chunk_item_id}: {response_text[:100]}...")  # Debugging line
                if not response_text:
                    logger.warning(f"Empty response from Gemini for {chunk_item_id}")
                    # Treat empty response as a retryable error
                    raise Exception("Empty response from Gemini API")
                
                cleaned_text = response_text.strip()
                cleaned_chunks.append(cleaned_text)
                
                logger.debug(f"Successfully cleaned chunk {chunk_idx+1}/{len(chunks)} for {item_id}: {len(chunk)} -> {len(cleaned_text)} chars")
                
                # Reset retry delay on success
                retry_delay = Config.MIN_RETRY_DELAY
                break  # Success - move to next chunk
                
            except KeyboardInterrupt:
                logger.info("Processing interrupted by user")
                raise
                
            except Exception as e:
                error_msg = str(e).lower()
                logger.error(f"Error cleaning {chunk_item_id}: {e}")
                
                # Classify error type and adjust retry strategy
                if "quota" in error_msg or "rate" in error_msg or "limit" in error_msg:
                    # Rate/quota error - wait longer
                    wait_time = retry_delay * 2
                    logger.info(f"Rate/quota error for {chunk_item_id}, waiting {wait_time} seconds")
                    time.sleep(wait_time)
                    
                elif "network" in error_msg or "connection" in error_msg or "timeout" in error_msg:
                    # Network error - shorter wait
                    wait_time = min(retry_delay, 300)  # Max 5 minutes for network errors
                    logger.info(f"Network error for {chunk_item_id}, waiting {wait_time} seconds")
                    time.sleep(wait_time)
                    
                elif "invalid" in error_msg or "malformed" in error_msg:
                    # Potentially unrecoverable error
                    logger.error(f"Potentially unrecoverable error for {chunk_item_id}: {e}")
                    state.mark_failed(chunk_item_id, str(e))
                    raise Exception(f"Unrecoverable error processing {chunk_item_id}: {e}")
                    
                else:
                    # Generic error - standard backoff
                    logger.info(f"Generic error for {chunk_item_id}, waiting {retry_delay} seconds before retry")
                    time.sleep(retry_delay)
                
                # Exponential backoff for next attempt
                retry_delay = min(retry_delay * Config.BACKOFF_MULTIPLIER, Config.MAX_RETRY_DELAY)
                
                # Record failure for monitoring
                state.mark_failed(chunk_item_id, str(e), time.time() + retry_delay)
    
        # Persistence failures must not retry an already successful provider call.
        state.record_api_call(estimated_tokens)

    # Combine all cleaned chunks
    final_cleaned_text = " ".join(cleaned_chunks).strip()
    
    # Persist the cleaned result and completion marker together.
    state.save_completed_text(item_id, source_hash, final_cleaned_text)
    
    logger.info(f"Successfully cleaned complete transcript for {item_id}: {len(raw_transcript_text)} -> {len(final_cleaned_text)} chars")
    return final_cleaned_text

# Import the rest of the functions from the original file
def time_to_seconds(time_str: str) -> float:
    """Converts a time string of the format HH:MM:SS,ms to seconds."""
    try:
        h, m, s_ms = time_str.replace(',', '.').split(':')
        if '.' in s_ms:
            s, ms = s_ms.split('.')
            return int(h) * 3600 + int(m) * 60 + float(s) + float(f"0.{ms}")
        else:
            return int(h) * 3600 + int(m) * 60 + float(s_ms)
    except (ValueError, IndexError) as e:
        logger.error(f"Invalid time format: {time_str}")
        raise ValueError(f"Invalid time format: {time_str}") from e

def chapter_time_to_seconds(time_str: str) -> int:
    """Converts a time string of the format HH:MM:SS or MM:SS to seconds."""
    try:
        parts = list(map(int, time_str.split(':')))
        if len(parts) == 2:
            return parts[0] * 60 + parts[1]
        elif len(parts) == 3:
            return parts[0] * 3600 + parts[1] * 60 + parts[2]
        else:
            raise ValueError(f"Invalid time format: {time_str}")
    except (ValueError, IndexError) as e:
        logger.error(f"Invalid chapter time format: {time_str}")
        raise ValueError(f"Invalid chapter time format: {time_str}") from e

def parse_srt(srt_content: str) -> List[Dict[str, any]]:
    """Parses SRT content and returns a list of subtitles with start and end times in seconds."""
    if not srt_content or not srt_content.strip():
        logger.warning("Empty SRT content provided")
        return []
    
    subtitles = []
    blocks = srt_content.strip().split('\n\n')
    
    for i, block in enumerate(blocks):
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            try:
                subtitle_num = int(lines[0])
                
                if ' --> ' not in lines[1]:
                    logger.warning(f"Invalid timing format in subtitle {subtitle_num}: {lines[1]}")
                    raise ValueError("Invalid subtitle timing")
                    
                start_str, end_str = lines[1].split(' --> ')
                start_time = time_to_seconds(start_str.strip())
                end_time = time_to_seconds(end_str.strip())
                
                if start_time >= end_time:
                    logger.warning(f"Invalid timing in subtitle {subtitle_num}: start >= end")
                    raise ValueError("Invalid subtitle timing")
                
                text = ' '.join(lines[2:]).strip()
                if not text:
                    raise ValueError("Empty subtitle text")
                if text:
                    subtitles.append({
                        "start": start_time, 
                        "end": end_time, 
                        "text": text,
                        "index": subtitle_num
                    })
            except (ValueError, IndexError) as e:
                raise ValueError(f"Invalid subtitle block {i+1}: {e}") from e
        else:
            raise ValueError(f"Incomplete subtitle block: {i+1}")
    
    logger.info(f"Parsed {len(subtitles)} valid subtitles from {len(blocks)} blocks")
    return subtitles

def validate_chapters_data(chapters_data: Dict[str, Any], video_id: str) -> bool:
    """Validate the structure of chapters data."""
    if not isinstance(chapters_data, dict):
        logger.error(f"Invalid chapters data for {video_id}: not a dictionary")
        return False
        
    if 'chapters' not in chapters_data:
        logger.error(f"Missing 'chapters' key in chapters data for {video_id}")
        return False
        
    if not isinstance(chapters_data['chapters'], list):
        logger.error(f"Invalid chapters data for {video_id}: 'chapters' is not a list")
        return False
        
    for i, chapter in enumerate(chapters_data['chapters']):
        if not isinstance(chapter, dict):
            logger.error(f"Invalid chapter {i} for {video_id}: not a dictionary")
            return False
            
        required_fields = ['title', 'start_timestamp', 'end_timestamp']
        for field in required_fields:
            if field not in chapter:
                logger.error(f"Missing '{field}' in chapter {i} for {video_id}")
                return False
                
    return True

def process_video(video_id: str, base_path: Path, state: ProcessingState, rate_limiter: RateLimiter) -> bool:
    """Enhanced video processing with guaranteed transcript cleaning."""
    logger.info(f"Processing video: {video_id}")
    
    # Validate input parameters
    if not video_id or not video_id.strip():
        logger.error("Empty video_id provided")
        return False
        
    if not isinstance(base_path, Path) or not base_path.exists():
        logger.error(f"Invalid base_path: {base_path}")
        return False
    
    chapters_file = base_path / f"{video_id}_chapters.json"
    srt_file = base_path / f"{video_id}.srt"
    output_file = base_path / f"{video_id}_v2_content.json"
    
    # Validate required input files exist
    missing_files = []
    if not chapters_file.exists():
        missing_files.append(str(chapters_file))
    if not srt_file.exists():
        missing_files.append(str(srt_file))
        
    if missing_files:
        logger.warning(f"Skipping {video_id} - missing files: {', '.join(missing_files)}")
        return False
    
    try:
        # Load and validate chapters data
        logger.debug(f"Loading chapters file: {chapters_file}")
        with open(chapters_file, 'r', encoding='utf-8') as f:
            chapters_data = json.load(f)
            
        if not validate_chapters_data(chapters_data, video_id):
            return False

        # Load and parse SRT content
        logger.debug(f"Loading SRT file: {srt_file}")
        with open(srt_file, 'r', encoding='utf-8') as f:
            srt_content = f.read()

        raw_transcript = parse_srt(srt_content)
        if not raw_transcript:
            logger.warning(f"No valid subtitles found for {video_id}")
            return False

        intervals = [(chapter_time_to_seconds(ch['start_timestamp']),
                      chapter_time_to_seconds(ch['end_timestamp']))
                     for ch in chapters_data['chapters']]
        assigned = assign_subtitles(raw_transcript, intervals)
        source_hashes = {
            'srt': content_hash(srt_content),
            'chapters': content_hash(chapters_data),
            'cleaning_version': Config.CLEANING_VERSION,
        }
        if output_file.exists():
            previous = json.loads(output_file.read_text(encoding='utf-8'))
            if (previous.get('source_hashes') == source_hashes
                    and previous.get('chapters_hash') == content_hash(previous.get('chapters'))
                    and previous.get('video_id') == video_id
                    and previous.get('total_chapters') == len(intervals)
                    and len(previous.get('chapters', [])) == len(intervals)
                    and all(ch.get('cleaned_transcript_text', '').strip()
                            and ch.get('source_subtitles') == assigned[i]
                            for i, ch in enumerate(previous['chapters']))):
                return True
            raise ValueError(f"Existing output is unverified or stale; preserve for migration: {output_file}")

        # Process each chapter with guaranteed cleaning
        chapters_with_transcript = []
        total_chapters = len(chapters_data['chapters'])
        
        for i, chapter_info in enumerate(chapters_data['chapters']):
            logger.info(f"Processing chapter {i+1}/{total_chapters} for {video_id}: {chapter_info.get('title', 'Untitled')}")
            
            try:
                start_time_chapter = chapter_time_to_seconds(chapter_info['start_timestamp'])
                end_time_chapter = chapter_time_to_seconds(chapter_info['end_timestamp'])
                
                chapter_transcript = assigned[i]

                raw_text = " ".join([sub["text"] for sub in chapter_transcript])
                
                # Clean transcript - guaranteed to succeed
                if not raw_text.strip():
                    raise ValueError(f"Chapter has no teaching text: {i}")
                cleaned_text = transform_transcript_with_gemini(raw_text, video_id, i, state, rate_limiter)
                
                chapters_with_transcript.append({
                    'title': chapter_info['title'],
                    'start': start_time_chapter,
                    'end': end_time_chapter,
                    'cleaned_transcript_text': cleaned_text,
                    'subtitle_count': len(chapter_transcript),
                    'source_subtitles': chapter_transcript,
                })
                
            except Exception as e:
                logger.error(f"Error processing chapter {i+1} for {video_id}: {e}")
                # In V2, we don't continue on chapter failures - we need all chapters cleaned
                raise e

        if not chapters_with_transcript:
            logger.error(f"No valid chapters processed for {video_id}")
            return False

        # Create result structure
        result = {
            "video_id": video_id,
            "total_chapters": len(chapters_with_transcript),
            "processed_at": str(datetime.datetime.now()),
            "version": "v2-integrity-1",
            "source_hashes": source_hashes,
            "chapters_hash": content_hash(chapters_with_transcript),
            "chapters": chapters_with_transcript,
        }

        # Save result
        logger.debug(f"Saving output to: {output_file}")
        atomic_json_write(output_file, result)
        
        logger.info(f"Successfully processed {video_id}: {len(chapters_with_transcript)} chapters, {len(raw_transcript)} subtitles")
        return True
    
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in chapters file for {video_id}: {e}")
        return False
    except UnicodeDecodeError as e:
        logger.error(f"Encoding error reading files for {video_id}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error processing {video_id}: {e}")
        # In V2, we don't fail silently - we need to ensure all videos are processed
        raise e

def get_video_ids_from_directory(directory: Path) -> List[str]:
    """Extract unique video IDs from files in a directory."""
    video_ids = set()
    
    for file in directory.iterdir():
        if file.is_file() and file.suffix in Config.SUPPORTED_EXTENSIONS:
            stem = file.stem
            if '_' in stem:
                video_id = stem.split('_')[0]
            else:
                video_id = stem
            
            if len(video_id) == 11 and video_id.replace('-', '').replace('_', '').isalnum():
                video_ids.add(video_id)
            else:
                logger.debug(f"Skipping invalid video ID format: {video_id}")
    
    return sorted(list(video_ids))

def main() -> int:
    """Enhanced main function with resilient processing."""
    Config.setup_logging()
    logger.info("Starting transcript chapter extraction process V2")
    
    # Initialize state management
    state = ProcessingState()
    rate_limiter = RateLimiter(state)
    
    try:
        # Find working directory
        current_dir = Path.cwd().parent.parent / "GeminiLongContext"
        logger.info(f"Working directory: {current_dir}")
        
        # Get all directories that start with "PL" (playlist IDs)
        playlist_dirs = [d for d in current_dir.iterdir() if d.is_dir() and d.name.startswith('PL')]
        
        if not playlist_dirs:
            logger.warning("No playlist directories found (directories starting with 'PL')")
            return 0
        
        logger.info(f"Found {len(playlist_dirs)} playlist directories")
        
        # Statistics tracking
        total_videos = 0
        successful_videos = 0
        failed_videos = 0
        skipped_videos = 0
        
        # Process failed items from previous runs first
        failed_items = state.get_failed_items_ready_for_retry()
        if failed_items:
            logger.info(f"Found {len(failed_items)} failed items ready for retry")
        
        for playlist_dir in sorted(playlist_dirs):
            logger.info(f"Processing playlist: {playlist_dir.name}")
            
            try:
                video_ids = get_video_ids_from_directory(playlist_dir)
                
                if not video_ids:
                    logger.warning(f"No valid video IDs found in {playlist_dir.name}")
                    continue
                
                logger.info(f"Found {len(video_ids)} videos in {playlist_dir.name}")
                total_videos += len(video_ids)
                
                # Process each video with guaranteed cleaning
                for video_id in video_ids:
                    try:
                        logger.info(f"Processing video {video_id} ({successful_videos + failed_videos + 1}/{total_videos})")
                        
                        # Process with resilient logic
                        result = process_video(video_id, playlist_dir, state, rate_limiter)
                        
                        if result:
                            successful_videos += 1
                            state.mark_completed(f"{video_id}_processed")
                            logger.info(f"✓ Completed {video_id}")
                        else:
                            failed_videos += 1
                            logger.error(f"✗ Failed {video_id}")
                            
                    except KeyboardInterrupt:
                        logger.info("Process interrupted by user")
                        raise
                    except Exception as e:
                        logger.error(f"Unexpected error processing {video_id}: {e}")
                        failed_videos += 1
                        state.mark_failed(f"{video_id}_processed", str(e))
                        
            except Exception as e:
                logger.error(f"Error processing playlist {playlist_dir.name}: {e}")
                continue
        
        # Final statistics
        logger.info(f"Processing complete:")
        logger.info(f"  Total videos: {total_videos}")
        logger.info(f"  Successful: {successful_videos}")
        logger.info(f"  Skipped: {skipped_videos}")
        logger.info(f"  Failed: {failed_videos}")
        logger.info(f"  Daily API calls used: {state.state['daily_call_count']}/{Config.DAILY_CALL_LIMIT}")
        
        if failed_videos > 0:
            logger.info(f"Failed videos will be retried in future runs")
            logger.info(f"Run this script again to continue processing failed items")
        
        return 0 if failed_videos == 0 else 1
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        state.save_state()  # Ensure state is saved on interrupt
        return 130
    except Exception as e:
        logger.error(f"Fatal error in main process: {e}")
        state.save_state()  # Ensure state is saved on error
        return 1

def test_model_list( ):
    """Test function to list available Gemini models."""
    if not GEMINI_AVAILABLE:
        logger.error("Gemini AI not available - cannot list models")
        return
    
    try:
        models = genai.list_models()
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(model.name)
    except Exception as e:
        logger.error(f"Error listing Gemini models: {e}")

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)