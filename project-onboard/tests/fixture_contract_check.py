#!/usr/bin/env python3
"""fixture-contract check (Linux CI).

Verifies the reproducible-fixture *contract* for the special behavior-test
cases, WITHOUT running OpenCode. It proves the fixtures can be materialized to
their intended on-disk shape; it does **not** assert Skill behavior. CI output
must therefore never claim "CASE-2.2c behavior PASS" -- only "Fixture
contract: PASS".

Checks:
  external-symlink : setup yields a REAL symlink whose target resolves outside
                     the scan root; committed fixture untouched; idempotent.
  large-notebook   : setup yields a valid nbformat-4 notebook > 524288 bytes in
                     the work copy, byte-identical across runs, without touching
                     the committed seed; idempotent.

Exit: 0 = all contracts hold; 1 = one or more contract failures.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent          # project-onboard/tests
FIXTURES = HERE / "fixtures"
THRESHOLD = 524_288
failures: list[str] = []


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_setup(fixture_dir: Path, work_dir: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(fixture_dir / "setup_fixture.py"), str(work_dir)],
        capture_output=True, text=True,
    )


def check_external_symlink() -> None:
    print("== external-symlink fixture contract ==")
    src = FIXTURES / "external-symlink"
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "case-2.2c"
        shutil.copytree(src, work)
        r1 = run_setup(src, work)
        print(r1.stdout.strip())
        if r1.returncode != 0:
            failures.append("external-symlink: setup returned non-zero / BLOCKED")
            return
        link = work / "src" / "shared"
        if os.path.islink(link):
            print("External link type: symlink")
        else:
            failures.append("external-symlink: materialized object is not a real symlink")
        resolved = Path(os.path.realpath(link))
        outside = not str(resolved).startswith(str(work.resolve()) + os.sep)
        print(f"External target outside scan root: {'PASS' if outside else 'FAIL'}")
        if not outside:
            failures.append("external-symlink: target does not resolve outside scan root")
        if (src / "src").exists():
            failures.append("external-symlink: committed fixture was modified")
        # idempotency
        r2 = run_setup(src, work)
        if r2.returncode != 0 or not os.path.islink(link):
            failures.append("external-symlink: not idempotent on second run")
        else:
            print("Idempotent: PASS")


def check_large_notebook() -> None:
    print("== large-notebook fixture contract ==")
    src = FIXTURES / "large-notebook"
    seed = src / "analysis.ipynb"
    seed_before = sha256(seed) if seed.exists() else None
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "case-4.1b"
        shutil.copytree(src, work)
        r1 = run_setup(src, work)
        print(r1.stdout.strip())
        if r1.returncode != 0:
            failures.append("large-notebook: setup returned non-zero")
            return
        nb = work / "analysis.ipynb"
        size = nb.stat().st_size
        print(f"Notebook size threshold: {'PASS' if size > THRESHOLD else 'FAIL'} ({size} bytes)")
        if size <= THRESHOLD:
            failures.append("large-notebook: size <= 524288")
        try:
            data = json.loads(nb.read_text(encoding="utf-8"))
            schema_ok = data.get("nbformat") == 4 and isinstance(data.get("cells"), list)
            print(f"Notebook schema: {'PASS' if schema_ok else 'FAIL'}")
            if not schema_ok:
                failures.append("large-notebook: invalid nbformat/cells")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"large-notebook: JSON parse error: {exc}")
        h1 = sha256(nb)
        run_setup(src, work)  # idempotency + determinism
        h2 = sha256(nb)
        if h1 != h2:
            failures.append("large-notebook: non-deterministic (hash changed on rerun)")
        else:
            print(f"Deterministic + idempotent: PASS (sha256 {h1[:16]}...)")
    seed_after = sha256(seed) if seed.exists() else None
    if seed_before != seed_after:
        failures.append("large-notebook: committed seed hash changed")
    else:
        print("Seed unchanged: PASS")


def main() -> int:
    check_external_symlink()
    print()
    check_large_notebook()
    print()
    if failures:
        print("Fixture contract: FAIL")
        for f in failures:
            print(f" - {f}")
        return 1
    print("Fixture contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
