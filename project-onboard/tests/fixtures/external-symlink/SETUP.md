# Fixture: external-symlink (case 2.2c)

**Case goal:** external filesystem *link* boundary — platform variant: symlink or junction.

The intended external link (`src/shared` -> outside the project root) is
**not committed** as a real filesystem object, because a committed symlink is
not portable: Windows checkouts may lack the symlink privilege, may have
`core.symlinks=false`, or may turn the link into a plain text file, and
junction vs. symlink semantics differ per host.

## How to materialize

```
python setup_fixture.py <work_dir>
```

The script (run against a copy of this fixture in `tests/work/<case>/`):

1. creates an external target directory **outside** the scanned root;
2. creates `src/shared` pointing at it, trying in order:
   - a real directory **symlink** (POSIX, or Windows with privilege),
   - a **junction** fallback (Windows, no elevation needed),
   - otherwise prints `BLOCKED` and exits non-zero (it never leaves an
     ordinary directory in place to be mistaken for a link);
3. prints the final `object_type`, `resolved_target`, and
   `target_outside_scan_root`.

Idempotent: re-running removes any existing link first (never nests).

## PASS criteria

`2.2c` may be marked **PASS** only when the materialized object is a real
`symlink` **or** `junction` whose target resolves outside the scan root, and
OpenCode records it as an unscanned external reference without entering it.
If neither a symlink nor a junction can be created, the case is **BLOCKED**
(the setup script's success must never be reported as Skill-behavior success).

The Linux `fixture-contract` CI job asserts this script yields a **real
symlink** (never a junction) with a target outside the scan root.
