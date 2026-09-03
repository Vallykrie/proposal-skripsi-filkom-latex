# Template Proposal Skripsi FILKOM UB (LaTeX)

Template LaTeX publik dan **tidak resmi** untuk proposal skripsi Fakultas Ilmu
Komputer Universitas Brawijaya (FILKOM UB). Paket ini memisahkan format dari isi:
pengguna normal cukup mengganti identitas, tiga bab, dan referensi. Logo UB siap
pakai sudah disertakan.

> Proyek ini tidak diterbitkan, disahkan, atau didukung oleh FILKOM UB. Panduan
> resmi FILKOM, ketentuan program studi, dan arahan dosen pembimbing selalu
> mengungguli template ini.

## Fitur

- Struktur khusus proposal: sampul, daftar awal, tiga bab, Jadwal Penelitian,
  Daftar Referensi, dan lampiran.
- A4; margin kiri 4 cm dan sisi lain 3 cm; satu spasi; nomor halaman di tengah.
- Metadata terpusat di `metadata.tex` dan logo UB berwarna siap pakai.
- Sitasi `biblatex` author–year dengan Biber serta contoh delapan tipe sumber.
- Mode `preview` memakai Calibri atau fallback bebas Carlito.
- Mode `official` mewajibkan Calibri dan berhenti jika syarat tidak terpenuhi.
- Build lintas platform, pengujian kontrak, audit log, dan pemeriksaan PDF.

## Mulai dalam 5 menit

Prasyarat utama adalah TeX Live/MacTeX atau MiKTeX yang menyediakan XeLaTeX,
`latexmk`, dan Biber. Untuk preview tanpa Calibri, pasang font Carlito.

1. Unduh/clone repositori dan buka direktori proyek.
2. Isi semua nilai contoh di `metadata.tex`.
3. Tulis isi pada `chapters/` dan ubah `bibliography/references.bib`.
4. Jalankan:

   ```sh
   make preview
   ```

5. Buka `build/proposal.pdf`. Sebelum dikumpulkan, pasang Calibri secara legal
   dari sumber yang berhak Anda gunakan, lalu jalankan:

   ```sh
   make official
   ```

Jangan masukkan berkas font Calibri ke Git. Carlito hanya untuk penyuntingan dan
CI; ia bukan pengganti persyaratan font pada keluaran resmi.

## Perintah

```sh
make preview   # XeLaTeX + Biber; Calibri atau fallback Carlito
make official  # XeLaTeX + Biber; Calibri wajib
make test      # semua unit/contract test
make check     # test, build preview, audit log, dan audit PDF
make clean     # hanya menghapus direktori build
```

Alternatif preview dengan Tectonic tersedia melalui `tectonic-preview.tex` dan
memakai BibTeX karena distribusi Tectonic tertentu membundel versi `biblatex`
yang tidak cocok dengan Biber sistem:

```sh
tectonic -X compile tectonic-preview.tex --outdir build/tectonic
```

## Struktur yang perlu diedit

```text
metadata.tex                         identitas dan pilihan logo
chapters/bab1-pendahuluan.tex        Bab 1
chapters/bab2-landasan-kepustakaan.tex
chapters/bab3-metodologi.tex         termasuk Jadwal Penelitian
bibliography/references.bib          basis data referensi
frontmatter/daftar-istilah.tex       opsional
appendices/lampiran-contoh.tex       lampiran
```

Hindari mengubah `filkomproposal.cls` untuk satu dokumen. Jika ada aturan format
baru, ajukan perubahan class beserta sumber resmi dan hasil pengujiannya.

## macOS, Linux, Windows, dan Overleaf

- **macOS:** MacTeX terbaru; Carlito dapat dipasang melalui Homebrew Fonts.
- **Linux:** TeX Live 2024+ serta paket XeLaTeX, Biber, `biblatex-ext`, dan
  Carlito dari repositori distribusi.
- **Windows:** TeX Live 2024+ atau MiKTeX terkini. Jalankan `python
  scripts/build.py preview` jika GNU Make tidak tersedia.
- **Overleaf:** unggah seluruh isi repo, pilih compiler XeLaTeX, lalu gunakan
  mode `preview`. Mode `official` hanya dapat dipakai jika proyek memiliki akses
  legal ke Calibri; Overleaf umumnya tidak menyediakannya.

Rincian paket dan batas dukungan ada di [panduan kompatibilitas](docs/compatibility.md).

## Acuan dan tingkat kepatuhan

Implementasi disusun secara clean-room dari Panduan Skripsi FILKOM versi 3.0 dan
template proposal Word resmi yang diaudit saat pengembangan. Halaman layanan
akademik FILKOM masih menautkan Buku Panduan Skripsi v3 pada 2 September 2026.
Lihat [matriks kepatuhan](docs/compliance-matrix.md) untuk pemetaan aturan ke
kode dan pengujian. Ini adalah dokumentasi audit, bukan pengesahan resmi.

## Bantuan

Masalah font, logo, Biber, referensi, atau Overleaf dibahas di
[troubleshooting](docs/troubleshooting.md). Format entri referensi dijelaskan di
[panduan bibliografi](docs/bibliography.md).

## Lisensi dan merek

Kode serta dokumentasi dirilis dengan **LPPL 1.3c atau lebih baru**. Logo UB
tidak tercakup LPPL dan tetap merupakan aset/merek milik pemegang haknya; lihat
`assets/NOTICE.md`. Calibri tidak didistribusikan oleh proyek ini.

## Status rilis

Versi awal adalah `0.1.0`. Perubahan terdokumentasi di `CHANGELOG.md`, aturan
kontribusi di `CONTRIBUTING.md`, dan metadata sitasi perangkat lunak di
`CITATION.cff`.
