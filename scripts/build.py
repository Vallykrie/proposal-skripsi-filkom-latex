#!/usr/bin/env python3
from pathlib import Path
import argparse
import subprocess


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
GENERATED_NAMES = {
    "entry.tex",
    "missfont.log",
    "proposal.aux",
    "proposal.bbl",
    "proposal.bcf",
    "proposal.blg",
    "proposal.fdb_latexmk",
    "proposal.fls",
    "proposal.loa",
    "proposal.lof",
    "proposal.log",
    "proposal.lot",
    "proposal.out",
    "proposal.pdf",
    "proposal.run.xml",
    "proposal.synctex.gz",
    "proposal.toc",
    "proposal.xdv",
}


def latexmk_command(mode: str, entry: Path) -> list[str]:
    if mode not in {"preview", "official"}:
        raise ValueError(f"Mode tidak didukung: {mode}")
    return [
        "latexmk",
        "-xelatex",
        "-bibtex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-outdir={BUILD}",
        "-jobname=proposal",
        str(entry),
    ]


def _validated_build(path: Path, expected_root: Path) -> Path:
    if path.is_symlink():
        raise ValueError("Direktori build tidak boleh berupa symlink")
    canonical = path.resolve()
    expected = (expected_root.resolve() / "build").resolve()
    if canonical != expected:
        raise ValueError("Direktori pembersihan harus tepat berada di root/build")
    return canonical


def clean_build_dir(path: Path = BUILD, expected_root: Path = ROOT) -> None:
    path = _validated_build(path, expected_root)
    if path.exists():
        for child in path.iterdir():
            if child.name in GENERATED_NAMES and (child.is_file() or child.is_symlink()):
                child.unlink()
    else:
        path.mkdir(parents=True)


def remove_stale_pdf(path: Path = BUILD / "proposal.pdf", expected_root: Path = ROOT) -> None:
    if path.is_symlink() or path.name != "proposal.pdf":
        raise ValueError("Hanya build/proposal.pdf yang boleh dihapus")
    try:
        build = _validated_build(path.parent, expected_root)
    except ValueError as exc:
        raise ValueError("Hanya build/proposal.pdf yang boleh dihapus") from exc
    path = build / "proposal.pdf"
    path.unlink(missing_ok=True)


def write_entry(mode: str) -> Path:
    BUILD.mkdir(exist_ok=True)
    entry = BUILD / "entry.tex"
    entry.write_text(
        f"\\PassOptionsToClass{{{mode}}}{{filkomproposal}}\n"
        "\\input{proposal.tex}\n",
        encoding="utf-8",
    )
    return entry


def build(mode: str) -> int:
    entry = write_entry(mode)
    remove_stale_pdf()
    command = latexmk_command(mode, entry)
    try:
        return subprocess.run(command, cwd=ROOT, check=False).returncode
    except FileNotFoundError:
        print("latexmk tidak ditemukan. Pasang TeX Live/MacTeX terlebih dahulu.")
        return 127


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("preview", "official", "clean"))
    args = parser.parse_args()
    if args.mode == "clean":
        clean_build_dir()
        return 0
    return build(args.mode)


if __name__ == "__main__":
    raise SystemExit(main())
