from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PackageContractTests(unittest.TestCase):
    def test_required_public_files_exist(self):
        required = {
            "LICENSE",
            "README.md",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "CITATION.cff",
            ".editorconfig",
            ".gitignore",
        }
        missing = sorted(name for name in required if not (ROOT / name).is_file())
        self.assertEqual([], missing)

    def test_license_is_lppl_1_3c(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("LaTeX Project Public License", license_text)
        self.assertIn("version 1.3c", license_text)

    def test_readme_declares_unofficial_filkom_status(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("tidak resmi", readme)
        self.assertIn("filkom", readme)


if __name__ == "__main__":
    unittest.main()
