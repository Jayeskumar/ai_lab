"""Historian check (CLM-C04-01/02): which published one-rule termination criteria cover the
census rules l -> r over {a,b}, 1 <= |l| <= 3, 0 <= |r| <= 3 (and the |r| <= 5 extension)?

Criteria (as stated in Geser-Waldmann-Wenzel, WST 2016, Sec. 4, and Geser, ICASE 2002-33, Sec. 3):
  E  |l| >= |r| and l != r                                  (folklore, 'easy')
  A  some letter occurs more often in l than in r           (Kurth's criterion A)
  D  l not a factor of r, and no overlap of the end of l with the beginning of r, or
     no overlap of the end of r with the beginning of l        (Kurth's criterion D)
  B  left or right barren (McNaughton; Geser ICASE 2002-33 Def. 3.1, Thm 3.3)
  Z  l = a^p b^q, r = b^r a^s and Zantema-Geser Thm 1 says terminating (either letter order)
  L  l is a factor of r (loop of length 1: non-terminating)
"""
import itertools

def words(n, alph="ab"):
    return ["".join(t) for t in itertools.product(alph, repeat=n)]

def ovl(u, v):
    """OVL(u,v): nonempty w, suffix of u and prefix of v, not (u == w == v)."""
    out = []
    for k in range(1, min(len(u), len(v)) + 1):
        w = u[len(u) - k:]
        if v.startswith(w) and not (len(u) == k and len(v) == k):
            out.append(w)
    return out

def crit_E(l, r): return len(l) >= len(r) and l != r
def crit_A(l, r): return any(l.count(c) > r.count(c) for c in "ab")
def crit_D(l, r): return (l not in r) and (not ovl(l, r) or not ovl(r, l))

def concat_set(parts, maxlen):
    """all concatenations of >= 1 parts, truncated to the last/first maxlen letters suffices"""
    return parts

def barren(l, r):
    if l in r: return False
    A = ovl(r, l); B = ovl(l, r)
    la = [l[len(a):] for a in A]            # l = alpha l_alpha
    ra = [r[:len(r) - len(a)] for a in A]   # r = r_alpha alpha
    lb = [l[:len(l) - len(b)] for b in B]   # l = l_beta beta
    rb = [r[len(b):] for b in B]            # r = beta r_beta
    def is_prefix_of_concat(x, parts):      # x prefix of some r_b1 r_b2 ... (k >= 1)
        if not parts: return False
        frontier = {""}
        for _ in range(len(x) + 1):
            new = set()
            for f in frontier:
                for p in parts:
                    g = f + p
                    if g.startswith(x): return True
                    if x.startswith(g) and len(g) < len(x): new.add(g)
            if not new: return False
            frontier = new
        return False
    def is_suffix_of_concat(x, parts):
        return is_prefix_of_concat(x[::-1], [p[::-1] for p in parts])
    left = not any(is_prefix_of_concat(x, rb) for x in la)
    right = not any(is_suffix_of_concat(x, ra) for x in lb)
    return left or right

def zg(l, r):
    for a, b in (("a", "b"), ("b", "a")):
        p = len(l) - len(l.lstrip(a)); q = len(l) - p
        if p >= 1 and q >= 1 and l == a * p + b * q:
            rr = len(r) - len(r.lstrip(b)); s = len(r) - rr
            if rr >= 1 and s >= 1 and r == b * rr + a * s:
                t = p >= s or q >= rr or (p < s < 2 * p and q < rr and rr % q) or (q < rr < 2 * q and p < s and s % p)
                return bool(t)
    return None

def classify(maxl, maxr):
    rows = []
    for nl in range(1, maxl + 1):
        for l in words(nl):
            for nr in range(0, maxr + 1):
                for r in words(nr):
                    if l == r: continue
                    rows.append((l, r))
    return rows

def _main():
      for maxr in (3, 5):
        rows = classify(3, maxr)
        uncovered = []; counts = {}
        for l, r in rows:
            tags = []
            if l in r: tags.append("L")
            if crit_E(l, r): tags.append("E")
            if crit_A(l, r): tags.append("A")
            if crit_D(l, r): tags.append("D")
            if barren(l, r): tags.append("B")
            z = zg(l, r)
            if z is True: tags.append("Z")
            if z is False: tags.append("Znt")
            key = "+".join(tags) if tags else "none"
            if not tags: uncovered.append((l, r))
            counts[key] = counts.get(key, 0) + 1
        print("|l|<=3, |r|<=%d: %d rules" % (maxr, len(rows)))
        nonterm_known = sum(1 for l, r in rows if l in r or zg(l, r) is False)
        print("  decided by L (loop of length 1) or ZG-nonterminating:", nonterm_known)
        term_known = sum(1 for l, r in rows if (l not in r) and (crit_E(l,r) or crit_A(l,r) or crit_D(l,r) or barren(l,r) or zg(l,r) is True))
        print("  covered by a published termination criterion (E/A/D/B/Z):", term_known)
        print("  rules with no published criterion applying:", len(uncovered), uncovered[:40])

if __name__ == '__main__':
    _main()
