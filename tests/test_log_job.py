import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from helpers import Sandbox, forward  # noqa: E402


class LogJobTests(Sandbox):
    def setUp(self):
        super().setUp()
        self.c = self.clone()
        self.handoff = self.c / "skills" / "demo" / "HANDOFF.md"

    def log(self, *extra, caso="caso-demo-01", hecho="Se hizo la prueba", bien="Salió bien", mal="nada relevante"):
        return self.run_tool("log_job.py", "--repo", forward(self.c), "--skill", "demo", "--caso", caso,
                             "--hecho", hecho, "--bien", bien, "--mal", mal, "--fecha", "2026-01-02", *extra)

    def text(self):
        return self.handoff.read_text(encoding="utf-8")

    def test_appends_entry_before_end_marker_and_never_rewrites(self):
        rc, out, err = self.log()
        self.assertEqual(rc, 0, out + err)
        first = self.text()
        self.assertIn("### 2026-01-02 · caso-demo-01 · tester", first)
        self.assertLess(first.index("caso-demo-01"), first.index("<!-- registro:fin -->"))
        rc, out, err = self.log(caso="caso-demo-02", hecho="Segunda prueba")
        self.assertEqual(rc, 0, out + err)
        second = self.text()
        self.assertIn("Se hizo la prueba", second)  # old entry preserved
        self.assertLess(second.index("caso-demo-01"), second.index("caso-demo-02"))

    def test_rule_candidate_adds_table_row(self):
        rc, out, err = self.log("--regla-candidata", "Probar siempre antes de publicar")
        self.assertEqual(rc, 0, out + err)
        self.assertIn("| Probar siempre antes de publicar | caso-demo-01 | candidata |", self.text())

    def test_private_term_is_refused_and_nothing_written(self):
        before = self.text()
        rc, out, err = self.log(hecho="Trabajo de ClienteSecreto")
        self.assertEqual(rc, 1)
        self.assertEqual(self.text(), before)
        self.assertIn("--hecho", err)

    def test_case_code_must_be_a_code(self):
        rc, _, err = self.log(caso="Universidad de Ejemplo")
        self.assertEqual(rc, 1)
        self.assertIn("caso-", err)

    def test_dry_run_writes_nothing(self):
        before = self.text()
        rc, out, _ = self.log("--dry-run")
        self.assertEqual(rc, 0)
        self.assertIn("[dry-run]", out)
        self.assertEqual(self.text(), before)

    def test_lf_file_stays_lf_and_crlf_file_stays_crlf(self):
        self.assertNotIn(b"\r", self.handoff.read_bytes())
        rc, out, err = self.log()
        self.assertEqual(rc, 0, out + err)
        self.assertNotIn(b"\r", self.handoff.read_bytes())
        self.handoff.write_bytes(self.handoff.read_bytes().replace(b"\n", b"\r\n"))
        rc, out, err = self.log(caso="caso-demo-02")
        self.assertEqual(rc, 0, out + err)
        data = self.handoff.read_bytes()
        self.assertEqual(data.count(b"\n"), data.count(b"\r\n"))  # every line break is still CRLF
        self.assertIn(b"caso-demo-02", data)


if __name__ == "__main__":
    unittest.main()
