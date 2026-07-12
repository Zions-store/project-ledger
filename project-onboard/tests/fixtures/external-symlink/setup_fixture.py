#!/usr/bin/env python3
"""setup_fixture.py -- materialize the external-link boundary case (2.2c).

Creates, inside the given work directory, an external filesystem link
``src/shared`` whose target resolves OUTSIDE the scanned project root, so the
external-reference boundary behavior can actually be exercised.

Platform variants (the case tests an *external filesystem link boundary*,
not specifically a POSIX symlink):

  * POSIX, or Windows with the symlink privilege : real directory **symlink**
  * Windows without that privilege               : **junction** (mount point)
  * neither possible                             : prints ``BLOCKED`` -> exit 2

Idempotent   : re-running removes any existing link first (never nests).
Deterministic: the external target has fixed contents.
Non-invasive : writes only inside <work_dir> (and a sibling target dir);
               never touches the committed fixture.

Usage: python setup_fixture.py <work_dir>
Exit : 0 = symlink or junction created and resolves outside root
       2 = BLOCKED (no link could be created) or bad arguments
"""
from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

IO_REPARSE_TAG_SYMLINK = 0xA000000C
IO_REPARSE_TAG_MOUNT_POINT = 0xA0000003  # junction


def _remove_link(link: Path) -> None:
    try:
        os.lstat(link)
    except FileNotFoundError:
        return
    try:
        os.unlink(link)
        return
    except OSError:
        pass
    try:
        os.rmdir(link)
        return
    except OSError:
        pass
    shutil.rmtree(link, ignore_errors=True)


def _object_type(link: Path) -> str:
    try:
        lst = os.lstat(link)
    except FileNotFoundError:
        return "missing"
    tag = getattr(lst, "st_reparse_tag", 0)
    if tag == IO_REPARSE_TAG_SYMLINK:
        return "symlink"
    if tag == IO_REPARSE_TAG_MOUNT_POINT:
        return "junction"
    if stat.S_ISLNK(lst.st_mode):
        return "symlink"
    if stat.S_ISDIR(lst.st_mode):
        return "ordinary-directory"
    return "ordinary-file"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python setup_fixture.py <work_dir>", file=sys.stderr)
        return 2
    work = Path(sys.argv[1]).resolve()
    if not work.is_dir():
        print(f"BLOCKED: work dir does not exist: {work}", file=sys.stderr)
        return 2

    # External target OUTSIDE the scanned root (sibling of the work dir).
    target = (work.parent / f"{work.name}__external_target").resolve()
    target.mkdir(parents=True, exist_ok=True)
    with open(target / "external_marker.txt", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("external dependency content outside project root\n")

    src = work / "src"
    src.mkdir(parents=True, exist_ok=True)
    link = src / "shared"
    _remove_link(link)  # idempotent

    made = None
    try:  # 1) real symlink (POSIX, or Windows w/ privilege)
        os.symlink(target, link, target_is_directory=True)
        made = "symlink"
    except (OSError, NotImplementedError, AttributeError):
        made = None
    if made is None and os.name == "nt":  # 2) junction fallback
        try:
            subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link), str(target)],
                check=True, capture_output=True,
            )
            made = "junction"
        except (OSError, subprocess.CalledProcessError):
            made = None

    if made is None:
        print("BLOCKED: could not create symlink or junction on this host")
        return 2

    obj = _object_type(link)
    resolved = Path(os.path.realpath(link))
    work_prefix = str(work) + os.sep
    outside = (str(resolved) != str(work)) and (not str(resolved).startswith(work_prefix))

    print(f"object_type={obj}")
    print(f"link={link}")
    print(f"resolved_target={resolved}")
    print(f"target_outside_scan_root={'yes' if outside else 'no'}")

    if obj not in ("symlink", "junction"):
        print("BLOCKED: created object is not a link")
        return 2
    if not outside:
        print("BLOCKED: link target does not resolve outside scan root")
        return 2
    print("SETUP_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
