# Fixture: large-notebook (case 4.1b)

**Case goal:** a Jupyter notebook that exceeds the 512 KiB (524288-byte)
full-read budget, so the large-structured-text sampling strategy is exercised
(head/structure extraction instead of a full read).

The repository stores only a small, human-readable **seed** (`analysis.ipynb`,
~1-2 KB) that documents the intended structure. The large notebook that the
test actually consumes is **generated deterministically into the work copy**
by `setup_fixture.py` — it is never committed, so the repo does not carry a
large duplicated text blob.

## How to materialize

```
python setup_fixture.py <work_dir>
```

The script writes `<work_dir>/analysis.ipynb` and:

- guarantees `size > 524288` bytes (targets ~540 KiB);
- produces a **valid** notebook (`nbformat == 4`, `cells` is a list);
- is **deterministic** — fixed cell content, no time/uuid/random data, LF
  newlines forced — so the file is byte-identical (same SHA-256) on every run
  and platform;
- is **idempotent** — overwrites the target each run;
- never modifies this committed seed.

## PASS criteria

`4.1b` may be marked **PASS** only when the materialized notebook is actually
`> 524288` bytes and OpenCode does not silently skip it but samples its
structure (head/cell entry points) and reports the sampling. The report
records: path, size in bytes, SHA-256, `nbformat`, cell count, setup-run-1 /
setup-run-2 hashes (must match), and the OpenCode sampling evidence.

The Linux `fixture-contract` CI job asserts size, schema, determinism, and
that the committed seed hash is unchanged.
