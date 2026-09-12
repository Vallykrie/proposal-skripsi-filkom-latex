import unittest

from scripts import check_pdf

from scripts.check_pdf import (
    parse_pdffonts,
    parse_pdfinfo,
    validate_document_structure,
    validate_fonts,
    validate_required_text,
    validate_reference_style,
)


class PdfCheckerTests(unittest.TestCase):
    def test_parse_pdfinfo_reads_a4_dimensions_and_page_count(self):
        info = parse_pdfinfo(
            "Pages:           12\nPage size:       595.28 x 841.89 pts (A4)\n"
        )
        self.assertEqual(info["pages"], 12)
        self.assertAlmostEqual(info["width_pt"], 595.28)
        self.assertAlmostEqual(info["height_pt"], 841.89)

    def test_parse_pdfinfo_rejects_missing_page_size(self):
        with self.assertRaisesRegex(ValueError, "Page size"):
            parse_pdfinfo("Pages: 2\n")

    def test_required_text_reports_every_missing_heading(self):
        errors = validate_required_text("PROPOSAL SKRIPSI\nBAB 1 PENDAHULUAN")
        self.assertIn("BAB 2 LANDASAN KEPUSTAKAAN", "\n".join(errors))
        self.assertIn("DAFTAR REFERENSI", "\n".join(errors))

    def test_parse_pdffonts_extracts_embedded_font_names(self):
        output = """name                                 type              encoding
------------------------------------ ----------------- ----------
ABCDEE+Carlito                       CID TrueType      Identity-H
ABCDEF+Carlito-Bold                  CID TrueType      Identity-H
"""
        self.assertEqual(parse_pdffonts(output), {"Carlito", "Carlito-Bold"})

    def test_preview_accepts_carlito_and_official_requires_calibri(self):
        self.assertEqual(validate_fonts({"Carlito", "Carlito-Bold"}, "preview"), [])
        self.assertEqual(validate_fonts({"Calibri", "Calibri-Bold"}, "preview"), [])
        self.assertTrue(validate_fonts({"Carlito"}, "official"))
        self.assertTrue(validate_fonts({"Calibri", "Calibri-Bold"}, "official"))
        self.assertEqual(
            validate_fonts({"Calibri", "Calibri-Bold", "Calibri-Italic"}, "official"),
            [],
        )

    def test_structure_requires_real_page_heading_order_and_lampiran_label(self):
        text = "\f".join(
            [
                "SAMPUL",
                "DAFTAR ISI\nDAFTAR ISI ii\nDAFTAR TABEL iii\nDAFTAR GAMBAR iv",
                "DAFTAR TABEL\nTabel 3.1 Contoh",
                "DAFTAR GAMBAR\nGambar 2.1 Contoh",
                "DAFTAR LAMPIRAN",
                "DAFTAR ISTILAH, SIMBOL, DAN SINGKATAN",
                "BAB 1 PENDAHULUAN\nisi",
                "BAB 2 LANDASAN KEPUSTAKAAN\nisi",
                "BAB 3 METODOLOGI PENELITIAN\nisi",
                "DAFTAR REFERENSI\nisi",
                "LAMPIRAN A INSTRUMEN ATAU RINCIAN PENDUKUNG\nisi",
            ]
        )
        self.assertEqual(validate_document_structure(text), [])
        self.assertTrue(validate_document_structure(text.replace("LAMPIRAN A", "BAB A")))

    def test_forbidden_thesis_frontmatter_is_case_insensitive(self):
        errors = validate_required_text(
            "proposal skripsi daftar isi bab 1 pendahuluan "
            "bab 2 landasan kepustakaan bab 3 metodologi penelitian "
            "jadwal penelitian daftar referensi "
            "lampiran a instrumen atau rincian pendukung AbStRaK"
        )
        self.assertIn("ABSTRAK", "\n".join(errors))

    def test_reference_style_requires_commas_and_all_three_authors(self):
        valid = (
            "(Lamport, 1994) Daftar Referensi Knuth, D.E., 1984. "
            "Fielding, R.T., Nottingham, M., dan Reschke, J., 2022. "
            "Dalam: Buku Contoh. Tersedia di: https://example.invalid "
            "[Diakses 2 September 2026]."
        )
        self.assertEqual(validate_reference_style(valid), [])
        self.assertTrue(validate_reference_style(valid.replace("D.E., 1984", "D.E. 1984")))
        for english in (
            " Fielding, R.T., and Reschke, J.",
            " In:",
            " Ed. by",
            " visited on",
            " URL:",
        ):
            self.assertTrue(validate_reference_style(valid + english))

    def test_frontmatter_requires_uppercase_titles_and_toc_entries(self):
        text = "\f".join(
            [
                "SAMPUL",
                "DAFTAR ISI\nDAFTAR ISI ii\nDAFTAR TABEL iii\nDAFTAR GAMBAR iv",
                "DAFTAR TABEL\nTabel 3.1 Contoh",
                "DAFTAR GAMBAR\nGambar 2.1 Contoh",
                "DAFTAR LAMPIRAN",
                "DAFTAR ISTILAH, SIMBOL, DAN SINGKATAN",
                "BAB 1 PENDAHULUAN",
                "BAB 2 LANDASAN KEPUSTAKAAN",
                "BAB 3 METODOLOGI PENELITIAN",
                "DAFTAR REFERENSI",
                "LAMPIRAN A INSTRUMEN ATAU RINCIAN PENDUKUNG",
            ]
        )
        self.assertEqual(validate_document_structure(text), [])
        self.assertTrue(validate_document_structure(text.replace("DAFTAR TABEL\n", "Daftar Tabel\n", 1)))
        self.assertTrue(validate_document_structure(text.replace("DAFTAR GAMBAR iv", "", 1)))

    def test_pdf_xml_requires_14pt_cover_text_and_fully_bold_captions(self):
        valid = """<?xml version="1.0" encoding="UTF-8"?>
<pdf2xml><page number="1">
<fontspec id="0" size="24" family="Carlito"/><fontspec id="1" size="21" family="Carlito"/>
<text top="100" font="0"><b>JUDUL PROPOSAL</b></text>
<text top="180" font="1"><b>PROPOSAL SKRIPSI</b></text><text top="220" font="1">Disusun oleh:</text>
</page><page number="2"><fontspec id="2" size="18" family="Carlito"/>
<text top="300" font="2"><b>Gambar 2.1</b></text><text top="300" font="2"><b>Contoh gambar</b></text>
<text top="400" font="2"><b>Tabel 3.1</b></text><text top="400" font="2"><b>Contoh tabel</b></text>
</page></pdf2xml>"""
        invalid_cover = valid.replace('font="1">Disusun', 'font="2">Disusun')
        invalid_caption = valid.replace("<b>Contoh gambar</b>", "Contoh gambar")
        self.assertEqual(check_pdf.validate_typography_xml(valid), [])
        self.assertTrue(check_pdf.validate_typography_xml(invalid_cover))
        self.assertTrue(check_pdf.validate_typography_xml(invalid_caption))


if __name__ == "__main__":
    unittest.main()
