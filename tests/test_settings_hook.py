import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import settings_hook  # noqa: E402

OLD = 'python "C:/ruta/gui-skills/tools/check_update.py" --hook'
OTHER = {"type": "command", "command": "echo otro-hook", "timeout": 5}


def run(*args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        rc = settings_hook.main(list(args))
    return rc, out.getvalue()


def ours(settings):
    return [h for g in settings["hooks"]["SessionStart"] for h in g["hooks"] if "check_update.py" in h.get("command", "")]


class SettingsHookTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.path = Path(self._tmp.name) / "settings.json"
        self.bak = Path(self._tmp.name) / "bak"

    def load(self):
        return json.loads(self.path.read_text(encoding="utf-8"))

    def test_command_has_pull(self):
        cmd = settings_hook.build_command("python", "C:\\ruta\\tools\\check_update.py")
        self.assertEqual(cmd, 'python "C:/ruta/tools/check_update.py" --hook --pull')

    def test_fresh_install_writes_new_command(self):
        rc, out = run("--settings", str(self.path), "--python", "python", "--script", "/x/tools/check_update.py")
        self.assertEqual(rc, 0)
        self.assertTrue(out.startswith("added"))
        hooks = ours(self.load())
        self.assertEqual(len(hooks), 1)
        self.assertTrue(hooks[0]["command"].endswith("check_update.py\" --hook --pull"))

    def test_rerun_is_unchanged(self):
        args = ("--settings", str(self.path), "--python", "python", "--script", "/x/tools/check_update.py", "--backup-dir", str(self.bak))
        run(*args)
        rc, out = run(*args)
        self.assertEqual(rc, 0)
        self.assertTrue(out.startswith("unchanged"))
        self.assertEqual(len(ours(self.load())), 1)

    def test_replaces_old_command_keeps_other_hooks(self):
        self.path.write_text(json.dumps({
            "model": "x",
            "hooks": {
                "SessionStart": [
                    {"matcher": "startup", "hooks": [OTHER]},
                    {"matcher": "startup|resume|clear", "hooks": [{"type": "command", "command": OLD, "timeout": 20}]},
                ],
                "PreToolUse": [{"matcher": "Bash", "hooks": [OTHER]}],
            }}), encoding="utf-8")
        new = 'python "/nueva/tools/check_update.py" --hook --pull'
        rc, out = run("--settings", str(self.path), "--command", new, "--backup-dir", str(self.bak))
        self.assertEqual(rc, 0)
        self.assertIn("updated", out)
        data = self.load()
        self.assertEqual(data["model"], "x")
        self.assertEqual(len(ours(data)), 1)
        self.assertEqual(ours(data)[0]["command"], new)
        self.assertEqual(data["hooks"]["PreToolUse"][0]["hooks"][0], OTHER)
        self.assertEqual(data["hooks"]["SessionStart"][0]["hooks"][0], OTHER)
        self.assertTrue(list(self.bak.glob("settings.json.bak-*")))

    def test_old_command_without_hook_flag_is_also_replaced(self):
        self.path.write_text(json.dumps({"hooks": {"SessionStart": [
            {"hooks": [{"type": "command", "command": "python /x/tools/check_update.py --quiet"}]}]}}), encoding="utf-8")
        new = 'python "/y/tools/check_update.py" --hook --pull'
        run("--settings", str(self.path), "--command", new, "--backup-dir", str(self.bak))
        self.assertEqual([h["command"] for h in ours(self.load())], [new])

    def test_duplicates_collapse_into_one(self):
        self.path.write_text(json.dumps({"hooks": {"SessionStart": [
            {"hooks": [{"type": "command", "command": OLD}, OTHER]},
            {"hooks": [{"type": "command", "command": OLD + " --extra"}]},
        ]}}), encoding="utf-8")
        new = 'python "/y/tools/check_update.py" --hook --pull'
        run("--settings", str(self.path), "--command", new, "--backup-dir", str(self.bak))
        data = self.load()
        self.assertEqual([h["command"] for h in ours(data)], [new])
        self.assertIn(OTHER, [h for g in data["hooks"]["SessionStart"] for h in g["hooks"]])
        self.assertTrue(all(g["hooks"] for g in data["hooks"]["SessionStart"]))

    def test_remove_keeps_other_hooks(self):
        self.path.write_text(json.dumps({"hooks": {"SessionStart": [
            {"hooks": [{"type": "command", "command": OLD}, OTHER]}]}}), encoding="utf-8")
        rc, out = run("--settings", str(self.path), "--remove", "--backup-dir", str(self.bak))
        self.assertEqual(rc, 0)
        data = self.load()
        self.assertEqual(ours_count(data), 0)
        self.assertEqual(data["hooks"]["SessionStart"][0]["hooks"], [OTHER])

    def test_invalid_json_untouched(self):
        self.path.write_text("{no es json", encoding="utf-8")
        rc, _ = run("--settings", str(self.path), "--command", "x check_update.py --hook --pull")
        self.assertEqual(rc, 1)
        self.assertEqual(self.path.read_text(encoding="utf-8"), "{no es json")


def ours_count(data):
    return sum(1 for g in data.get("hooks", {}).get("SessionStart", []) for h in g["hooks"] if "check_update.py" in h.get("command", ""))


if __name__ == "__main__":
    unittest.main()
