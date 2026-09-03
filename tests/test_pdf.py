import unittest

from scripts.check_pdf import (
    parse_pdffonts,
    parse_pdfinfo,
    validate_fonts,
    validate_required_text,
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
        self.assertTrue(validate_fonts({"Carlito"}, "official"))
        self.assertEqual(validate_fonts({"Calibri", "Calibri-Bold"}, "official"), [])


if __name__ == "__main__":
    unittest.main()
