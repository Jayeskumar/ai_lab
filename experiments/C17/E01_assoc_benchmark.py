"""EXP-C17-01: deciding associativity of a finite magma - exhaustive vs Light vs anchored vs randomised tests."""

import time

import numpy as np

from systems.law_testing import (anchored, anchored_assoc, corrupt, count_bad_triples, cyclic_group,
                                 generating_set, light, naive, rajagopalan_schulman, random_magma, random_triples)

META = {
    "id": "EXP-C17-01",
    "cycle": "C17",
    "title": "Benchmark of associativity tests: exhaustive, Light's generator test, the anchored O(n^2) test, "
             "Rajagopalan-Schulman and random triples",
    "agent": "Application Researcher",
    "question": "How much cheaper than the exhaustive n^3 check are generator-based, anchored and randomised "
                "associativity tests, on which inputs, and with which error rates?",
    "hypothesis": "H-C17-1 (bold): Light's test with a greedy generating set beats the exhaustive test by a factor "
                  ">= n/10 in table probes on every input family. H-C17-3: the Rajagopalan-Schulman test with 40 "
                  "rounds never errs on the benchmark (one-sided error <= (7/8)^40 per non-associative input).",
    "assumptions": ["n in {32, 64, 128, 256, 512}; 3 instances per randomised family", "probes = table look-ups "
                    "(machine-independent cost); wall times are medians of 3 runs on a shared, loaded machine and "
                    "are indicative only", "families: cyclic group Z_n, anchored x+y+1, left-zero band x*y = x "
                    "(needs all n generators), the first two with one corrupted entry, random magmas"],
    "methodology": "Run every algorithm on every instance; record verdict, probes, time; compare with the "
                   "exhaustive verdict; for random triples use a budget of n^2/16 samples to expose its failure "
                   "mode on near-associative inputs. The exhaustive check is charged the probes of a sequential "
                   "check that stops at the first violating triple (revised after the Skeptic's review - the first "
                   "version charged a whole 64-row slab, so its ratios on non-associative inputs measured the slab "
                   "size). Probe ratios are reported separately for associative inputs (certification, where every "
                   "test must do its full work) and non-associative inputs (refutation).",
    "falsification": "H-C17-1: a family where Light's test costs more than 10/n of the exhaustive probes. H-C17-3: a "
                     "wrong verdict of the randomised test.",
    "seed": 17,
}

SIZES = (32, 64, 128, 256, 512)


def timed(fn, *args, reps=3):
    ts, out = [], None
    for _ in range(reps):
        t0 = time.perf_counter()
        out = fn(*args)
        ts.append(time.perf_counter() - t0)
    return out, float(np.median(ts))


def run():
    rng = np.random.default_rng(META["seed"])
    rows, timings = [], {}
    for n in SIZES:
        fams = [("cyclic", cyclic_group(n)), ("anchored", anchored_assoc(n)),
                ("left_zero", np.tile(np.arange(n)[:, None], (1, n)))]
        for i in range(3):
            fams.append((f"cyclic+1err#{i}", corrupt(cyclic_group(n), rng)))
            fams.append((f"anchored+1err#{i}", corrupt(anchored_assoc(n), rng, protect_column0=True)))
            fams.append((f"random#{i}", random_magma(n, rng)))
        for fam, T in fams:
            (truth, p_naive), t_naive = timed(naive, T)
            (gens, p_gen), t_gen = timed(generating_set, T, reps=1)
            (v_light, p_light), t_light = timed(light, T, gens)
            (v_rs, p_rs), t_rs = timed(rajagopalan_schulman, T, 40, rng, reps=1)
            (v_rt, p_rt), _ = timed(random_triples, T, max(1, n * n // 16), rng, reps=1)
            row = {"n": n, "family": fam, "associative": truth,
                   "probes": {"naive": p_naive, "light": p_light, "light_incl_gens": p_light + p_gen,
                              "rs40": p_rs, "random_triples": p_rt},
                   "n_gens": len(gens),
                   "verdicts_ok": {"light": v_light == truth, "rs40": v_rs == truth, "random_triples": v_rt == truth},
                   "bad_triples": count_bad_triples(T) if n <= 128 else None}
            if fam.startswith("anchored"):
                (v_an, p_an), t_an = timed(anchored, T)
                row["probes"]["anchored"] = p_an
                row["verdicts_ok"]["anchored"] = v_an == truth
                timings[f"{n}/{fam}/anchored"] = t_an
            timings.update({f"{n}/{fam}/naive": t_naive, f"{n}/{fam}/light": t_light, f"{n}/{fam}/gens": t_gen,
                            f"{n}/{fam}/rs40": t_rs})
            rows.append(row)
    wrong = {alg: [(r["n"], r["family"]) for r in rows if not r["verdicts_ok"].get(alg, True)]
             for alg in ("light", "rs40", "anchored", "random_triples")}
    ratio = {}
    for r in rows:
        key = r["family"].split("#")[0]
        ratio.setdefault(key, {})[r["n"]] = round(r["probes"]["naive"] / r["probes"]["light_incl_gens"], 2)
    h1_fail = sorted({k for k, v in ratio.items() for n, x in v.items() if x < n / 10})
    assoc_fams = sorted({r["family"].split("#")[0] for r in rows if r["associative"]})
    nonassoc_fams = sorted({r["family"].split("#")[0] for r in rows if not r["associative"]})
    return {
        "rows": rows,
        "naive_over_light_probe_ratio": ratio,
        "wrong_verdicts": wrong,
        "h1_failing_families": h1_fail,
        "timings": timings,
        "summary": [
            f"wrong verdicts: Light {len(wrong['light'])}, anchored {len(wrong['anchored'])}, RS(40) "
            f"{len(wrong['rs40'])}, random triples (n^2/16 samples) {len(wrong['random_triples'])}",
            "certification (associative inputs) - exhaustive/Light probe ratio incl. generating set at n = 512: " +
            ", ".join(f"{k}: {ratio[k].get(512)}" for k in assoc_fams),
            "refutation (non-associative inputs, exhaustive check stopping at the first violation) - ratio at "
            "n = 512: " + ", ".join(f"{k}: {ratio[k].get(512)}" for k in nonassoc_fams),
            f"H-C17-1 fails for: {h1_fail}",
        ],
    }
