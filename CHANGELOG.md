# Changelog

## [Unreleased]

- Menyesuaikan jarak paragraf 6 pt, jarak judul dengan style Word, judul level empat miring, serta posisi awal persamaan setelah sepuluh spasi sesuai Panduan v3.0.
- Menyesuaikan artikel jurnal ke pola judul tanpa tanda petik, nama jurnal tanpa awalan "Dalam:", dan volume(nomor).

- Mengubah judul bagian awal (Daftar Isi, Daftar Tabel, Daftar Gambar) menjadi huruf kapital dan memastikan masuk dalam daftar isi.
- Memperbaiki ukuran teks pada sampul selain judul menjadi 14 pt untuk menyesuaikan panduan resmi.
- Memperbaiki ketebalan judul tabel dan gambar agar ditebalkan secara keseluruhan, tidak hanya pada nomornya.
- Melokalisasikan kata-kata struktural bibliografi ke bahasa Indonesia (seperti "dan", "Dalam:", "Tersedia di:", "Diakses", dan "Penyunting") dengan menyertakan `indonesian.lbx`.
- Memperbaiki delimiter penulis menjadi `dan` ber-koma untuk referensi lebih dari dua penulis.
- Memperbaiki masalah overfull hbox pada URL bibliografi panjang dengan menggunakan paket `xurl`.
- Menyesuaikan validator PDF untuk mengurangi *false positive* saat rujukan gambar atau tabel muncul di dalam teks narasi.

## 0.1.0 - 2026-09-02

- Memulai implementasi clean-room template proposal skripsi FILKOM UB.
- Menambahkan class proposal, struktur tiga bab, bibliografi author–year, dan
  logo UB siap pakai.
- Menambahkan mode preview/official, build lintas platform, CI, pemeriksa log,
  pemeriksa PDF, dokumentasi kompatibilitas, serta matriks kepatuhan.
- Menyelaraskan label lampiran, ukuran judul sampul/logo, indentasi paragraf,
  dan tanda baca sitasi dengan hasil audit dokumen acuan.
- Memperketat validasi font, struktur halaman, gaya referensi, tautan dokumentasi,
  serta pembersihan artefak build agar tidak menghapus berkas pengguna.
