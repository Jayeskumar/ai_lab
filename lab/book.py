"""Build the living textbook: Markdown -> standalone HTML (MathML) -> PDF.

The chapter order is given by ``textbook/src/BOOK.yaml``.  PDF export uses a
headless Chromium (``CHROMIUM`` env var, default the Playwright install) and is
skipped with a warning when no browser is available.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import yaml

from .paths import TEXTBOOK
from .util import now_iso

SRC = TEXTBOOK / "src"
BUILD = TEXTBOOK / "build"

CSS = """
body { font-family: 'DejaVu Serif', Georgia, serif; max-width: 46em; margin: 2em auto; padding: 0 1em;
       line-height: 1.5; color: #111; background: #fff; }
h1, h2, h3, h4 { font-family: 'DejaVu Sans', Helvetica, sans-serif; line-height: 1.25; }
h1 { page-break-before: always; border-bottom: 2px solid #333; padding-bottom: .2em; }
h1.title { page-break-before: avoid; border: none; text-align: center; font-size: 2.1em; }
code, pre { font-family: 'DejaVu Sans Mono', monospace; font-size: .86em; }
pre { background: #f5f5f5; padding: .6em; overflow-x: auto; border-left: 3px solid #999; }
table { border-collapse: collapse; margin: 1em 0; font-size: .9em; }
th, td { border: 1px solid #aaa; padding: .25em .5em; }
blockquote { border-left: 4px solid #4a6fa5; margin-left: 0; padding-left: 1em; color: #222; background: #f3f6fb; }
nav#TOC { page-break-after: always; }
.status { font-weight: bold; }
math { font-size: 1.05em; }
"""


def chapters() -> tuple[dict, list[Path]]:
    manifest = yaml.safe_load((SRC / "BOOK.yaml").read_text(encoding="utf-8"))
    files = [SRC / f for f in manifest["chapters"]]
    missing = [f for f in files if not f.exists()]
    if missing:
        raise FileNotFoundError(f"chapters missing: {missing}")
    return manifest, files


def _chromium() -> str | None:
    for cand in (os.environ.get("CHROMIUM"), "/opt/pw-browsers/chromium", shutil.which("chromium"),
                 shutil.which("chromium-browser"), shutil.which("google-chrome")):
        if cand and Path(cand).exists():
            return cand
    return None


def build(pdf: bool = True) -> int:
    manifest, files = chapters()
    BUILD.mkdir(parents=True, exist_ok=True)
    combined = BUILD / "book.md"
    parts = []
    for f in files:
        parts.append(f.read_text(encoding="utf-8").rstrip() + "\n")
    combined.write_text("\n\n".join(parts), encoding="utf-8")
    css = BUILD / "book.css"
    css.write_text(CSS, encoding="utf-8")
    html = BUILD / "book.html"
    cmd = ["pandoc", str(combined), "-s", "--toc", "--toc-depth=2", "--mathml", "--number-sections",
           "-c", "book.css", "--embed-resources",
           "--metadata", f"title={manifest['title']}",
           "--metadata", f"subtitle={manifest.get('subtitle', '')}",
           "--metadata", f"date=Version {manifest.get('version', '1')} — built {now_iso()}",
           "-o", str(html)]
    subprocess.run(cmd, check=True, cwd=BUILD)
    print(f"[book] wrote {html.relative_to(TEXTBOOK.parent)} ({html.stat().st_size // 1024} KiB)")
    if not pdf:
        return 0
    chrome = _chromium()
    if chrome is None:
        print("[book] no Chromium found; PDF skipped")
        return 0
    out = BUILD / "book.pdf"
    subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", html.resolve().as_uri()], check=True,
                   capture_output=True, timeout=600)
    print(f"[book] wrote {out.relative_to(TEXTBOOK.parent)} ({out.stat().st_size // 1024} KiB)")
    return 0
