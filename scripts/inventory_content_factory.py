#!/usr/bin/env python3
"""Inventory local metadata/artifacts; refuses a nonempty WAL and keeps its snapshot in /tmp.

Only the requested JSON report and a temporary database copy are written.
No corpus/state/database edits, application imports, credentials, or network calls.
"""
from pathlib import Path
import argparse
import sqlite3, shutil, tempfile, json, re, hashlib, ast, os
from collections import defaultdict, Counter

def main():
    parser=argparse.ArgumentParser(description="Read-only local Content Factory inventory; never imports the application or calls a provider.")
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output',type=Path,help="Write JSON here; otherwise print JSON to stdout.")
    args=parser.parse_args()
    root=args.root.resolve()
    db=root/'youtube-iug.db'
    wal=Path(str(db)+'-wal')
    before=(db.stat().st_size,db.stat().st_mtime_ns,wal.stat().st_size if wal.exists() else None)
    if wal.exists() and wal.stat().st_size != 0:
        raise RuntimeError('Nonempty WAL needs a WAL-aware copied snapshot')
    temp=Path(tempfile.mkdtemp(prefix='cf-inventory-final-'))
    snapshot=temp/db.name
    shutil.copy2(db,snapshot)
    after=(db.stat().st_size,db.stat().st_mtime_ns,wal.stat().st_size if wal.exists() else None)
    if before != after:
        raise RuntimeError('Database changed during copy')
    conn=sqlite3.connect(snapshot.as_uri()+'?mode=ro&immutable=1',uri=True)
    conn.row_factory=sqlite3.Row
    playlists=[dict(r) for r in conn.execute('SELECT source_id,title,course_name,topic,instructor,faculty_name,target_audience,study_lang,skip,entries FROM playlists')]
    sync=[dict(r) for r in conn.execute('SELECT video_id,playlist_id,downloaded_r2,synced,upload_srt_r2,skip FROM sync_github')]
    conn.close()
    metadata={p['source_id']:p for p in playlists}
    rows_by_playlist=defaultdict(list)
    for row in sync: rows_by_playlist[row['playlist_id']].append(row)
    rx=re.compile(r'^([A-Za-z0-9_-]{11})(_raw\.json|_raw\.srt|_chapters\.json|_v2_content\.json|\.srt)$')
    artifacts={}
    for label,base in [('data',root/'data'),('GeminiLongContext',root/'GeminiLongContext'),('root_sample',root)]:
        groups=defaultdict(lambda:defaultdict(list))
        directories=[]
        if label=='root_sample':
            directories=[p for p in base.iterdir() if p.is_dir() and p.name.startswith('PL')]
        else:
            for dirname,subdirs,filenames in os.walk(base):
                subdirs[:]=[name for name in subdirs if not name.startswith('.') and name not in ['gemini_logs','__pycache__']]
                directory=Path(dirname)
                directories.append(directory)
        for directory in directories:
            for path in directory.iterdir():
                if path.is_file() and (m:=rx.fullmatch(path.name)):
                    groups[m[2]][m[1]].append(path)
        artifacts[label]=groups
    raw=artifacts['data']['_raw.json']
    raw_srt=artifacts['data']['_raw.srt']
    members={(r['video_id'],r['playlist_id']) for r in sync}
    sync_ids={r['video_id'] for r in sync}
    raw_members={(vid,p.parent.name) for vid,paths in raw.items() for p in paths}
    def describe_pair(pair):
        vid,pid=pair
        rows=[r for r in rows_by_playlist[pid] if r['video_id']==vid]
        p=metadata.get(pid,{})
        return {'video_id':vid,'playlist_id':pid,'title':p.get('title'),'playlist_skip':p.get('skip'),'sync':rows}
    def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
    duplicates=[]
    for vid,paths in sorted(raw.items()):
        if len(paths)>1:
            item={'video_id':vid,'memberships':len(paths)}
            for suffix in ['_raw.json','_raw.srt']:
                checks=[]
                for label,groups in artifacts.items():
                    for p in groups[suffix].get(vid,[]):
                        checks.append({'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':digest(p)})
                item[suffix]={'distinct_hashes':len({r['sha256'] for r in checks}),'copies':checks}
            duplicates.append(item)
    playlist_artifact_counts=defaultdict(Counter)
    for label,groups in artifacts.items():
        for suffix,ids in groups.items():
            for vid,paths in ids.items():
                for pid in {path.parent.name for path in paths}:
                    playlist_artifact_counts[pid][label+suffix]+=1
    summary=[]
    for p in playlists:
        pid=p['source_id']; expected={r['video_id'] for r in rows_by_playlist[pid]}
        count=dict(playlist_artifact_counts[pid])
        entry_format='native'
        entries=p['entries']
        if isinstance(entries,str):
            try:
                entries=json.loads(entries)
                entry_format='json'
            except json.JSONDecodeError:
                try:
                    entries=ast.literal_eval(entries)
                    entry_format='python_literal'
                except (ValueError,SyntaxError):
                    entries=None
                    entry_format='unparseable'
        if isinstance(entries,dict):
            entries=entries.get('entries',entries)
        entry_ids={str(e.get('id')) for e in entries if isinstance(e,dict) and e.get('id')} if isinstance(entries,list) else set()
        summary.append({k:v for k,v in p.items() if k!='entries'}|{'sync_memberships':len(expected),'entry_format':entry_format,'entry_count':len(entries) if isinstance(entries,list) else None,'entry_ids_count':len(entry_ids),'entry_not_sync':sorted(entry_ids-expected),'sync_not_entries':sorted(expected-entry_ids),'counts':count})
    state_results=[]
    v2=artifacts['GeminiLongContext']['_v2_content.json']
    v2ids=set(v2)
    for state_path in [root/'.transcript_processing_state.json',root/'src/.transcript_processing_state.json',root/'src/etl/.transcript_processing_state.json']:
        state=json.loads(state_path.read_text())
        completed=state['completed_items']
        processed={s[:-len('_processed')] for s in completed if s.endswith('_processed')}
        failed=state['failed_items']
        state_results.append({'path':str(state_path.relative_to(root)),'last_checkpoint':state['last_checkpoint'],'completed_count':len(completed),'processed_count':len(processed),'failed_count':len(failed),'processed_missing_v2':sorted(processed-v2ids),'v2_missing_processed_count':len(v2ids-processed),'v2_missing_processed_ids':sorted(v2ids-processed),'failed_ids':[e.get('id') for e in failed],'completed_failed_overlap':sorted(set(completed)&{e.get('id') for e in failed})})
    counts={label:{suffix:{'files':sum(map(len,ids.values())),'unique_ids':len(ids)} for suffix,ids in groups.items()} for label,groups in artifacts.items()}
    result={'snapshot':str(snapshot),'database_path':str(db),'database_sha256':digest(snapshot),'db_stat':before,'wal_bytes':wal.stat().st_size if wal.exists() else None,'playlist_rows':len(playlists),'playlist_unique_ids':len(metadata),'sync_rows':len(sync),'sync_unique_pairs':len(members),'sync_unique_video_ids':len(sync_ids),'sync_playlist_count':len(rows_by_playlist),'playlist_skip_counts':dict(Counter(str(p['skip']) for p in playlists)),'sync_skip_counts':dict(Counter(str(p['skip']) for p in sync)),'counts':counts,'sync_ids_missing_any_raw':sorted(sync_ids-set(raw)),'raw_ids_without_sync':sorted(set(raw)-sync_ids),'sync_pairs_missing_raw':list(map(describe_pair,sorted(members-raw_members))),'raw_pairs_without_sync':list(map(describe_pair,sorted(raw_members-members))),'raw_json_without_raw_srt':sorted(set(raw)-set(raw_srt)),'raw_srt_without_raw_json':sorted(set(raw_srt)-set(raw)),'duplicate_raw_ids':duplicates,'playlists':summary,'state':state_results}
    payload=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if args.output:
        args.output.write_text(payload,encoding='utf-8')
        print(f"Inventory written to {args.output}; temporary immutable snapshot: {snapshot}")
    else:
        print(payload,end='')

if __name__=='__main__':
    main()
