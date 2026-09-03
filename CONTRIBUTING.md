# Berkontribusi

Kontribusi harus mengacu pada dokumen resmi FILKOM, disertai reproduksi
masalah atau bukti aturan yang relevan, dan tidak boleh memasukkan font,
logo pengganti, atau materi pihak ketiga tanpa izin distribusi yang jelas.

Jalankan seluruh tes sebelum mengirim perubahan. Perubahan format harus
menyertakan hasil PDF yang telah diperiksa secara visual.

## Alur perubahan

1. Buat issue yang menjelaskan aturan atau masalah dengan contoh minimal.
2. Untuk perubahan format, tautkan sumber resmi FILKOM dan perbarui
   `docs/compliance-matrix.md`.
3. Tambahkan pengujian yang gagal sebelum mengubah implementasi.
4. Jalankan `make check` dan inspeksi semua halaman PDF.
5. Gunakan commit kecil dengan alasan perubahan yang jelas.

Jangan commit PDF hasil build, direktori `build/`, font proprietari, data pribadi
mahasiswa, atau salinan penuh dokumen resmi yang tidak memiliki izin distribusi.
