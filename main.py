#!/usr/bin/env python3
"""Copy the finished front page into the grader's output folder.

The artwork itself lives in this repository as entry.png: a 1024 by 1024
front page drawn in code at build time by generate_image.py. This
entrypoint needs no network and no third-party packages. It copies the
same file on every invocation, so repeated runs are byte-identical.

The destination is $MAKEFUN_OUTPUT_DIR when set, otherwise /output.
The copy is a plain file copy: no decoding, no re-encoding, no network.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

MAX_BYTES = 1024 * 1024


def source_image() -> Path:
    return Path(__file__).resolve().parent / "entry.png"


def destination_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def main() -> int:
    out = destination_dir()
    out.mkdir(parents=True, exist_ok=True)
    target = out / "entry.png"
    shutil.copyfile(source_image(), target)
    size = target.stat().st_size
    print(f"copied entry.png to {target} ({size} bytes, 1024x1024)")
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB cap")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
