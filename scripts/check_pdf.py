#!/usr/bin/env python3
"""Validate the generated proposal PDF using Poppler command-line tools."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_TEXT = (
    "PROPOSAL SKRIPSI",
    "DAFTAR ISI",
    "BAB I PENDAHULUAN",
    "BAB II LANDASAN KEPUSTAKAAN",
    "BAB III METODOLOGI",
    "JADWAL PENELITIAN",
    "DAFTAR REFERENSI",
)


def parse_pdfinfo(output: str) -> dict[str, float | int]:
    pages_match = re.search(r"^Pages:\s+(\d+)", output, re.MULTILINE)
    size_match = re.search(
        r"^Page size:\s+([0-9.]+)\s+x\s+([0-9.]+)\s+pts", output, re.MULTILINE
    )
    if not size_match:
        raise ValueError("Page size is missing from pdfinfo output")
    return {
        "pages": int(pages_match.group(1)) if pages_match else 0,
        "width_pt": float(size_match.group(1)),
        "height_pt": float(size_match.group(2)),
    }


def parse_pdffonts(output: str) -> set[str]:
    fonts: set[str] = set()
    for line in output.splitlines():
        if (
            not line.strip()
            or line.startswith("name")
            or not line.replace("-", "").strip()
        ):
            continue
        name = line.split()[0]
        fonts.add(re.sub(r"^[A-Z]{6}\+", "", name))
    return fonts


def _normalized_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.upper()).strip()


def validate_required_text(text: str) -> list[str]:
    normalized = _normalized_text(text)
    return [f"Teks wajib tidak ditemukan: {heading}" for heading in REQUIRED_TEXT if heading not in normalized]


def validate_fonts(fonts: set[str], mode: str) -> list[str]:
    if mode not in {"preview", "official"}:
        raise ValueError(f"Mode tidak dikenal: {mode}")
    required = "Carlito" if mode == "preview" else "Calibri"
    if any(font.casefold().startswith(required.casefold()) for font in fonts):
        return []
    return [f"Mode {mode} wajib menggunakan {required}; font terdeteksi: {', '.join(sorted(fonts))}"]


def validate_page(info: dict[str, float | int], tolerance_pt: float = 1.0) -> list[str]:
    errors: list[str] = []
    if int(info["pages"]) < 1:
        errors.append("PDF tidak memiliki halaman")
    if abs(float(info["width_pt"]) - 595.28) > tolerance_pt or abs(
        float(info["height_pt"]) - 841.89
    ) > tolerance_pt:
        errors.append(
            "Ukuran halaman bukan A4: "
            f"{info['width_pt']} x {info['height_pt']} pt"
        )
    return errors


def run_tool(command: list[str]) -> str:
    try:
        completed = subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Perintah tidak tersedia: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip()
        raise RuntimeError(f"{' '.join(command)} gagal: {detail}") from exc
    return completed.stdout


def check_pdf(pdf: Path, mode: str) -> list[str]:
    if not pdf.is_file():
        return [f"PDF tidak ditemukan: {pdf}"]
    try:
        info = parse_pdfinfo(run_tool(["pdfinfo", str(pdf)]))
        text = run_tool(["pdftotext", "-layout", str(pdf), "-"])
        fonts = parse_pdffonts(run_tool(["pdffonts", str(pdf)]))
    except (RuntimeError, ValueError) as exc:
        return [str(exc)]
    return validate_page(info) + validate_required_text(text) + validate_fonts(fonts, mode)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--mode", choices=("preview", "official"), default="preview")
    args = parser.parse_args()
    errors = check_pdf(args.pdf, args.mode)
    if errors:
        print("Pemeriksaan PDF gagal:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"PDF valid untuk mode {args.mode}: {args.pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
