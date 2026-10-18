"""EXP-C04-01: termination census of all one-rule systems l -> r over {a,b}, |l|,|r| <= 3."""

from collections import Counter

from systems.derivations import all_rules, check_self_embedding, classify_termination

META = {
    "id": "EXP-C04-01",
    "cycle": "C04",
    "title": "Termination census of the 196 one-rule string rewriting systems with |l|, |r| <= 3",
    "agent": "Formal Verifier",
    "question": "Which one-rule systems over {a,b} with sides of length <= 3 terminate, and can every verdict be "
                "backed by a checkable certificate?",
    "hypothesis": "Every one of the 196 rules is decided by a simple certificate: length decrease, lexicographic "
                  "monotonicity (length-preserving), a strictly decreasing linear interpretation over N, a "
                  "decreasing factor count, or a self-embedding derivation w ->+ x w y.",
    "assumptions": ["System A over {a,b}", "1 <= |l| <= 3, 0 <= |r| <= 3, l != r"],
    "methodology": "Apply the certificate searches in order; re-check every self-embedding certificate step by "
                   "step with an independent checker.",
    "falsification": "A rule left UNKNOWN, or a certificate that fails the independent check.",
}


def run():
    rows, unknown, bad_cert = [], [], []
    for rule in all_rules():
        c = classify_termination(rule)
        row = {"rule": list(rule), "status": c["status"], "proof": c.get("proof")}
        if c.get("proof") == "self-embedding":
            row["certificate"] = c["certificate"][:12]
            row["certificate_len"] = len(c["certificate"]) - 1
            if not check_self_embedding(rule, c["certificate"]):
                bad_cert.append(rule)
        elif "certificate" in c:
            row["certificate"] = c["certificate"]
        if c["status"] == "UNKNOWN":
            unknown.append(rule)
        rows.append(row)
    by_proof = Counter(r["proof"] for r in rows)
    by_status = Counter(r["status"] for r in rows)
    growing_term = [r["rule"] for r in rows if r["status"] == "TERMINATING" and len(r["rule"][1]) > len(r["rule"][0])]
    return {
        "rows": rows,
        "by_status": dict(by_status),
        "by_proof": dict(by_proof),
        "unknown": unknown,
        "bad_certificates": bad_cert,
        "growing_terminating_rules": growing_term,
        "summary": [
            f"196 rules: {dict(by_status)}; certificates by kind: {dict(by_proof)}",
            f"unknown: {len(unknown)}; certificates failing the independent check: {len(bad_cert)}",
            f"{len(growing_term)} length-increasing rules terminate (linear interpretation or factor count)",
        ],
    }
