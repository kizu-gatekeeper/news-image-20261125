#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261125.

Copies the bundled front-page image to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output/entry.png). Standard library only, no network, and
deterministic: every run writes the exact same bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as fh:
        head = fh.read(len(PNG_MAGIC))
    if head != PNG_MAGIC:
        print("error: bundled entry.png is not a PNG", file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        if fh.read(len(PNG_MAGIC)) != PNG_MAGIC:
            print("error: copied file failed PNG check", file=sys.stderr)
            return 1
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
