#!/usr/bin/env python3
"""THE WHOLE DAY DAILY — entry program for news-image-20261123 (akun3).

Concept: THE WHOLE DAY DAILY, a one-page broadsheet that sums up Monday
23 November 2026 — 40 stories, 7 regions, lead story the Kyiv boy pulled
alive from the rubble. This program is the deliverable's runner: it
copies the composed front page (entry.png, drawn in the recorded build
session) into the output directory, byte for byte, and refuses to run
if the image has been altered since the build.

Standard library only. No imaging libraries: the PNG is treated as an
opaque, hash-pinned artifact.
"""

import hashlib
import os
import sys

EXPECTED_BYTES = 119020
EXPECTED_SHA256 = "3323bda3a21dc1a033a6151644233b1de7e73ca38ed5413b8775ab63781b5efc"
HARD_CAP = 1048576  # competition ceiling: 1 MiB
PNG_HEADER = b"\x89PNG\r\n\x1a\n"


def load_entry():
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "entry.png"), "rb") as fh:
        return fh.read()


def verify(blob):
    if not blob.startswith(PNG_HEADER):
        sys.exit("entry.png is not a PNG file")
    if len(blob) > HARD_CAP:
        sys.exit("entry.png exceeds the 1 MiB competition cap: %d" % len(blob))
    if len(blob) != EXPECTED_BYTES:
        sys.exit("entry.png size drifted: %d != %d" % (len(blob), EXPECTED_BYTES))
    digest = hashlib.sha256(blob).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("entry.png hash drifted: %s" % digest)
    return digest


def main():
    blob = load_entry()
    digest = verify(blob)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as fh:
        fh.write(blob)
    sys.stderr.write("wrote %s (%d bytes, sha256=%s)\n" % (target, len(blob), digest))


if __name__ == "__main__":
    main()
