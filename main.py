#!/usr/bin/env python3
"""Validate news.png and copy it byte-for-byte to the output directory.

Checks: PNG signature, 1024x1024 dimensions, size <= 1048576 bytes.
Output: $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
Standard library only.
"""
import hashlib
import os
import struct
import sys

MAX_BYTES = 1048576
EXPECTED_W, EXPECTED_H = 1024, 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")
    if not os.path.isfile(src):
        fail(f"{src} not found")

    with open(src, "rb") as f:
        data = f.read()

    if len(data) > MAX_BYTES:
        fail(f"news.png is {len(data)} bytes, over the {MAX_BYTES} byte limit")
    if data[:8] != PNG_SIGNATURE:
        fail("news.png does not start with the PNG signature")
    if len(data) < 33 or data[12:16] != b"IHDR":
        fail("news.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_W, EXPECTED_H):
        fail(f"news.png is {width}x{height}, expected "
             f"{EXPECTED_W}x{EXPECTED_H}")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as f:
        f.write(data)

    with open(out_path, "rb") as f:
        out_data = f.read()
    if hashlib.sha256(out_data).hexdigest() != hashlib.sha256(data).hexdigest():
        fail("entry.png is not byte-identical to news.png")

    print(f"ok: news.png {width}x{height}, {len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()}")
    print(f"ok: wrote {out_path} (byte-identical)")


if __name__ == "__main__":
    main()
