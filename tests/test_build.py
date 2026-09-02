from pathlib import Path
import tempfile
import unittest

from scripts.build import clean_build_dir, latexmk_command
from scripts.check_log import log_problems


class BuildToolTests(unittest.TestCase):
    def test_latexmk_command_uses_xelatex_biber_and_selected_mode(self):
        command = latexmk_command("official", Path("build/entry.tex"))
        self.assertEqual("latexmk", command[0])
        self.assertIn("-xelatex", command)
        self.assertIn("-use-biber", command)
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

    def test_log_checker_reports_actionable_latex_failures(self):
        log = "LaTeX Warning: Citation 'x' undefined.\nOverfull \\hbox (4.0pt too wide)"
        self.assertEqual(
            ["sitasi tidak terdefinisi", "overfull box melebihi 2.0 pt"],
            log_problems(log, overfull_limit=2.0),
        )


if __name__ == "__main__":
    unittest.main()
