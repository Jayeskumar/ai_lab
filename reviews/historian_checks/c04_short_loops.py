"""Historian check (CLM-C04-02): the looping rules of the |r| <= 5 census that are neither
'l factor of r' nor in the Zantema-Geser family -- do they have loops of length 2 or 3
(the case characterised by Kurth, RAIRO ITA 30 (1996) 415-429)?"""
import itertools, sys
sys.path.insert(0, 'reviews/historian_checks')
from c04_census_criteria import words, zg, crit_E, crit_A, crit_D, barren

def steps(w, l, r):
    i = w.find(l)
    while i >= 0:
        yield w[:i] + r + w[i + len(l):]
        i = w.find(l, i + 1)

def short_loop(l, r, maxlen=10, maxsteps=3):
    for n in range(len(l), maxlen + 1):
        for t in words(n):
            if l not in t: continue
            frontier = {t}
            for k in range(1, maxsteps + 1):
                frontier = {v for u in frontier for v in steps(u, l, r)}
                for v in frontier:
                    if t in v:
                        return t, k, v
    return None

rows = []
for nl in range(1, 4):
    for l in words(nl):
        for nr in range(0, 6):
            for r in words(nr):
                if l != r and l not in r and zg(l, r) is None and not (crit_E(l,r) or crit_A(l,r) or crit_D(l,r) or barren(l,r)):
                    rows.append((l, r))
for l, r in rows:
    print(l, "->", r, ":", short_loop(l, r))
