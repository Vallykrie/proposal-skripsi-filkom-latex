import argparse
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


REQUIRED_TEXT = (
    "PROPOSAL SKRIPSI",
    "BAB 1 PENDAHULUAN",
    "BAB 2 LANDASAN KEPUSTAKAAN",
    "BAB 3 METODOLOGI PENELITIAN",
    "DAFTAR REFERENSI",
    "LAMPIRAN A INSTRUMEN ATAU RINCIAN PENDUKUNG",
)
FORBIDDEN_TEXT = (
    "ABSTRAK",
    "KATA PENGANTAR",
    "BAB 4 HASIL DAN PEMBAHASAN",
    "BAB 5 KESIMPULAN",
)


def _normalized_text(text: str) -> str:
    return " ".join(text.upper().split())


def _collapsed_text(text: str) -> str:
    return " ".join(text.split())


def parse_pdfinfo(output: str) -> dict[str, float | int]:
    info: dict[str, float | int] = {}
    for line in output.splitlines():
        if line.startswith("Pages:"):
            info["pages"] = int(line.split(":", 1)[1].strip())
        elif line.startswith("Page size:"):
            match = re.search(r"([\d.]+)\s*x\s*([\d.]+)", line)
            if not match:
                raise ValueError(f"Page size tidak dikenali: {line}")
            info["width_pt"] = float(match.group(1))
            info["height_pt"] = float(match.group(2))
    if "width_pt" not in info:
        raise ValueError("Page size tidak ditemukan dalam output pdfinfo")
    return info


def parse_pdffonts(output: str) -> set[str]:
    lines = output.splitlines()
    if len(lines) < 2:
        return set()
    fonts: set[str] = set()
    for line in lines[2:]:
        parts = line.split()
        if not parts:
            continue
        name = parts[0]
        if "+" in name:
            name = name.split("+", 1)[1]
        fonts.add(name)
    return fonts


def validate_required_text(text: str) -> list[str]:
    normalized = _normalized_text(text)
    errors = [
        f"Teks wajib tidak ditemukan: {heading}"
        for heading in REQUIRED_TEXT
        if heading not in normalized
    ]
    errors.extend(
        f"Bagian skripsi yang tidak semestinya ditemukan: {heading}"
        for heading in FORBIDDEN_TEXT
        if heading in normalized
    )
    if "BAB A" in normalized:
        errors.append("Lampiran tidak boleh memakai heading BAB A")
    return errors


def validate_document_structure(text: str) -> list[str]:
    raw_pages = [_collapsed_text(page) for page in text.split("\f") if page.strip()]
    pages = [page.upper() for page in raw_pages]
    headings = (
        "BAB 1 PENDAHULUAN",
        "BAB 2 LANDASAN KEPUSTAKAAN",
        "BAB 3 METODOLOGI PENELITIAN",
        "DAFTAR REFERENSI",
        "LAMPIRAN A INSTRUMEN ATAU RINCIAN PENDUKUNG",
    )
    positions: list[int] = []
    errors: list[str] = []
    frontmatter = (
        "DAFTAR ISI",
        "DAFTAR TABEL",
        "DAFTAR GAMBAR",
        "DAFTAR LAMPIRAN",
        "DAFTAR ISTILAH, SIMBOL, DAN SINGKATAN",
    )
    for heading in frontmatter:
        if not any(page.startswith(heading) for page in raw_pages):
            errors.append(f"Judul bagian awal harus kapital: {heading}")
    toc_pages = [page for page in raw_pages if page.startswith("DAFTAR ISI")]
    if toc_pages:
        toc = toc_pages[0]
        for entry in ("DAFTAR ISI", "DAFTAR TABEL", "DAFTAR GAMBAR"):
            if entry not in toc:
                errors.append(f"Entri tidak ditemukan dalam Daftar Isi: {entry}")
    for heading in headings:
        matches = [index for index, page in enumerate(pages) if page.startswith(heading)]
        if not matches:
            errors.append(f"Heading tidak ditemukan pada awal halaman: {heading}")
        else:
            positions.append(matches[0])
    if len(positions) == len(headings) and positions != sorted(positions):
        errors.append("Urutan bab, referensi, dan lampiran tidak benar")
    return errors


def validate_typography_xml(xml_text: str) -> list[str]:
    """Validate cover and caption typography from pdftohtml XML."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        return [f"XML tipografi PDF tidak valid: {exc}"]
    fonts = {
        element.attrib["id"]: float(element.attrib["size"])
        for element in root.iter("fontspec")
        if "id" in element.attrib and "size" in element.attrib
    }
    pages = list(root.iter("page"))
    if not pages:
        return ["XML PDF tidak memiliki halaman"]

    errors: list[str] = []
    cover_text = [element for element in pages[0].iter("text") if "font" in element.attrib]
    cover_sizes = [fonts.get(element.attrib["font"]) for element in cover_text]
    cover_sizes = [size for size in cover_sizes if size is not None]
    if not cover_sizes:
        errors.append("Ukuran teks sampul tidak dapat dibaca")
    else:
        title_size = max(cover_sizes)
        secondary_size = title_size * 14 / 16
        invalid = [
            size
            for size in cover_sizes
            if abs(size - title_size) > 0.25 and abs(size - secondary_size) > 0.25
        ]
        if invalid:
            errors.append("Teks identitas dan institusi pada sampul harus 14 pt")

    captions_found: set[str] = set()
    for page in pages[1:]:
        lines: dict[str, list[ET.Element]] = {}
        for element in page.iter("text"):
            lines.setdefault(element.attrib.get("top", ""), []).append(element)
        for elements in lines.values():
            line = " ".join(_collapsed_text("".join(e.itertext())) for e in elements)
            match = re.search(r"^(Tabel|Gambar)\s+\d+\.\d+\b", line)
            if not match:
                continue
            captions_found.add(match.group(1))
            if not all(_is_fully_bold(element) for element in elements):
                errors.append(f"Seluruh caption {match.group(1)} harus tebal")
    for kind in ("Tabel", "Gambar"):
        if kind not in captions_found:
            errors.append(f"Caption {kind} tidak ditemukan dalam XML PDF")
    return errors


def _is_fully_bold(element: ET.Element) -> bool:
    if (element.text or "").strip():
        return False
    children = list(element)
    return bool(children) and all(
        child.tag.rsplit("}", 1)[-1] == "b" and not (child.tail or "").strip()
        for child in children
    )


def validate_reference_style(text: str) -> list[str]:
    normalized = _normalized_text(text)
    references = normalized.rsplit("DAFTAR REFERENSI", 1)[-1]
    errors: list[str] = []
    if "(LAMPORT, 1994)" not in normalized:
        errors.append("Sitasi author–year harus memakai koma: (Lamport, 1994)")
    if not re.search(r"KNUTH,\s*D\.E\.,\s*1984", normalized):
        errors.append("Daftar referensi harus memakai pola Nama, Inisial., Tahun")
    if not re.search(r"FIELDING,\s*R\.T\.,\s*NOTTINGHAM,\s*M\.,\s*DAN\s*RESCHKE", normalized):
        errors.append("Sitasi/referensi tiga penulis harus menampilkan semua nama")
    forbidden = {
        r",\s+AND\s+[A-Z]": "and",
        r"\bIN:": "In:",
        r"\bED\.\s+BY\b": "Ed. by",
        r"\bVISITED\s+ON\b": "visited on",
        r"\bURL:": "URL:",
    }
    for pattern, token in forbidden.items():
        if re.search(pattern, references):
            errors.append(f"Kata struktural bibliografi belum dilokalkan: {token}")
    for required in ("DALAM:", "TERSEDIA DI:", "DIAKSES"):
        if required not in references:
            errors.append(f"Kata struktural bibliografi tidak ditemukan: {required}")
    return errors


def validate_fonts(fonts: set[str], mode: str) -> list[str]:
    if mode not in {"preview", "official"}:
        raise ValueError(f"Mode tidak dikenal: {mode}")
    lowered = {font.casefold() for font in fonts}
    if mode == "preview":
        if any(font.startswith(("carlito", "calibri")) for font in lowered):
            return []
        required = "Calibri atau Carlito"
    else:
        required_faces = {"calibri", "calibri-bold", "calibri-italic"}
        missing = sorted(required_faces - lowered)
        has_fallback = any(font.startswith("carlito") for font in lowered)
        if not missing and not has_fallback:
            return []
        required = "Calibri regular, bold, dan italic tanpa Carlito"
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
        typography_xml = run_tool(["pdftohtml", "-xml", "-stdout", str(pdf)])
    except (RuntimeError, ValueError) as exc:
        return [str(exc)]
    return (
        validate_page(info)
        + validate_required_text(text)
        + validate_document_structure(text)
        + validate_typography_xml(typography_xml)
        + validate_reference_style(text)
        + validate_fonts(fonts, mode)
    )


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
