"""EXP-C13-04: the finite spectra {1,2} and {1,3} of CLM-C06-10 - all models affine up to N = 12?"""

import time

from systems.anchored import affine_roots, affine_system, anchored_status
from systems.magma import parse

META = {
    "id": "EXP-C13-04",
    "cycle": "C13",
    "title": "Non-affine models of the 17 finite-spectrum laws of CLM-C06-10, N <= 12",
    "agent": "Mathematical Skeptic",
    "question": "Do the seven {1,3}-laws and ten {1,2}-laws of CLM-C06-10 have anchored models (affine or not) for "
                "any N in 2..12 outside their conjectured spectra?",
    "hypothesis": "CLM-C06-10 (from C06): spectra exactly {1,3} and {1,2}; all models affine except the known "
                  "non-affine N = 2 model of x(yz) = y((yx)z).",
    "assumptions": ["N = 2..12; one SAT call per law and N with every affine table blocked (conflict budget "
                    "4,000,000); affine models counted separately from the affine system"],
    "methodology": "Spectrum(N) = (affine roots exist) or (SAT finds a non-affine model).",
    "falsification": "A model at N outside {1,3} resp. {1,2}, or a non-affine model other than the known one.",
}

LAWS13 = ["x(yz)=((zx)x)y", "x(yz)=((zx)y)x", "x(yz)=((zy)x)x", "(xy)z=y((zx)y)", "(xy)z=y((zy)x)",
          "(xy)z=z((yx)z)", "(xy)z=z((yz)x)"]
LAWS12 = ["x(yz)=y((yx)z)", "x(yz)=((xx)y)z", "x(yz)=((xx)z)y", "x(yz)=((xy)x)z", "x(yz)=((xy)y)z",
          "x(yz)=((xy)z)x", "x(yz)=((xy)z)y", "x(yz)=((xz)x)y", "x(yz)=((xz)y)x", "x(yz)=((xz)y)y"]


def run():
    t0 = time.perf_counter()
    rows = []
    for conj, laws in (("{1,3}", LAWS13), ("{1,2}", LAWS12)):
        for L in laws:
            s, t = L.split("=")
            law = (parse(s), parse(t))
            sysm = affine_system(law)
            prof = {}
            for N in range(2, 13):
                aff = len(affine_roots(sysm, N))
                st, T = anchored_status([law], N, budget=4_000_000, exclude_affine=True)
                prof[N] = {"affine": aff, "non_affine": st,
                           "example": T.tolist() if (T is not None and N <= 4) else None}
            spec = [1] + [N for N, p in prof.items() if p["affine"] or p["non_affine"] == "SAT"]
            rows.append({"law": L, "conjectured": conj, "spectrum_le12": spec,
                         "non_affine_N": [N for N, p in prof.items() if p["non_affine"] == "SAT"],
                         "unknown_N": [N for N, p in prof.items() if p["non_affine"] == "UNKNOWN"],
                         "profile": prof})
    agree = [r["law"] for r in rows if str(set(r["spectrum_le12"])).replace(" ", "") == r["conjectured"]]
    return {"rows": rows, "agree": agree, "timings": {"total_s": round(time.perf_counter() - t0, 1)},
            "summary": [f"{len(rows)} laws; spectrum (N <= 12) equals the conjectured set for {len(agree)}",
                        "non-affine models: " + "; ".join(f"{r['law']} at {r['non_affine_N']}" for r in rows
                                                          if r["non_affine_N"]),
                        f"UNKNOWN instances: {sum(len(r['unknown_N']) for r in rows)}"]}
