#!/usr/bin/env python3
"""Runner for THE WHOLE DAY DAILY — make.fun news-image-20261123, akun3.

The artwork is a single 1024x1024 front page for Monday 23 November
2026: twelve numbered cards (the Kyiv rescue leads the page), a numbers
box, a dotted world map, a date-check panel and twenty-eight short
briefs — forty stories from seven regions, all from that one day.

This runner's only job is delivery. It reads the page stored beside it,
checks the byte count and SHA-256 fingerprint recorded at build time,
and writes an identical copy into the output folder. Any drift — a
resized, recompressed or swapped image — aborts the run.

Pure standard library; the PNG is never decoded, only carried.
"""

import hashlib
import os
import sys

PIN_BYTES = 119020
PIN_SHA256 = "3323bda3a21dc1a033a6151644233b1de7e73ca38ed5413b8775ab63781b5efc"
CAP_BYTES = 1048576
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_page():
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, "entry.png"), "rb") as handle:
        return handle.read()


def check_page(page):
    if page[:8] != SIGNATURE:
        sys.exit("entry.png: bad PNG signature")
    if len(page) > CAP_BYTES:
        sys.exit("entry.png: %d bytes over the 1 MiB cap" % len(page))
    if len(page) != PIN_BYTES:
        sys.exit("entry.png: expected %d bytes, found %d" % (PIN_BYTES, len(page)))
    if hashlib.sha256(page).hexdigest() != PIN_SHA256:
        sys.exit("entry.png: fingerprint mismatch")


def main():
    page = read_page()
    check_page(page)
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out, exist_ok=True)
    dest = os.path.join(out, "entry.png")
    with open(dest, "wb") as handle:
        handle.write(page)
    sys.stderr.write(
        "delivered %s — %d bytes, sha256 %s\n"
        % (dest, len(page), hashlib.sha256(page).hexdigest())
    )


if __name__ == "__main__":
    main()
