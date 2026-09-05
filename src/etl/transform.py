import pysrt
import re
from pathlib import Path
import json
from ..utils import open_file, save_file, batched
from ..ai.gemini import genai_completion
from ..config import CHUNK_SIZE

def get_transcripts(raw_transcript_file):
    subs = pysrt.open(raw_transcript_file)
    return [sub for sub in subs]

def format_timestamp(seconds, always_include_hours=False, decimal_marker="."):
    if seconds is not None:
        assert seconds >= 0, "non-negative timestamp expected"
        milliseconds = round(seconds * 1000.0)
        hours = milliseconds // 3_600_000
        milliseconds -= hours * 3_600_000
        minutes = milliseconds // 60_000
        milliseconds -= minutes * 60_000
        seconds = milliseconds // 1_000
        milliseconds -= seconds * 1_000
        hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
        return (
            f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
        )
    else:
        return seconds

def write_srt(file, segments):
    for i, segment in enumerate(segments, start=1):
        if isinstance(segment, dict):
            segment_start = segment["start"]
            segment_end = segment["end"]
            segment_text = segment["text"]
        else:
            segment_start = segment.start
            segment_end = segment.end
            segment_text = segment.text
        start_time = format_timestamp(
            segment_start, always_include_hours=True, decimal_marker=","
        )
        end_time = format_timestamp(
            segment_end, always_include_hours=True, decimal_marker=","
        )
        file.write("%d\n" % i)
        file.write("%s --> %s\n" % (start_time, end_time))
        file.write(segment_text.strip().replace("-->", "->"))
        file.write("\n\n")

def fix_typos(raw_transcript_file, output_path):
    splitter = "\n\n"
    transcripts_text = open_file(raw_transcript_file)
    chunks = list(batched(transcripts_text.split(splitter), CHUNK_SIZE))
    output = []
    for chunk in chunks:
        chunk_text = splitter.join(chunk)
        prompt = open_file('src/ai/prompts/clarify_transcript.txt').replace(
            '<<TRANSCRIPT>>', chunk_text)
        essay = genai_completion(prompt)
        if essay:
            output.append(essay.replace("```", ""))
    if output:
        save_file(output_path, splitter.join(output).replace("\n\n\n", "\n\n"))
        return True
    return False