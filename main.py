"""Entrypoint for the 27 Nov 2026 news-image bounty entry.

The front-page artwork (entry.png) is drawn by a separate generator;
this script only delivers it: it finds the picture sitting next to
itself, checks that it exists and is at most one mebibyte, then copies
it byte for byte into the folder the bounty harness expects.
"""

import os
import shutil
import sys

MAX_BYTES = 1024 * 1024  # one mebibyte


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("source picture not found:", src, file=sys.stderr)
        return 1
    if os.path.getsize(src) > MAX_BYTES:
        print("source picture too large:", src, file=sys.stderr)
        return 1
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out, exist_ok=True)
    shutil.copyfile(src, os.path.join(out, "entry.png"))
    print("delivered entry.png to", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
