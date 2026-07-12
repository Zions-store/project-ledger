#!/usr/bin/env python3
"""setup_fixture.py -- materialize the large-notebook case (4.1b).

Deterministically generates, inside the given work directory, a VALID
Jupyter notebook (``nbformat`` 4) whose size exceeds the 512 KiB
(524288-byte) full-read budget, so the large-structured-text sampling
strategy is genuinely exercised (the committed seed alone is small).

Deterministic: fixed cell content -- no time, uuid, or random data -- so
the same script yields a byte-identical file (identical SHA-256) on every
run and on every platform (LF newlines forced).
Idempotent   : overwrites the target notebook each run.
Non-invasive : writes only <work_dir>/analysis.ipynb; never touches the
               committed seed.

Usage: python setup_fixture.py <work_dir>
Exit : 0 = notebook > 524288 bytes and valid nbformat-4; 2 = failure
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

THRESHOLD = 524_288          # 512 KiB full-read budget
TARGET = 552_960             # ~540 KiB, comfortably over the threshold

_PAD_SOURCE = [
    "# deterministic padding cell to exceed the 512 KiB read budget\n",
    "x = np.arange(1000).reshape(50, 20)  # fixed values, no randomness\n",
    "result = x.sum(axis=0)\n",
]


def _serialize(nb: dict) -> str:
    # Stable, ASCII-only serialization; identical bytes on every platform.
    return json.dumps(nb, ensure_ascii=True, indent=1) + "\n"


def build_notebook() -> dict:
    nb = {
        "cells": [
            {"cell_type": "markdown", "metadata": {},
             "source": ["# Analysis notebook (generated fixture)\n",
                        "Deterministic large notebook for behavior-test case 4.1b."]},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
             "source": ["import numpy as np\n", "import pandas as pd\n"]},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
             "source": ["def load(path):\n", "    return pd.read_csv(path)\n"]},
        ],
        "metadata": {"language_info": {"name": "python"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    i = 0
    while len(_serialize(nb).encode("utf-8")) < TARGET:
        nb["cells"].append({
            "cell_type": "code", "execution_count": None,
            "metadata": {"pad_index": i}, "outputs": [], "source": _PAD_SOURCE,
        })
        i += 1
    return nb


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python setup_fixture.py <work_dir>", file=sys.stderr)
        return 2
    work = Path(sys.argv[1]).resolve()
    if not work.is_dir():
        print(f"FAILURE: work dir does not exist: {work}", file=sys.stderr)
        return 2

    nb = build_notebook()
    out = work / "analysis.ipynb"
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(_serialize(nb))

    size = out.stat().st_size
    data = json.loads(out.read_text(encoding="utf-8"))
    ok_schema = data.get("nbformat") == 4 and isinstance(data.get("cells"), list)
    digest = hashlib.sha256(out.read_bytes()).hexdigest()

    print(f"notebook_path={out}")
    print(f"size_bytes={size}")
    print(f"sha256={digest}")
    print(f"nbformat={data.get('nbformat')}")
    print(f"cell_count={len(data.get('cells', []))}")

    if size <= THRESHOLD:
        print(f"FAILURE: size {size} <= threshold {THRESHOLD}")
        return 2
    if not ok_schema:
        print("FAILURE: invalid notebook schema (nbformat/cells)")
        return 2
    print("SETUP_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
