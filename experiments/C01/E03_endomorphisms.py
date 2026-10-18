"""EXP-C01-03: multiplication emerges as composition of transformations."""

import itertools
import random

META = {
    "id": "EXP-C01-03",
    "cycle": "C01",
    "title": "Endomorphisms of the one-symbol free monoid form the semiring of natural numbers",
    "agent": "Mathematical Inventor",
    "question": "Is there a second operation on unary numerals that arises from transformations alone?",
    "hypothesis": "Endomorphisms of {a}* (substitutions a -> w) with pointwise juxtaposition (f+g)(u) = f(u)g(u) "
                  "and composition form a commutative semiring isomorphic to (N, +, x) via f -> f(a). With two "
                  "symbols modulo commutation, composition is no longer commutative.",
    "assumptions": ["System A over {a} and over {a,b} modulo commutation", "finite window of images"],
    "methodology": "Represent an endomorphism by the image of a (a word). Implement substitution and "
                   "juxtaposition on strings only; check every semiring axiom on all images a^0..a^K; check the "
                   "length map is a homomorphism. For {a,b}/commutation, sample substitutions and look for "
                   "non-commuting compositions.",
    "falsification": "Any failure of a semiring axiom, or commuting compositions for all two-symbol samples.",
    "seed": 7,
}

K = 12


def subst(image, word):
    """Apply the endomorphism a -> image to a word over {a} (pure string manipulation)."""
    return "".join(image for _ in word)


def compose(f, g):          # (f o g)(a) = f(g(a))
    return subst(f, g)


def plus(f, g):             # (f + g)(a) = f(a) g(a)
    return f + g


def run():
    imgs = ["a" * k for k in range(K + 1)]
    zero, one = "", "a"
    fails = []
    for f, g, h in itertools.product(imgs, repeat=3):
        checks = {
            "plus_assoc": plus(plus(f, g), h) == plus(f, plus(g, h)),
            "comp_assoc": compose(compose(f, g), h) == compose(f, compose(g, h)),
            "left_distrib": compose(f, plus(g, h)) == plus(compose(f, g), compose(f, h)),
            "right_distrib": compose(plus(f, g), h) == plus(compose(f, h), compose(g, h)),
        }
        fails += [(name, f, g, h) for name, ok in checks.items() if not ok]
    for f, g in itertools.product(imgs, repeat=2):
        checks = {
            "plus_comm": plus(f, g) == plus(g, f),
            "comp_comm": compose(f, g) == compose(g, f),
            "zero": plus(f, zero) == f,
            "one": compose(f, one) == f and compose(one, f) == f,
            "annihilate": compose(f, zero) == zero and compose(zero, f) == zero,
            "pluss_is_endo": all(plus(subst(f, w), subst(g, w)) == subst(plus(f, g), w) for w in imgs[:5]),
            "length_hom_plus": len(plus(f, g)) == len(f) + len(g),
            "length_hom_comp": len(compose(f, g)) == len(f) * len(g),
        }
        fails += [(name, f, g) for name, ok in checks.items() if not ok]

    # two symbols modulo commutation: a word is identified with its sorted form
    rng = random.Random(META["seed"])
    norm = lambda w: "".join(sorted(w))

    def apply2(sub, w):
        return norm("".join(sub[c] for c in w))

    noncomm = []
    for _ in range(200):
        s = {c: norm("".join(rng.choice("ab") for _ in range(rng.randint(0, 3)))) for c in "ab"}
        t = {c: norm("".join(rng.choice("ab") for _ in range(rng.randint(0, 3)))) for c in "ab"}
        st = {c: apply2(s, t[c]) for c in "ab"}
        ts = {c: apply2(t, s[c]) for c in "ab"}
        if st != ts:
            noncomm.append({"s": s, "t": t, "s_after_t": st, "t_after_s": ts})
    return {
        "window": K,
        "axiom_failures": fails[:20],
        "n_axiom_failures": len(fails),
        "two_symbol_noncommuting_examples": noncomm[:3],
        "two_symbol_noncommuting_count": len(noncomm),
        "summary": [
            f"semiring axioms + length homomorphism checked on all images a^0..a^{K}: {len(fails)} failures",
            f"two symbols mod commutation: {len(noncomm)}/200 random pairs of substitutions do not commute "
            f"(composition = 2x2 matrix product)",
        ],
    }
