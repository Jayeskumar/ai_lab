"""Compare stored timings (before my re-run) with the re-run, for EXP-C15-03, EXP-C18-04, EXP-C18-05."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
B = lambda e: json.load(open(os.path.join(os.path.dirname(__file__), 'out', 'lab_rerun_before', e + '.json')))
A = lambda e: json.load(open(os.path.join(ROOT, 'results', e + '.json')))
out = {}
b, a = B('EXP-C15-03')['results']['timings'], A('EXP-C15-03')['results']['timings']
rows = []
for k in sorted(b):
    if 'speedup' in b[k]:
        rows.append((k, b[k]['speedup'], a[k]['speedup']))
out['C15-03 speedups (before, after)'] = rows
# claims: affine at L=1024; fuse; commutative
def sel(pred):
    return [(k, x, y) for k, x, y in rows if pred(k)]
aff = ['xor Z2', 'x+y Z3', 'x+2y+1 Z3', '2x+2y Z3', 'golden']
summ = {}
for t in (100, 1000, 10000, 100000):
    vals_b = [x for k, x, y in rows if any(k.startswith(m) for m in aff) and '|L=1024|' in k and k.endswith(f't={t}')]
    vals_a = [y for k, x, y in rows if any(k.startswith(m) for m in aff) and '|L=1024|' in k and k.endswith(f't={t}')]
    summ[f'affine L=1024 t={t}'] = {'before': [min(vals_b), max(vals_b)], 'after': [min(vals_a), max(vals_a)]}
for t in (100, 1000, 10000, 100000):
    vb = [x for k, x, y in rows if k.startswith(('mult mod 3', 'min (chain', 'GF(4)')) and '|L=1024|' in k and k.endswith(f't={t}')]
    va = [y for k, x, y in rows if k.startswith(('mult mod 3', 'min (chain', 'GF(4)')) and '|L=1024|' in k and k.endswith(f't={t}')]
    summ[f'commutative L=1024 t={t}'] = {'before': [min(vb), max(vb)], 'after': [min(va), max(va)]}
for L in (256, 1024, 4096):
    for t in (100, 100000):
        k = f'fuse|L={L}|t={t}'
        if k in b and 'speedup' in b[k]:
            summ[k] = {'before': b[k]['speedup'], 'after': a[k]['speedup']}
for L in (256, 1024, 4096):
    vb = [x for k, x, y in rows if any(k.startswith(m) for m in aff + ['fuse']) and f'|L={L}|' in k and k.endswith('t=100')]
    va = [y for k, x, y in rows if any(k.startswith(m) for m in aff + ['fuse']) and f'|L={L}|' in k and k.endswith('t=100')]
    summ[f'affine+fuse t=100 L={L}'] = {'before': [min(vb), max(vb)], 'after': [min(va), max(va)]}
big = {k: (b[k]['ff_s'], a[k]['ff_s']) for k in b if k.endswith('t=1000000000')}
summ['t=1e9 ff seconds (before, after)'] = big
out['C15-03 claim-relevant ranges'] = summ
b4, a4 = B('EXP-C18-04')['results']['timings']['MB_per_s'], A('EXP-C18-04')['results']['timings']['MB_per_s']
out['C18-04 MB/s (before, after)'] = {k: (b4[k], a4[k]) for k in sorted(b4)}
b5, a5 = B('EXP-C18-05')['results']['timings'], A('EXP-C18-05')['results']['timings']
out['C18-05 MB/s (before, after)'] = {k: (b5[k]['MB_per_s'], a5[k]['MB_per_s']) for k in b5}
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'out', 'timing_compare.json'), 'w'), indent=1)
print(json.dumps(out['C15-03 claim-relevant ranges'], indent=0))
print(json.dumps(out['C18-04 MB/s (before, after)']))
print(json.dumps(out['C18-05 MB/s (before, after)']))
