import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import privacy_scan  # noqa: E402

# Fixtures are assembled at run time so this file itself stays clean for the repo-wide scan.
EMAIL = "persona" + "@" + "empresa-real.com"
TOKEN = "gh" + "p_" + "abcdEFGH1234ijklMNOP5678qrstUVWX"
WIN_PATH = "C:" + chr(92) + "Users" + chr(92) + "alguien" + chr(92) + "Desktop"


class PrivacyScanTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        terms = Path(self._tmp.name) / "terms.txt"
        terms.write_text("ClienteSecreto\nre:PROY-\\d{3}\n", encoding="utf-8")
        old_home = os.environ.get("GUI_SKILLS_HOME")
        os.environ["GUI_SKILLS_HOME"] = self._tmp.name  # no private-terms.txt of the real user is read
        self.addCleanup(lambda: os.environ.pop("GUI_SKILLS_HOME", None) if old_home is None
                        else os.environ.__setitem__("GUI_SKILLS_HOME", old_home))
        self.scanner = privacy_scan.build_scanner(use_terms=True, extra_terms=[str(terms)])

    def cats(self, text):
        return {f.category for f in self.scanner.scan_text(text, "x")}

    def test_clean_text(self):
        self.assertEqual(self.cats("Se maquetó la home en HTML con el caso caso-web-universidad-01."), set())

    def test_detects_email_token_path_and_terms(self):
        self.assertIn("correo", self.cats(f"escribir a {EMAIL}"))
        self.assertTrue(any("token" in c for c in self.cats(TOKEN)))
        self.assertTrue(self.cats(WIN_PATH))
        self.assertEqual(self.cats("trabajo de clientesecreto"), {"termino-privado"})
        self.assertEqual(self.cats("expediente PROY-123"), {"termino-privado"})

    def test_example_email_and_ignore_mark_are_allowed(self):
        self.assertEqual(self.cats("correo: ana@ejemplo.com"), set())
        self.assertEqual(self.cats("ana@gui-skills.local"), set())
        self.assertEqual(self.cats(f"{EMAIL} privacy-scan: ignore"), set())

    def test_cli_exit_codes(self):
        d = Path(self._tmp.name)
        good, bad = d / "bien.md", d / "mal.md"
        good.write_text("todo limpio\n", encoding="utf-8")
        bad.write_text(f"contacto {EMAIL}\n", encoding="utf-8")
        self.assertEqual(privacy_scan.main(["--ci", str(good)]), 0)
        self.assertEqual(privacy_scan.main(["--ci", str(bad)]), 1)


if __name__ == "__main__":
    unittest.main()
