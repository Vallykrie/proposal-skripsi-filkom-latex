# Sitasi dan Daftar Referensi

Template menggunakan `biblatex` dan Biber dengan gaya
`filkom-authoryear`. Gunakan `\textcite{kunci}` untuk sitasi naratif dan
`\parencite{kunci}` untuk sitasi dalam kurung.

Gaya menguji pola dasar yang tampak pada panduan: `(Nama, Tahun)`, daftar
referensi `Nama, Inisial., Tahun`, dan seluruh nama untuk sumber dengan sampai
tiga penulis. Fixture juga membangun artikel jurnal, buku, bab buku, prosiding,
tesis, sumber daring, laporan, dan perangkat lunak.

Simpan DOI sebagai pengenal saja, misalnya `10.1093/comjnl/27.2.97`, bukan
sebagai URL. Sumber daring perlu memiliki `url` dan `urldate`.

Implementasi ini merupakan adaptasi awal, bukan replika normatif lengkap dari
Harvard Anglia. Detail yang tidak dicontohkan panduan—misalnya standar,
dataset, edisi terjemahan, atau sumber tanpa penulis—tetap perlu diperiksa
manual. Apabila tampilannya berbeda dari contoh resmi FILKOM, laporkan contoh
bibliografinya agar gaya dapat diuji dan diperbaiki.
