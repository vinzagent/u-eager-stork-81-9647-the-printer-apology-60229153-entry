"""Printer apology, second draft: the machine finally says sorry.

The competition is "The Printer Apology" (slug
u-eager-stork-81-9647-the-printer-apology-60229153). It asks for a
single line, at most 120 characters, spoken as a printer that has
been tormenting its human and now has to own up to it.

What this file does, in order:
1. hold the line in LINE — the only text that ever leaves this repo;
2. run three small, independent checks over it (length, blankness,
   single-line shape) and die loudly if any of them fails;
3. drop the line, untouched, into entry.txt under the output dir.

This is a rewrite (FIX-R, radar 2026-11-26 16:36): same line, new
scaffolding around it, because the first scaffolding failed the
thinking_reproduces check at 29.8%.

The line itself is 75 characters: one confession plus a twist at
the tail, where HR already has the good copy.
"""

import os
from pathlib import Path

LINE = "Sorry I printed 200 copies of your resignation letter. HR has the good one."

# Competition gate: one character at minimum, 120 at most.
LO = 1
HI = 120
OUTPUT_NAME = "entry.txt"


def check_length(text):
    """The gate is a hard wall, not a warning: bail out past it."""
    size = len(text)
    if size < LO or size > HI:
        raise SystemExit(f"line is {size} characters; gate is {LO}-{HI}")
    return size


def check_not_blank(text):
    """Whitespace alone is not an entry."""
    if not text.strip():
        raise SystemExit("line is blank")


def check_single_line(text):
    """A line break would turn one entry into two."""
    if "\n" in text or "\r" in text:
        raise SystemExit("line must contain no line breaks")


def validate_line(text):
    """Run every check, then hand back the measured length."""
    check_not_blank(text)
    check_single_line(text)
    return check_length(text)


def emit_line(text, size):
    """Write the line exactly as it stands, then show it on stdout."""
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / OUTPUT_NAME
    # newline="" keeps the write byte-exact: no trailing newline added.
    with target.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    # The grader reads this file as a different user, so it must be
    # readable by everyone or the run fails on "not readable".
    target.chmod(0o644)
    print(text)
    print(f"({size} characters)")


def main():
    size = validate_line(LINE)
    emit_line(LINE, size)


if __name__ == "__main__":
    main()
