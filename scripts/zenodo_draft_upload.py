"""Create an UNPUBLISHED Zenodo draft for the FloodWave-At raw data and upload files.
Never publishes. The token is read from ~/.zenodo_token and never printed or saved.
usage: zenodo_draft_upload.py <zenodo_raw_deposit.json> <report.json> <file> [<file> ...]
"""
import hashlib, json, os, sys, time
import requests

meta_path, report_path, files = sys.argv[1], sys.argv[2], sys.argv[3:]
TOK = open(os.path.expanduser('~/.zenodo_token')).read().strip()
H = {'Authorization': f'Bearer {TOK}'}
API = 'https://zenodo.org/api/deposit/depositions'

class HashingReader:
    def __init__(self, path):
        self.f = open(path, 'rb'); self.n = os.path.getsize(path); self.md5 = hashlib.md5(); self.sent = 0
    def __len__(self): return self.n
    def read(self, size=-1):
        b = self.f.read(1 << 22 if size is None or size < 0 else size)
        self.md5.update(b); self.sent += len(b); return b

meta = json.load(open(meta_path))['metadata']
r = requests.post(API, json={'metadata': meta}, headers=H, timeout=60)
r.raise_for_status(); dep = r.json()
bucket = dep['links']['bucket']
report = dict(deposition_id=dep['id'], draft_url=dep['links']['html'], published=False, files=[])
json.dump(report, open(report_path, 'w'), indent=1)
print('draft created', dep['id'], dep['links']['html'], flush=True)

for p in files:
    name = os.path.basename(p); t0 = time.time(); rd = HashingReader(p)
    for attempt in range(3):
        try:
            u = requests.put(f'{bucket}/{requests.utils.quote(name)}', data=rd, headers=H, timeout=3600)
            u.raise_for_status(); break
        except Exception as e:
            print(f'retry {name}: {type(e).__name__}', flush=True)
            rd = HashingReader(p); time.sleep(10)
    else:
        raise SystemExit(f'upload failed: {name}')
    remote = u.json().get('checksum', '')
    local = 'md5:' + rd.md5.hexdigest()
    ok = remote == local
    report['files'].append(dict(name=name, bytes=rd.n, md5=local, zenodo_checksum=remote, match=ok, seconds=round(time.time() - t0, 1)))
    json.dump(report, open(report_path, 'w'), indent=1)
    print(f"{'OK ' if ok else 'MISMATCH'} {name} {rd.n/1e6:.1f} MB in {time.time()-t0:.0f}s", flush=True)

state = requests.get(f"{API}/{dep['id']}", headers=H, timeout=60).json()
report['state'] = state.get('state'); report['submitted'] = state.get('submitted')
report['all_match'] = all(f['match'] for f in report['files'])
json.dump(report, open(report_path, 'w'), indent=1)
print('done: state', report['state'], 'submitted', report['submitted'], 'all checksums match', report['all_match'], flush=True)
