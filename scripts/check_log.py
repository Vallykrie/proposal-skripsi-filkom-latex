#!/usr/bin/env python3
from pathlib import Path
import re
import sys


def log_problems(text: str, overfull_limit: float = 2.0) -> list[str]:
    problems: list[str] = []
    lowered = text.lower()
    if "citation" in lowered and "undefined" in lowered:
        problems.append("sitasi tidak terdefinisi")
    if "reference" in lowered and "undefined" in lowered:
        problems.append("referensi silang tidak terdefinisi")
    if "! latex error" in lowered or "emergency stop" in lowered:
        problems.append("error fatal LaTeX")
    if (
        "language 'bahasa' not supported" in lowered
        or "'csquotes' missing" in lowered
        or "no style for language 'indonesian'" in lowered
        or "using fallback definition for \\mkbib" in lowered
        or "bibliography string" in lowered and "untranslated" in lowered
    ):
        problems.append("konfigurasi bahasa bibliografi tidak lengkap")
    widths = [float(value) for value in re.findall(r"Overfull \\hbox \(([0-9.]+)pt too wide\)", text)]
    if any(width > overfull_limit for width in widths):
        problems.append(f"overfull box melebihi {overfull_limit:.1f} pt")
    return problems


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "build/proposal.log")
    problems = log_problems(path.read_text(encoding="utf-8", errors="replace"))
    for problem in problems:
        print(f"ERROR: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
