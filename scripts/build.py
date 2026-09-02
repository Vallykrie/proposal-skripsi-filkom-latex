#!/usr/bin/env python3
from pathlib import Path
import argparse
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"


def latexmk_command(mode: str, entry: Path) -> list[str]:
    if mode not in {"preview", "official"}:
        raise ValueError(f"Mode tidak didukung: {mode}")
    return [
        "latexmk",
        "-xelatex",
        "-use-biber",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-outdir={BUILD}",
        "-jobname=proposal",
        str(entry),
    ]


def clean_build_dir(path: Path = BUILD) -> None:
    path = path.resolve()
    if path.name != "build":
        raise ValueError("Direktori pembersihan harus bernama build")
    if path.exists():
        for child in path.iterdir():
            if child.is_dir() and not child.is_symlink():
                shutil.rmtree(child)
            else:
                child.unlink()
    else:
        path.mkdir(parents=True)


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
