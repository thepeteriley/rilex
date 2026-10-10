#!/usr/bin/env python3
"""Download an authorized GitHub Actions artifact with bounded HTTPS ranges.
Credentials and signed redirect URLs remain in memory and are never logged.
"""
import argparse
import concurrent.futures
import hashlib
import json
import pathlib
import subprocess
import urllib.error
import urllib.parse
import urllib.request
import zipfile
p = argparse.ArgumentParser()
p.add_argument('run_id', type=int)
p.add_argument('output', type=pathlib.Path)
p.add_argument('--repo', default='thepeteriley/rilex')
p.add_argument('--name', default='rilex-candidate')
p.add_argument('--workers', type=int, default=8)
a = p.parse_args()
if not 1 <= a.workers <= 16: p.error('workers must be 1..16')
meta = json.loads(subprocess.check_output(['gh', 'api', f'repos/{a.repo}/actions/runs/{a.run_id}/artifacts']))
artifact = next(x for x in meta['artifacts'] if x['name'] == a.name and not x['expired'])
token = subprocess.check_output(['gh', 'auth', 'token']).decode().strip()
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): return None
opener = urllib.request.build_opener(NoRedirect())
request = urllib.request.Request(f'https://api.github.com/repos/{a.repo}/actions/artifacts/{artifact["id"]}/zip', headers={'Authorization': 'Bearer '+token, 'Accept': 'application/vnd.github+json'})
try:
    opener.open(request, timeout=30)
    raise RuntimeError('Expected archive redirect')
except urllib.error.HTTPError as e:
    if e.code != 302: raise RuntimeError(f'Archive API returned HTTP {e.code}') from None
    url = e.headers['Location']
del token
if urllib.parse.urlsplit(url).scheme != 'https': raise RuntimeError('Refusing non-HTTPS archive URL')
a.output.mkdir(parents=True, exist_ok=True)
parts = a.output / '.download'
parts.mkdir(exist_ok=True)
size = artifact['size_in_bytes']
chunk = 32 * 1024 * 1024
count = (size+chunk-1)//chunk
def download(i):
    start, end = i*chunk, min(size, (i+1)*chunk)-1
    part = parts / f'{i:05}.part'
    if part.exists() and part.stat().st_size == end-start+1: return i
    req = urllib.request.Request(url, headers={'Range': f'bytes={start}-{end}'})
    with urllib.request.urlopen(req, timeout=120) as response:
        if response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{size}':
            raise RuntimeError('Server did not honor exact range')
        temporary = part.with_suffix('.partial')
        with temporary.open('wb') as output:
            while data := response.read(1024*1024): output.write(data)
        if temporary.stat().st_size != end-start+1: raise RuntimeError('Incomplete archive range')
        temporary.replace(part)
    return i
with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
    for done, future in enumerate(concurrent.futures.as_completed([pool.submit(download, i) for i in range(count)]), 1):
        future.result()
        if done % 8 == 0 or done == count: print(f'Downloaded {done}/{count} ranges', flush=True)
archive = parts / 'artifact.zip'
with archive.open('wb') as output:
    for i in range(count):
        with (parts / f'{i:05}.part').open('rb') as source:
            while data := source.read(1024*1024): output.write(data)
digest = 'sha256:'+hashlib.file_digest(archive.open('rb'), 'sha256').hexdigest()
if artifact.get('digest') and digest != artifact['digest']: raise RuntimeError('Archive digest mismatch')
with zipfile.ZipFile(archive) as z:
    for member in z.infolist():
        target = (a.output / member.filename).resolve()
        if not target.is_relative_to(a.output.resolve()): raise RuntimeError('Unsafe archive member path')
    z.extractall(a.output)
(a.output / 'artifact-provenance.json').write_text(json.dumps({'run_id': a.run_id, 'repository': a.repo, 'artifact_id': artifact['id'], 'archive_digest': digest, 'api_digest': artifact.get('digest')}, indent=2)+'\n')
print('Archive integrity verified and extracted.', flush=True)
