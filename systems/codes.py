"""Universal integer codes (cycle C11): exact bit-level encoders/decoders and length functions.

Every code here encodes integers n >= 1 into binary strings ('0'/'1').  Codes that
are conventionally defined on n >= 0 (Levenshtein, Exp-Golomb, Golomb/Rice, LEB128)
are applied to x = n - 1, so that every code gives its shortest codeword to n = 1.

Each code object provides
    encode(n) -> str
    decode(bits, pos) -> (n, new_pos)
    length(n) -> int            (== len(encode(n)), without building the string)

The *pattern-terminated* code T_p (the lab's invented family) uses as codewords the
binary words in which the pattern p occurs for the first time at the very end,
assigned to integers in order of (length, lexicographic order) -- enumerative coding
with a KMP automaton.  T_11 is the Fibonacci (C1) code and T_{1^k} the generalized
Fibonacci codes of order k (same codeword sets).
"""

from __future__ import annotations

import bisect


# ------------------------------------------------------------------ helpers
def _bin(n: int) -> str:
    return bin(n)[2:]


class Code:
    name = "code"

    def encode(self, n: int) -> str:
        raise NotImplementedError

    def decode(self, bits: str, pos: int = 0):
        raise NotImplementedError

    def length(self, n: int) -> int:
        return len(self.encode(n))

    def encode_seq(self, values) -> str:
        return "".join(self.encode(v) for v in values)

    def decode_seq(self, bits: str, count: int):
        out, pos = [], 0
        for _ in range(count):
            v, pos = self.decode(bits, pos)
            out.append(v)
        assert pos == len(bits)
        return out


# ------------------------------------------------------------------ Elias codes
class EliasGamma(Code):
    name = "Elias gamma"

    def encode(self, n):
        b = _bin(n)
        return "0" * (len(b) - 1) + b

    def decode(self, bits, pos=0):
        z = 0
        while bits[pos + z] == "0":
            z += 1
        v = int(bits[pos + z: pos + 2 * z + 1], 2)
        return v, pos + 2 * z + 1

    def length(self, n):
        return 2 * n.bit_length() - 1


class EliasDelta(Code):
    name = "Elias delta"
    _g = EliasGamma()

    def encode(self, n):
        b = _bin(n)
        return self._g.encode(len(b)) + b[1:]

    def decode(self, bits, pos=0):
        L, pos = self._g.decode(bits, pos)
        v = int("1" + bits[pos: pos + L - 1], 2)
        return v, pos + L - 1

    def length(self, n):
        L = n.bit_length()
        return 2 * L.bit_length() - 1 + L - 1


class EliasOmega(Code):
    name = "Elias omega"

    def encode(self, n):
        code = "0"
        while n > 1:
            b = _bin(n)
            code = b + code
            n = len(b) - 1
        return code

    def decode(self, bits, pos=0):
        n = 1
        while bits[pos] == "1":
            chunk = bits[pos: pos + n + 1]
            pos += n + 1
            n = int(chunk, 2)
        return n, pos + 1

    def length(self, n):
        total = 1
        while n > 1:
            L = n.bit_length()
            total += L
            n = L - 1
        return total


class Levenshtein(Code):
    """Levenshtein's code applied to x = n - 1."""
    name = "Levenshtein"

    def encode(self, n):
        x = n - 1
        if x == 0:
            return "0"
        c, code, m = 1, "", x
        while True:
            b = _bin(m)[1:]
            code = b + code
            if len(b) == 0:
                break
            c += 1
            m = len(b)
        return "1" * c + "0" + code

    def decode(self, bits, pos=0):
        c = 0
        while bits[pos] == "1":
            c += 1
            pos += 1
        pos += 1
        if c == 0:
            return 1, pos
        N = 1
        for _ in range(c - 1):
            chunk = bits[pos: pos + N]
            pos += N
            N = int("1" + chunk, 2)
        return N + 1, pos

    def length(self, n):
        x = n - 1
        if x == 0:
            return 1
        c, total, m = 1, 0, x
        while True:
            L = m.bit_length() - 1
            total += L
            if L == 0:
                break
            c += 1
            m = L
        return c + 1 + total


# ------------------------------------------------------------------ Golomb family
class ExpGolomb(Code):
    def __init__(self, k: int):
        self.k = k
        self.name = f"Exp-Golomb({k})"

    def encode(self, n):
        w = n - 1 + (1 << self.k)
        b = _bin(w)
        return "0" * (len(b) - self.k - 1) + b

    def decode(self, bits, pos=0):
        z = 0
        while bits[pos + z] == "0":
            z += 1
        L = z + self.k + 1
        w = int(bits[pos + z: pos + z + L], 2)
        return w - (1 << self.k) + 1, pos + z + L

    def length(self, n):
        w = n - 1 + (1 << self.k)
        return 2 * w.bit_length() - self.k - 1


class Golomb(Code):
    """Golomb code with modulus M applied to x = n - 1 (unary quotient, truncated-binary remainder)."""

    def __init__(self, M: int):
        assert M >= 1
        self.M = M
        self.b = (M - 1).bit_length()          # ceil(log2 M)
        self.u = (1 << self.b) - M             # number of short remainders
        self.name = f"Golomb({M})" if M & (M - 1) else f"Rice({self.b})"

    def encode(self, n):
        x = n - 1
        q, r = divmod(x, self.M)
        out = "1" * q + "0"
        if self.b == 0:
            return out
        if r < self.u:
            return out + format(r, f"0{self.b - 1}b") if self.b > 1 else out
        return out + format(r + self.u, f"0{self.b}b")

    def decode(self, bits, pos=0):
        q = 0
        while bits[pos] == "1":
            q += 1
            pos += 1
        pos += 1
        if self.b == 0:
            return q * self.M + 1, pos
        r = int(bits[pos: pos + self.b - 1], 2) if self.b > 1 else 0
        if self.b > 1 and r < self.u:
            pos += self.b - 1
        else:
            r = int(bits[pos: pos + self.b], 2) - self.u
            pos += self.b
        return q * self.M + r + 1, pos

    def length(self, n):
        q, r = divmod(n - 1, self.M)
        if self.b == 0:
            return q + 1
        return q + 1 + (self.b - 1 if r < self.u else self.b)


class LEB128(Code):
    """Little-endian base-128 varint of x = n - 1 (8 bits per group, continuation flag first)."""
    name = "LEB128 varint"

    def encode(self, n):
        x = n - 1
        out = []
        while True:
            byte = x & 0x7F
            x >>= 7
            out.append(("1" if x else "0") + format(byte, "07b"))
            if not x:
                return "".join(out)

    def decode(self, bits, pos=0):
        x, shift = 0, 0
        while True:
            more = bits[pos] == "1"
            x |= int(bits[pos + 1: pos + 8], 2) << shift
            pos += 8
            shift += 7
            if not more:
                return x + 1, pos

    def length(self, n):
        return 8 * max(1, -(-(n - 1).bit_length() // 7))


# ------------------------------------------------------------------ Fibonacci (C1)
class FibonacciC1(Code):
    """Zeckendorf digits (weights 1, 2, 3, 5, ...; least significant first) followed by '1'."""
    name = "Fibonacci C1"

    def __init__(self):
        self.F = [1, 2]
        while len(self.F) < 200:
            self.F.append(self.F[-1] + self.F[-2])

    def encode(self, n):
        k = bisect.bisect_right(self.F, n) - 1
        digits = ["0"] * (k + 1)
        while n:
            j = bisect.bisect_right(self.F, n) - 1
            digits[j] = "1"
            n -= self.F[j]
        return "".join(digits) + "1"

    def decode(self, bits, pos=0):
        n, i, prev = 0, 0, "0"
        while True:
            c = bits[pos + i]
            if c == "1" and prev == "1":
                return n, pos + i + 1
            if c == "1":
                n += self.F[i]
            prev = c
            i += 1

    def length(self, n):
        return bisect.bisect_right(self.F, n) + 1


class FraenkelKleinC3(Code):
    """Fraenkel-Klein (1996) code C3: C1 codewords minus their final 1, each length block taken twice with prefixes
    '10' then '11' (101, 111, 1001, 1101, 10001, ...).  Uniquely decipherable but NOT prefix-free: a codeword ends
    where '011' is seen with its last 1 being the first bit of the next codeword (the input is virtually followed by
    '1'); the codeword 111 is recognised as '1111'."""
    name = "Fraenkel-Klein C3"

    def __init__(self):
        self.c1 = FibonacciC1()
        self.Fs = [0, 1, 1]                        # standard Fibonacci numbers F_0, F_1, F_2, ...
        while len(self.Fs) < 400:
            self.Fs.append(self.Fs[-1] + self.Fs[-2])
        self.cum = [max(2 * f - 2, 0) for f in self.Fs]   # cum[r] = codewords of length <= r = 2 F_r - 2

    def length(self, n):
        return bisect.bisect_left(self.cum, n)

    def encode(self, n):
        r = self.length(n)
        t = n - self.cum[r - 1] - 1
        b, j = divmod(t, self.Fs[r - 2])
        return ("11" if b else "10") + self.c1.encode(self.Fs[r - 1] + j)[:-1]

    def decode(self, bits, pos=0):
        def bit(i):
            return bits[i] if i < len(bits) else "1"
        if bit(pos) == bit(pos + 1) == bit(pos + 2) == bit(pos + 3) == "1":
            return 2, pos + 3
        i = pos + 1
        while not (bit(i) == "0" and bit(i + 1) == "1" and bit(i + 2) == "1"):
            i += 1
        end = i + 2
        r = end - pos
        j, _ = self.c1.decode(bits[pos + 2:end] + "1")
        return self.cum[r - 1] + (bits[pos + 1] == "1") * self.Fs[r - 2] + (j - self.Fs[r - 1]) + 1, end


# ------------------------------------------------------------------ pattern-terminated codes
class PatternCode(Code):
    """T_p: codewords = binary words whose first occurrence of p is at the end (enumerative coding)."""

    def __init__(self, p: str, max_len: int = 400):
        assert p and set(p) <= {"0", "1"}
        self.p = p
        self.k = k = len(p)
        self.name = f"T_{p}"
        # KMP automaton: states 0..k (k = pattern just completed)
        fail = [0] * (k + 1)
        j = 0
        for i in range(1, k):
            while j and p[i] != p[j]:
                j = fail[j]
            if p[i] == p[j]:
                j += 1
            fail[i + 1] = j
        self.delta = []
        for s in range(k):
            row = {}
            for ch in "01":
                t = s
                while t and p[t] != ch:
                    t = fail[t]
                row[ch] = t + 1 if p[t] == ch else 0
            self.delta.append(row)
        # N[r][s]: number of words of length r leading from state s to state k exactly at the last letter
        N = [[0] * (k + 1) for _ in range(max_len + 1)]
        N[0][k] = 1
        for r in range(1, max_len + 1):
            for s in range(k):
                N[r][s] = N[r - 1][self.delta[s]["0"]] + N[r - 1][self.delta[s]["1"]]
        self.N = N
        self.count = [N[L][0] for L in range(max_len + 1)]          # codewords of each length
        self.cum = []
        acc = 0
        for c in self.count:
            acc += c
            self.cum.append(acc)                                       # codewords of length <= L
        self.max_len = max_len

    def length(self, n):
        L = bisect.bisect_left(self.cum, n)
        if L > self.max_len:
            raise ValueError("increase max_len")
        return L

    def encode(self, n):
        L = self.length(n)
        rank = n - (self.cum[L - 1] if L else 0) - 1
        s, out = 0, []
        for i in range(1, L + 1):
            r = L - i
            for ch in "01":
                t = self.delta[s][ch]
                cnt = self.N[r][t]
                if rank < cnt:
                    out.append(ch)
                    s = t
                    break
                rank -= cnt
            else:
                raise AssertionError("rank out of range")
        return "".join(out)

    def decode(self, bits, pos=0):
        s, i, path = 0, 0, []
        while s != self.k:
            ch = bits[pos + i]
            path.append((s, ch))
            s = self.delta[s][ch]
            i += 1
        L = i
        rank = 0
        for idx, (st, ch) in enumerate(path, start=1):
            if ch == "1":
                rank += self.N[L - idx][self.delta[st]["0"]]
        n = (self.cum[L - 1] if L else 0) + rank + 1
        return n, pos + L


def autocorrelation(p: str) -> list[int]:
    """Coefficients c_0..c_{k-1} of Guibas-Odlyzko's correlation polynomial: c_j = 1 iff p has period j."""
    k = len(p)
    return [1 if p[j:] == p[: k - j] else 0 for j in range(k)]


def growth_rate(p: str) -> float:
    """lambda_p = 1/rho, rho the smallest positive root of x^k + (1 - 2x) c_p(x)."""
    import numpy as np
    k = len(p)
    c = autocorrelation(p)
    D = [0.0] * (k + 1)                     # coefficients in increasing powers
    for j, cj in enumerate(c):
        D[j] += cj
        D[j + 1] -= 2 * cj
    D[k] += 1
    roots = np.roots(D[::-1])
    pos = [r.real for r in roots if abs(r.imag) < 1e-9 and r.real > 0]
    return 1 / min(pos)


def baseline_codes():
    return [EliasGamma(), EliasDelta(), EliasOmega(), Levenshtein(), FibonacciC1(), LEB128(), ExpGolomb(0),
            ExpGolomb(2), ExpGolomb(4)]
