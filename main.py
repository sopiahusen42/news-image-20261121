#!/usr/bin/env python3
"""Copy the shipped entry.png to the make.fun output directory.

Grader contract: /bot = this repo (read-only), /output writable,
MAKEFUN_OUTPUT_DIR=/output, no network, 60 s. This program locates the
pre-built entry.png next to itself and copies it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output).

Standard library only.
"""
import os
import struct
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_DIM = 1024
MAX_BYTES = 1048576


def find_entry() -> Path:
    """Locate entry.png: next to this file, in /bot, or in the cwd."""
    here = Path(__file__).resolve().parent
    for cand in (here / "entry.png", Path("/bot/entry.png"), Path.cwd() / "entry.png"):
        if cand.is_file():
            return cand
    sys.exit("FATAL: entry.png not found (looked next to main.py, in /bot, in cwd)")


def validate_png(path: Path) -> tuple[int, int, int, bytes]:
    """Check PNG magic, IHDR dimensions and file size.

    Return (width, height, byte_count, raw_bytes).
    """
    data = path.read_bytes()
    if not data.startswith(PNG_MAGIC):
        sys.exit(f"FATAL: {path} is not a PNG (bad magic bytes)")
    if len(data) < 33:
        sys.exit(f"FATAL: {path} too small to hold an IHDR chunk")
    (ihdr_len,) = struct.unpack(">I", data[8:12])
    if data[12:16] != b"IHDR" or ihdr_len != 13:
        sys.exit(f"FATAL: {path} first chunk is not IHDR")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        sys.exit(f"FATAL: {width}x{height} exceeds {MAX_DIM}x{MAX_DIM} limit")
    if len(data) > MAX_BYTES:
        sys.exit(f"FATAL: {len(data)} bytes exceeds {MAX_BYTES} byte limit")
    return width, height, len(data), data


def main() -> None:
    src = find_entry()
    width, height, nbytes, data = validate_png(src)

    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    out_dir = Path(raw) if raw else Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"

    # byte-exact copy: write the exact validated bytes
    out.write_bytes(data)
    if out.stat().st_size != nbytes:
        sys.exit(f"FATAL: output size mismatch: {out.stat().st_size} != {nbytes}")
    print(f"OK: entry.png {width}x{height} {nbytes} bytes -> {out}")


if __name__ == "__main__":
    main()
