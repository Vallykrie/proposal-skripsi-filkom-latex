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

    def test_latex_entry_points_and_structure_exist(self):
        required = [
            "filkomproposal.cls",
            "proposal.tex",
            "metadata.tex",
            "chapters/bab1-pendahuluan.tex",
            "chapters/bab2-landasan-kepustakaan.tex",
            "chapters/bab3-metodologi.tex",
            "frontmatter/daftar-istilah.tex",
            "appendices/lampiran-contoh.tex",
        ]
        self.assertEqual([], [name for name in required if not (ROOT / name).is_file()])

    def test_class_contract_has_modes_fonts_and_geometry(self):
        source = (ROOT / "filkomproposal.cls").read_text(encoding="utf-8")
        for token in (
            r"\ProvidesClass{filkomproposal}",
            r"\DeclareBoolOption[true]{preview}",
            r"\DeclareComplementaryOption{official}{preview}",
            r"\IfFontExistsTF{Calibri}",
            r"\setmainfont{Carlito}",
            "left=4cm",
            "right=3cm",
            "top=3cm",
            "bottom=3cm",
            r"\setlength{\parindent}{0.6cm}",
            r"\fontsize{16pt}{19pt}",
            r"\includegraphics[width=5cm]",
            r"\widowpenalty=10000",
            r"\filkomsetup",
        ):
            self.assertIn(token, source)

    def test_language_stack_uses_supported_babel_and_biblatex_configuration(self):
        cls = (ROOT / "filkomproposal.cls").read_text(encoding="utf-8")
        proposal = (ROOT / "proposal.tex").read_text(encoding="utf-8")
        self.assertIn(r"\RequirePackage[indonesian]{babel}", cls)
        self.assertIn(r"\RequirePackage{csquotes}", cls)
        self.assertIn(r"\DeclareQuoteAlias[american]{english}{indonesian}", cls)
        self.assertIn(r"\DeclareLanguageMapping{indonesian}{english}", proposal)
        self.assertNotIn(r"\RequirePackage[bahasa]{babel}", cls)

    def test_proposal_has_required_sections_without_final_thesis_frontmatter(self):
        files = [
            ROOT / "filkomproposal.cls",
            ROOT / "proposal.tex",
            *sorted((ROOT / "chapters").glob("*.tex")),
        ]
        text = "\n".join(path.read_text(encoding="utf-8") for path in files)
        for required in (
            "PROPOSAL SKRIPSI",
            "Pendahuluan",
            "Landasan Kepustakaan",
            "Metodologi Penelitian",
            "Jadwal Penelitian",
            "DAFTAR REFERENSI",
        ):
            self.assertIn(required, text)
        for forbidden in ("PENGESAHAN", "PERNYATAAN ORISINALITAS", "PRAKATA", "ABSTRACT"):
            self.assertNotIn(forbidden, text)

    def test_no_personal_or_obsolete_hardcodes_in_template_sources(self):
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for pattern in ("*.cls", "*.tex")
            for path in ROOT.rglob(pattern)
        )
        for forbidden in ("235150207111051", "2 Juli 2019", "Tri Astoto", "/Users/"):
            self.assertNotIn(forbidden, text)

    def test_bibliography_fixture_covers_supported_source_types(self):
        bib = (ROOT / "bibliography" / "references.bib").read_text(encoding="utf-8")
        for entry_type in (
            "@article",
            "@book",
            "@incollection",
            "@inproceedings",
            "@thesis",
            "@online",
            "@report",
            "@software",
        ):
            self.assertIn(entry_type, bib)
        self.assertNotIn("doi = {https://", bib.lower())
        self.assertIn("urldate", bib.lower())
        self.assertTrue((ROOT / "bibliography" / "filkom-authoryear.bbx").is_file())
        self.assertTrue((ROOT / "bibliography" / "filkom-authoryear.cbx").is_file())


if __name__ == "__main__":
    unittest.main()
