# Kompatibilitas

Mesin utama template adalah **XeLaTeX** dengan **Biber**. Versi minimum yang
ditargetkan adalah TeX Live 2024 atau MiKTeX terkini. Jalur berikut merupakan
target dukungan; kombinasi paket yang lebih lama dapat bekerja tetapi tidak diuji.

| Lingkungan | Jalur yang disarankan | Mode | Catatan |
|---|---|---|---|
| macOS | MacTeX + `latexmk` + Biber | preview/official | Pasang Carlito untuk preview; Calibri legal untuk official. |
| Linux | TeX Live 2024+ | preview/official | Paket umum: XeLaTeX, Biber, `biblatex-ext`, Carlito, Poppler. |
| Windows | TeX Live 2024+ atau MiKTeX | preview/official | MiKTeX dapat meminta instalasi paket saat build pertama. |
| Overleaf | compiler XeLaTeX | preview | Carlito tersedia melalui distribusi TeX; Calibri biasanya tidak tersedia. |
| Tectonic 0.17+ | `tectonic-preview.tex` | preview | Memakai BibTeX khusus jalur alternatif ini. |

## Perintah tanpa GNU Make

Semua platform yang memiliki Python 3 dapat menjalankan:

```text
python scripts/build.py preview
python scripts/build.py official
python -m unittest discover -s tests -v
```

Di Windows PowerShell, gunakan `python` atau `py -3` sesuai instalasi. Perintah
yang dibentuk skrip tetap memanggil `latexmk`, XeLaTeX, dan Biber.

## Paket CI

Workflow GitHub Actions memasang `texlive-xetex`, `texlive-latex-extra`,
`texlive-bibtex-extra`, `biber`, `latexmk`, `fonts-crosextra-carlito`, dan
`poppler-utils`. Daftar ini juga menjadi referensi paket Debian/Ubuntu.

## Batas kompatibilitas

- pdfLaTeX tidak didukung karena tidak dapat memakai font OpenType sistem dengan
  kontrak yang sama.
- LuaLaTeX belum menjadi target uji.
- Keluaran `official` tidak dapat dibuat tanpa Calibri; font tersebut tidak
  dibundel karena lisensinya.
- Ketersediaan paket Overleaf dapat berubah. Jika build cloud berbeda dari lokal,
  cocokkan versi TeX Live proyek terlebih dahulu.
