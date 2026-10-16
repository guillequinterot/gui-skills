import shutil
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from helpers import REPO_ROOT, Sandbox  # noqa: E402

SKILL = "seo-content-system"
HOSTED = "seo-content-system-web-hosted"


class BuildHostedTests(Sandbox):
    """build_hosted.py --check must not depend on how the checkout turned line endings (core.autocrlf)."""

    def setUp(self):
        super().setUp()
        self.work = self.tmp / "copia"
        (self.work / "tools").mkdir(parents=True)
        shutil.copy2(REPO_ROOT / "tools" / "build_hosted.py", self.work / "tools")
        for name in (SKILL, HOSTED):
            shutil.copytree(REPO_ROOT / "skills" / name, self.work / "skills" / name)
        self.convert(self.work / "skills", crlf=False)  # start from LF, as in the repository

    def convert(self, root: Path, crlf: bool):
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in (".md", ".json", ".txt"):
                text = path.read_bytes().replace(b"\r\n", b"\n")
                path.write_bytes(text.replace(b"\n", b"\r\n") if crlf else text)

    def check(self):
        return self.run_tool("build_hosted.py", "--check", "--repo", str(self.work))

    def test_lf_checkout_is_up_to_date(self):
        rc, out, err = self.check()
        self.assertEqual(rc, 0, out + err)
        self.assertIn("AL DIA", out)

    def test_crlf_checkout_is_still_up_to_date(self):
        self.convert(self.work / "skills", crlf=True)
        rc, out, err = self.check()
        self.assertEqual(rc, 0, out + err)
        self.assertIn("AL DIA", out)

    def test_real_difference_is_still_detected(self):
        target = self.work / "skills" / HOSTED / "00-instrucciones-del-proyecto.md"
        target.write_bytes(target.read_bytes() + b"\nlinea de mas\n")
        self.convert(self.work / "skills", crlf=True)
        rc, out, _ = self.check()
        self.assertEqual(rc, 1)
        self.assertIn("DESFASADA", out)
        self.assertIn("00-instrucciones-del-proyecto.md", out)


if __name__ == "__main__":
    unittest.main()
