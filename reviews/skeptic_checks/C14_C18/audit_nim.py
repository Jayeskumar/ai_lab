"""Audit: the lab's nim-product table (systems/quasigroup_hash.py, Fermat-power recursion) versus the skeptic's table
from Conway's mex definition (nim_mex.c). Imports the lab module only to read its output."""
import json, os, sys
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, ROOT)
from systems.quasigroup_hash import nim_product_table, nim_inverse_quasigroup
mine = np.fromfile(os.path.join(os.path.dirname(__file__), 'out', 'nim256_mex.bin'), np.uint8).reshape(256, 256)
lab = nim_product_table()
inv = np.zeros(256, np.int64)
for a in range(1, 256):
    inv[a] = int(np.nonzero(mine[a] == 1)[0][0])
x = np.arange(256)
res = {'nim_tables_equal': bool(np.array_equal(mine, lab)),
       'niminv_quasigroups_equal': bool(np.array_equal(inv[x[:, None] ^ x[None, :]].astype(np.uint8), nim_inverse_quasigroup()))}
json.dump(res, open(os.path.join(os.path.dirname(__file__), 'out', 'audit_nim.json'), 'w'))
print(res)
