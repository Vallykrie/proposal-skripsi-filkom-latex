import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DocumentationTests(unittest.TestCase):
    def test_public_guides_exist(self):
        required = (
            "docs/compatibility.md",
            "docs/compliance-matrix.md",
            "docs/troubleshooting.md",
            "examples/minimal/README.md",
        )
        self.assertEqual([], [path for path in required if not (ROOT / path).is_file()])

    def test_readme_covers_complete_user_journey(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        for phrase in (
            "mulai dalam 5 menit",
            "metadata.tex",
            "make preview",
            "make official",
            "macos",
            "linux",
            "windows",
            "overleaf",
            "calibri",
            "carlito",
            "lppl 1.3c",
            "tidak resmi",
        ):
            self.assertIn(phrase, readme)

    def test_compliance_matrix_is_auditable(self):
        matrix = (ROOT / "docs/compliance-matrix.md").read_text(encoding="utf-8")
        for rule in (
            "A4",
            "4 cm",
            "3 cm",
            "Calibri",
            "PROPOSAL SKRIPSI",
            "Jadwal Penelitian",
            "Daftar Referensi",
            "Panduan Skripsi FILKOM versi 3.0",
        ):
            self.assertIn(rule, matrix)
        self.assertIn("https://filkom.ub.ac.id/pendidikan/layanan-akademik-filkom-ub/", matrix)

    def test_compatibility_and_troubleshooting_cover_supported_paths(self):
        compatibility = (ROOT / "docs/compatibility.md").read_text(encoding="utf-8").lower()
        troubleshooting = (ROOT / "docs/troubleshooting.md").read_text(encoding="utf-8").lower()
        for token in ("tex live", "miktex", "overleaf", "xelatex", "biber"):
            self.assertIn(token, compatibility)
        for token in ("calibri", "carlito", "biber", "logo", "referensi"):
            self.assertIn(token, troubleshooting)


if __name__ == "__main__":
    unittest.main()
