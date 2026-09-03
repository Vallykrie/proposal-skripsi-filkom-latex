from pathlib import Path
import tempfile
import unittest

from scripts.build import clean_build_dir, latexmk_command, remove_stale_pdf
from scripts.check_log import log_problems


class BuildToolTests(unittest.TestCase):
    def test_latexmk_command_uses_xelatex_and_enables_bibliography_processing(self):
        command = latexmk_command("official", Path("build/entry.tex"))
        self.assertEqual("latexmk", command[0])
        self.assertIn("-xelatex", command)
        self.assertIn("-bibtex", command)
        self.assertNotIn("-use-biber", command)
        self.assertIn("-jobname=proposal", command)

    def test_latexmk_command_rejects_unknown_mode(self):
        with self.assertRaisesRegex(ValueError, "Mode tidak didukung"):
            latexmk_command("release", Path("build/entry.tex"))

    def test_clean_only_accepts_directory_named_build(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            unsafe = root / "output"
            unsafe.mkdir()
            (unsafe / "keep.txt").write_text("keep", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "bernama build"):
                clean_build_dir(unsafe)
            self.assertTrue((unsafe / "keep.txt").exists())

    def test_clean_removes_build_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            build = Path(directory) / "build"
            build.mkdir()
            (build / "proposal.aux").write_text("generated", encoding="utf-8")
            clean_build_dir(build)
            self.assertTrue(build.is_dir())
            self.assertEqual([], list(build.iterdir()))

    def test_remove_stale_pdf_only_accepts_proposal_pdf_inside_build(self):
        with tempfile.TemporaryDirectory() as directory:
            build = Path(directory) / "build"
            build.mkdir()
            stale = build / "proposal.pdf"
            stale.write_bytes(b"old preview")
            remove_stale_pdf(stale)
            self.assertFalse(stale.exists())
            unsafe = Path(directory) / "proposal.pdf"
            unsafe.write_bytes(b"keep")
            with self.assertRaisesRegex(ValueError, "build/proposal.pdf"):
                remove_stale_pdf(unsafe)
            self.assertTrue(unsafe.exists())

    def test_log_checker_reports_actionable_latex_failures(self):
        log = "LaTeX Warning: Citation 'x' undefined.\nOverfull \\hbox (4.0pt too wide)"
        self.assertEqual(
            ["sitasi tidak terdefinisi", "overfull box melebihi 2.0 pt"],
            log_problems(log, overfull_limit=2.0),
        )

    def test_log_checker_rejects_bibliography_language_fallbacks(self):
        log = (
            "Package biblatex Warning: Language 'bahasa' not supported.\n"
            "Package biblatex Warning: 'babel/polyglossia' detected but "
            "'csquotes' missing.\n"
            "Package biblatex Warning: Using fallback definition for "
            "\\mkbibdateshort.\n"
            "Package biblatex Warning: Bibliography string 'edition' untranslated.\n"
        )
        self.assertEqual(
            ["konfigurasi bahasa bibliografi tidak lengkap"],
            log_problems(log),
        )

    def test_log_checker_rejects_untranslated_bibliography_fallbacks(self):
        log = (
            "Package csquotes Warning: No style for language 'indonesian'.\n"
            "Package biblatex Warning: Using fallback definition for "
            "\\mkbibdateshort.\n"
            "Package biblatex Warning: Bibliography string 'edition' untranslated.\n"
        )
        self.assertEqual(
            ["konfigurasi bahasa bibliografi tidak lengkap"],
            log_problems(log),
        )

    def test_log_checker_rejects_missing_indonesian_quote_style(self):
        log = "Package csquotes Warning: No style for language 'indonesian'.\n"
        self.assertEqual(
            ["konfigurasi bahasa bibliografi tidak lengkap"],
            log_problems(log),
        )


if __name__ == "__main__":
    unittest.main()
