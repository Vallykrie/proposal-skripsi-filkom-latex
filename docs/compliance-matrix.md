# Matriks Kepatuhan Format

Matriks ini memetakan aturan yang ditemukan pada **Panduan Skripsi FILKOM versi 3.0**
dan template proposal Word resmi ke implementasi. Sumber publik utama:
[Layanan Akademik FILKOM UB](https://filkom.ub.ac.id/pendidikan/layanan-akademik-filkom-ub/),
yang menautkan Buku Panduan Skripsi v3 (diakses 2 September 2026).

Status **terimplementasi** berarti aturan terdapat dalam class/contoh dan diuji;
bukan berarti FILKOM telah mengesahkan proyek ini.

| Aturan | Implementasi | Bukti otomatis | Status |
|---|---|---|---|
| Kertas A4 | opsi `a4paper` | `scripts/check_pdf.py` membaca dimensi PDF | Terimplementasi |
| Margin kiri 4 cm; atas, kanan, bawah 3 cm | `geometry` pada class | `test_class_contract_has_modes_fonts_and_geometry` | Terimplementasi |
| Teks utama 12 pt, satu spasi | class `12pt`, `\setstretch{1}` | audit sumber dan PDF | Terimplementasi |
| Font Calibri | mode `official` menolak font lain | pemeriksaan font PDF dan uji kegagalan prasyarat | Terimplementasi |
| Judul bab 16 pt tebal rata tengah | `titlesec` | audit sumber dan inspeksi visual | Terimplementasi |
| Subbab 14/14/12 pt tebal | `titlesec` per tingkat | audit sumber | Terimplementasi |
| Nomor halaman tengah bawah | `fancyhdr` | inspeksi visual seluruh halaman | Terimplementasi |
| Sampul bertuliskan `PROPOSAL SKRIPSI` | `\makeproposalcover` | contract test dan ekstraksi teks PDF | Terimplementasi |
| Sampul proposal tanpa kalimat syarat gelar | class khusus proposal | contract test atas elemen laporan akhir | Terimplementasi |
| Daftar Isi, Tabel, Gambar, dan Lampiran | `\makeproposalfrontmatter` | ekstraksi teks dan inspeksi PDF | Terimplementasi |
| Bab 1 Pendahuluan | contoh bab terpisah | contract test dan ekstraksi teks PDF | Terimplementasi |
| Bab 2 Landasan Kepustakaan | contoh bab terpisah | contract test dan ekstraksi teks PDF | Terimplementasi |
| Bab 3 Metodologi Penelitian | contoh bab terpisah | contract test dan ekstraksi teks PDF | Terimplementasi |
| Jadwal Penelitian pada Bab 3 | subbab dan tabel contoh | contract test dan ekstraksi teks PDF | Terimplementasi |
| Bagian bernama Daftar Referensi | judul `DAFTAR REFERENSI` | contract test dan ekstraksi teks PDF | Terimplementasi |
| Sitasi author–year/Harvard-Anglia | style `filkom-authoryear` | fixture delapan tipe sumber dan build PDF | Adaptasi terdokumentasi |
| Lampiran setelah referensi | `\appendix` dan helper lampiran | daftar lampiran serta inspeksi PDF | Terimplementasi |

## Hal yang tetap harus diperiksa pengguna

- Arahan terbaru dosen pembimbing, program studi, atau FILKOM.
- Substansi dan urutan subbagian yang bergantung pada metode penelitian.
- Konsistensi data mahasiswa dan nama unit organisasi.
- Hasil akhir mode `official` benar-benar menanam Calibri.
- Kesesuaian referensi kasus khusus dengan contoh pada panduan resmi.
