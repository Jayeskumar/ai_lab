"""Compare the code sha256 stored in results/EXP-Cnn-*.json with the current experiment scripts (C14, C15, C16, C18).
Also check whether any non-'timings' key looks volatile (runtime/time/seconds) - such keys break hash reproducibility."""
import glob, hashlib, json, os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
out = {}
volatile_pat = re.compile(r'(runtime|seconds|_s$|time|elapsed|MB_per_s|speedup)', re.I)
def walk(obj, path, hits):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'timings':
                continue
            if volatile_pat.search(str(k)):
                hits.append(path + '/' + str(k))
            walk(v, path + '/' + str(k), hits)
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:50]):
            walk(v, path + f'[{i}]', hits)
for cyc in ('C14', 'C15', 'C16', 'C18'):
    for f in sorted(glob.glob(os.path.join(ROOT, 'results', f'EXP-{cyc}-*.json'))):
        d = json.load(open(f))
        script = os.path.join(ROOT, d['code']['file'])
        cur = hashlib.sha256(open(script, 'rb').read()).hexdigest()
        hits = []
        walk(d.get('results', {}), '', hits)
        out[d['id']] = {'script': d['code']['file'], 'stored_sha256': d['code']['sha256'][:16],
                        'current_sha256': cur[:16], 'match': cur == d['code']['sha256'],
                        'error': d.get('error') is not None, 'runtime_s': d.get('runtime_s'),
                        'started': d.get('started'), 'suspicious_volatile_keys_outside_timings': hits[:10]}
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'out', 'code_hashes.json'), 'w'), indent=1)
for k, v in out.items():
    print(k, 'match' if v['match'] else 'MISMATCH', 'ERROR' if v['error'] else '', v['runtime_s'], v['started'], v['suspicious_volatile_keys_outside_timings'])
