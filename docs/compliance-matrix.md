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
| Indentasi paragraf sekitar 0,6 cm | `\parindent` 0,6 cm | contract test | Terimplementasi |
| Judul bab 16 pt tebal rata tengah | `titlesec` | audit sumber dan inspeksi visual | Terimplementasi |
| Subbab 14/14/12 pt tebal | `titlesec` per tingkat | audit sumber | Terimplementasi |
| Nomor halaman tengah bawah | `fancyhdr` | inspeksi visual seluruh halaman | Terimplementasi |
| Sampul: judul 16 pt dan logo sekitar 5 cm | `\makeproposalcover` | contract test dan inspeksi visual | Terimplementasi |
| Sampul: identitas dan institusi 14 pt | `\makeproposalcover` | pemeriksaan font di xml tipografi pdf | Terimplementasi |
| Sampul bertuliskan `PROPOSAL SKRIPSI` | `\makeproposalcover` | contract test dan ekstraksi teks PDF | Terimplementasi |
| Sampul proposal tanpa kalimat syarat gelar | class khusus proposal | contract test atas elemen laporan akhir | Terimplementasi |
| Daftar Isi, Tabel, Gambar berhuruf kapital | `\renewcommand` di `\makeproposalfrontmatter` | ekstraksi teks dan inspeksi PDF | Terimplementasi |
| Seluruh text caption tabel dan gambar tebal | `\captionsetup` | ekstraksi font tag bold xml tipografi | Terimplementasi |
| Bab 1 Pendahuluan | contoh bab terpisah | contract test dan ekstraksi teks PDF | Terimplementasi |
| Bab 2 Landasan Kepustakaan | contoh bab terpisah | contract test dan ekstraksi teks PDF | Terimplementasi |
| Bab 3 Metodologi Penelitian | contoh bab terpisah | contract test dan ekstraksi teks PDF | Terimplementasi |
| Jadwal Penelitian pada Bab 3 | subbab dan tabel contoh | contract test dan ekstraksi teks PDF | Terimplementasi |
| Bagian bernama Daftar Referensi | judul `DAFTAR REFERENSI` | contract test dan ekstraksi teks PDF | Terimplementasi |
| Sitasi author–year/Harvard-Anglia terjemahan Indonesia | style `filkom-authoryear` dengan terjemahan lbx | pemeriksaan pelokalan referensi, koma tiga penulis | Terimplementasi; kasus tepi referensi tertentu belum teruji penuh |
| Lampiran setelah referensi, berlabel `LAMPIRAN A` | `\appendix` dan helper lampiran | urutan heading per halaman dan larangan `BAB A` | Terimplementasi |

## Hal yang tetap harus diperiksa pengguna

Audit lanjutan 10 September 2026 menyelaraskan jarak paragraf 6 pt, jarak setelah judul bab 18 pt, jarak subbab menurut style Word, judul tingkat empat tebal-miring, dan persamaan rata kiri setelah sepuluh spasi. Ukuran judul tingkat tiga tetap 14 pt mengikuti ketentuan eksplisit Panduan bagian 3.6.1.3, meskipun style Word memuat 13 pt. Format artikel jurnal mengikuti pola bagian 3.6.6: judul tanpa tanda petik, nama jurnal diikuti volume(nomor), tanpa awalan "Dalam:".

- Arahan terbaru dosen pembimbing, program studi, atau FILKOM.
- Substansi dan urutan subbagian yang bergantung pada metode penelitian.
- Konsistensi data mahasiswa dan nama unit organisasi.
- Hasil akhir mode `official` benar-benar menanam Calibri.
- Kesesuaian referensi kasus khusus dengan contoh pada panduan resmi.
