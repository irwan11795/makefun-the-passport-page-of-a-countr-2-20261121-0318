#!/usr/bin/env python3
"""Entry point for the-passport-page-of-a-countr-2-20261121-0318 (stdlib only).

Copies the pre-rendered entry.png into the output directory and prints its
SHA-256. Verifies the file against the expected hash and fails loudly on any
mismatch. No network, no Pillow, no code generation.

The image is a flat-vector cartoon illustration of an invented passport
spread for the fictional Republic of Valdoria (holder Mara Kovac) — clearly
fictional, no real country or person.
"""
import hashlib
import os
import shutil
import sys
import tempfile
from pathlib import Path

EXPECTED_SHA256 = "3023cf992a2678b12f74a34196709f9be1f6d849bf0e9c4dfdfac7aaeb4c568b"
ENTRY_NAME = "entry.png"


def output_dir():
    for candidate in (
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        "./output",
    ):
        if candidate:
            try:
                Path(candidate).mkdir(parents=True, exist_ok=True)
                probe = Path(candidate) / ".write-test"
                probe.write_bytes(b"ok")
                probe.unlink()
                return Path(candidate)
            except OSError:
                continue
    return Path(tempfile.mkdtemp(prefix="makefun-output-"))


def main():
    here = Path(__file__).resolve().parent
    src = here / ENTRY_NAME
    if not src.is_file():
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1
    data = src.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print("error: entry.png sha256 mismatch", file=sys.stderr)
        print("  expected: " + EXPECTED_SHA256, file=sys.stderr)
        print("  actual:   " + digest, file=sys.stderr)
        return 1
    out = output_dir()
    dest = out / ENTRY_NAME
    shutil.copyfile(src, dest)
    if dest.read_bytes() != data:
        print("error: copied file differs from source", file=sys.stderr)
        return 1
    print(digest)
    print(str(dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
