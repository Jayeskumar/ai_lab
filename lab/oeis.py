"""OEIS look-ups for the Historian / Novelty Analyst, with an on-disk cache.

Every query and its raw answer are cached in ``cache/oeis`` (and committed),
so novelty assessments remain reproducible even if the OEIS changes or is
unreachable later.  Absence of a match is *weak* evidence of novelty only.
"""

from __future__ import annotations

import hashlib
import json
import time
import urllib.parse
import urllib.request

from .paths import OEIS_CACHE
from .util import now_iso, read_json, write_json

_last_call = [0.0]


def _query(q: str) -> dict:
    key = hashlib.sha256(q.encode()).hexdigest()[:24]
    path = OEIS_CACHE / f"{key}.json"
    cached = read_json(path)
    if cached is not None:
        return cached
    wait = 1.5 - (time.time() - _last_call[0])
    if wait > 0:
        time.sleep(wait)
    url = "https://oeis.org/search?" + urllib.parse.urlencode({"q": q, "fmt": "json"})
    with urllib.request.urlopen(url, timeout=60) as resp:
        raw = resp.read().decode("utf-8")
    _last_call[0] = time.time()
    data = json.loads(raw) if raw.strip() else None
    record = {"query": q, "fetched": now_iso(), "url": url, "response": data}
    write_json(path, record)
    return record


def search_terms(terms, max_results: int = 10) -> dict:
    """Search OEIS for a sequence of integers (uses at most the first 40 terms)."""
    terms = [int(t) for t in terms][:40]
    q = ",".join(str(t) for t in terms)
    rec = _query(q)
    resp = rec.get("response") or []
    if isinstance(resp, dict):  # older API shape
        resp = resp.get("results") or []
    hits = [{"anumber": f"A{r['number']:06d}", "name": r.get("name", "")} for r in resp[:max_results]]
    return {"query": q, "fetched": rec.get("fetched"), "n_hits": len(resp), "hits": hits}


def search_text(text: str, max_results: int = 10) -> dict:
    rec = _query(text)
    resp = rec.get("response") or []
    if isinstance(resp, dict):
        resp = resp.get("results") or []
    hits = [{"anumber": f"A{r['number']:06d}", "name": r.get("name", "")} for r in resp[:max_results]]
    return {"query": text, "fetched": rec.get("fetched"), "n_hits": len(resp), "hits": hits}


def novelty_check(terms, skip_trivial: int = 0) -> dict:
    """Search with the full prefix and, if nothing is found, with shorter windows.

    Returns a dict with ``status`` in {"MATCH", "NO MATCH", "ERROR"}.
    """
    try:
        full = search_terms(terms)
        if full["n_hits"]:
            return {"status": "MATCH", **full}
        # try a window that skips initial terms (sequences are often offset)
        alt = None
        if len(terms) > skip_trivial + 8:
            alt = search_terms(list(terms)[skip_trivial + 2: skip_trivial + 22])
            if alt["n_hits"]:
                return {"status": "MATCH (shifted window)", **alt, "full_query": full["query"]}
        return {"status": "NO MATCH", **full, "shifted_query": alt and alt["query"]}
    except Exception as exc:  # network problems must not be mistaken for novelty
        return {"status": "ERROR", "error": repr(exc), "query": ",".join(map(str, list(terms)[:40]))}
