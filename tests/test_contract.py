from pathlib import Path
import hashlib
import unittest
import xml.etree.ElementTree as ET


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

    def test_bundled_logo_is_safe_and_documented(self):
        svg = ROOT / "assets" / "logo-ub.svg"
        png = ROOT / "assets" / "logo-ub.png"
        notice = ROOT / "assets" / "NOTICE.md"
        self.assertEqual(
            "47f1aa7d2b067dc3224a9e0066d09d49a3db84a8130c280de2dac296d57965c7",
            hashlib.sha256(svg.read_bytes()).hexdigest(),
        )
        root = ET.parse(svg).getroot()
        forbidden = []
        for element in root.iter():
            tag = element.tag.rsplit("}", 1)[-1].lower()
            if tag in {"script", "foreignobject"}:
                forbidden.append(tag)
            for key, value in element.attrib.items():
                value_lower = value.lower()
                if key.lower().startswith("on") or value_lower.startswith(
                    ("http://", "https://", "data:", "javascript:")
                ):
                    forbidden.append(f"{tag}:{key}")
        self.assertEqual([], forbidden)
        self.assertEqual(b"\x89PNG\r\n\x1a\n", png.read_bytes()[:8])
        self.assertIn("tidak tercakup oleh lppl", notice.read_text(encoding="utf-8").lower())


if __name__ == "__main__":
    unittest.main()
