# Troubleshooting

## `Calibri wajib untuk mode official`

Mode official memang menolak fallback. Pasang Calibri dari sumber legal yang
Anda miliki, pastikan aplikasi lain dapat melihat regular/bold/italic/bold-italic,
lalu mulai ulang terminal atau editor. Jangan mengunduh atau memasukkan font ke
repo dari sumber tidak resmi. Untuk menyunting sementara, gunakan mode preview
dengan Carlito.

## `Calibri dan Carlito tidak ditemukan`

Pasang Carlito melalui pengelola paket sistem atau paket font TeX Live, lalu
jalankan ulang `make preview`. Periksa nama font dengan `fc-match Carlito` pada
Linux/macOS yang menyediakan Fontconfig.

## Logo tidak ditemukan

Nilai bawaan `logo={assets/logo-ub.png}` sudah siap. Pastikan seluruh repo
diunduh, bukan hanya berkas `.tex`. Jika mengganti logo, gunakan PNG/PDF yang
dapat dibaca XeLaTeX dan perbarui kunci `logo` di `metadata.tex`.

## Biber gagal atau referensi tidak muncul

Pastikan Biber dan paket `biblatex-ext` terpasang serta versinya cocok dengan
TeX Live/MiKTeX. Bersihkan artefak lalu build ulang:

```sh
make clean
make preview
```

Jangan menjalankan hanya satu kali `xelatex`; `latexmk` mengatur siklus
XeLaTeX–Biber–XeLaTeX yang diperlukan. Periksa juga nama kunci sitasi dan sintaks
`bibliography/references.bib`.

## Referensi atau nomor bagian bertanda `??`

Jalankan build penuh lagi dan baca `build/proposal.log`. `make check` akan gagal
jika sitasi atau referensi silang masih tidak terdefinisi.

## Overleaf memakai font/layout yang berbeda

Pilih compiler XeLaTeX pada pengaturan proyek dan gunakan mode preview. Jangan
memilih pdfLaTeX. Cocokkan versi TeX Live Overleaf dengan versi yang didukung di
`docs/compatibility.md`.

## `Style 'filkom-authoryear' not found`

Pastikan direktori `bibliography/` beserta berkas `.bbx` dan `.cbx` ikut
diunggah. Jangan memindahkan style tanpa memperbarui `\input@path` di
`proposal.tex`.

## PDF terbentuk tetapi pemeriksaan gagal

Jalankan dua pemeriksa secara terpisah untuk pesan yang lebih jelas:

```sh
python scripts/check_log.py build/proposal.log
python scripts/check_pdf.py build/proposal.pdf --mode preview
```

Laporkan masalah dengan versi OS, distribusi TeX, perintah, dan bagian log yang
relevan; jangan menyertakan data pribadi atau seluruh proposal tanpa kebutuhan.
