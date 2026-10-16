import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from helpers import Sandbox, forward  # noqa: E402


class CheckUpdateTests(Sandbox):
    def setUp(self):
        super().setUp()
        self.c = self.clone()

    def check(self, *args):
        rc, out, err = self.run_tool("check_update.py", "--repo", forward(self.c), *args)
        self.assertEqual(rc, 0, err)
        return out.strip()

    # ---------------------------------------------------------------- --pull
    def test_al_dia(self):
        self.assertEqual(self.check("--quiet", "--pull"), "AL_DIA")

    def test_behind_and_clean_pulls(self):
        new = self.push_from_other()
        out = self.check("--quiet", "--pull")
        self.assertEqual(out, "ACTUALIZADA 1")
        self.assertEqual(self.head(self.c), new)
        self.assertEqual(self.status(self.c), "")

    def test_pull_message_in_spanish_when_not_quiet(self):
        self.push_from_other()
        out = self.check("--pull")
        self.assertTrue(out.startswith("ACTUALIZADA 1 - "), out)
        self.assertIn("vuelve a leer el SKILL.md", out)

    def test_without_pull_flag_stays_behind(self):
        before = self.head(self.c)
        self.push_from_other()
        self.assertEqual(self.check("--quiet"), "ATRASADA 1")
        self.assertEqual(self.head(self.c), before)

    def test_two_commits_count(self):
        self.push_from_other()
        self.push_from_other(text="\notro\n")
        self.assertEqual(self.check("--quiet", "--pull"), "ACTUALIZADA 2")

    def test_dirty_never_pulls(self):
        before = self.head(self.c)
        self.push_from_other()
        self.edit(self.c)
        out = self.check("--quiet", "--pull")
        self.assertEqual(out, "CAMBIOS_LOCALES")
        self.assertEqual(self.head(self.c), before)
        self.assertIn("línea nueva", (self.c / "skills/demo/HANDOFF.md").read_text(encoding="utf-8"))

    def test_unpushed_commit_never_pulls(self):
        self.edit(self.c)
        self.git(self.c, "commit", "-qam", "local", "--no-verify")
        before = self.head(self.c)
        self.push_from_other()
        self.assertEqual(self.check("--quiet", "--pull"), "CAMBIOS_LOCALES")
        self.assertEqual(self.head(self.c), before)

    def test_unreachable_remote(self):
        self.git(self.c, "remote", "set-url", "origin", forward(self.tmp / "no-existe.git"))
        before = self.head(self.c)
        self.assertEqual(self.check("--quiet", "--pull"), "SIN_RED")
        self.assertEqual(self.head(self.c), before)

    def test_other_branch_is_not_pulled(self):
        self.git(self.c, "checkout", "-q", "-b", "trabajo")
        self.push_from_other()
        out = self.check("--pull")
        self.assertTrue(out.startswith("ATRASADA 1"), out)
        self.assertIn("trabajo", out)
        self.assertEqual(self.check("--quiet", "--pull"), "ATRASADA 1")

    def test_failed_pull_reports_atrasada_with_reason(self):
        # a local edit hidden from `git status` (assume-unchanged) that the incoming commit also touches:
        # the clone looks clean, but `git pull --ff-only` refuses to overwrite it
        self.edit(self.c, "skills/demo/SKILL.md", "\nedicion local oculta\n")
        self.git(self.c, "update-index", "--assume-unchanged", "skills/demo/SKILL.md")
        self.assertEqual(self.status(self.c), "")
        self.push_from_other(rel="skills/demo/SKILL.md", text="\nremoto\n")
        before = self.head(self.c)
        out = self.check("--pull")
        self.assertTrue(out.startswith("ATRASADA 1 - "), out)
        self.assertIn("no se pudieron descargar solos", out)
        self.assertEqual(self.head(self.c), before)
        self.assertEqual(self.check("--quiet", "--pull"), "ATRASADA 1")
        rc, hook, _ = self.run_tool("check_update.py", "--repo", forward(self.c), "--hook", "--pull")
        self.assertEqual(rc, 0)
        self.assertEqual(len(hook.strip().splitlines()), 1)
        self.assertIn("no se pudieron descargar solos", hook)

    # ---------------------------------------------------------------- --hook
    def test_hook_pull_one_line_exit_zero(self):
        self.push_from_other()
        rc, out, _ = self.run_tool("check_update.py", "--repo", forward(self.c), "--hook", "--pull")
        self.assertEqual(rc, 0)
        self.assertEqual(len(out.strip().splitlines()), 1, out)
        self.assertIn("se descargaron 1 cambio", out)
        self.assertEqual(self.status(self.c), "")

    def test_hook_pull_is_not_rate_limited(self):
        run = lambda *a: self.run_tool("check_update.py", "--repo", forward(self.c), "--hook", *a)  # noqa: E731
        rc, out, _ = run("--pull")
        self.assertIn("al día", out)
        last = json.loads((self.home / "last_check.json").read_text(encoding="utf-8"))
        self.assertEqual(last["estado"], "AL_DIA")
        new = self.push_from_other()
        # old behaviour without --pull: a check made seconds ago is reused, GitHub is not asked again
        rc, out, _ = run()
        self.assertEqual(rc, 0)
        self.assertIn("al día", out)
        self.assertIn("hace 0 h", out)
        self.assertNotEqual(self.head(self.c), new)
        # with --pull every session start fetches and updates
        rc, out, _ = run("--pull")
        self.assertEqual(len(out.strip().splitlines()), 1, out)
        self.assertIn("se descargaron 1 cambio", out)
        self.assertEqual(self.head(self.c), new)

    def test_hook_pull_dirty_and_offline_never_fail(self):
        self.edit(self.c)
        rc, out, _ = self.run_tool("check_update.py", "--repo", forward(self.c), "--hook", "--pull")
        self.assertEqual(rc, 0)
        self.assertEqual(len(out.strip().splitlines()), 1)
        self.assertIn("sin guardar", out)
        self.git(self.c, "checkout", "-q", "--", ".")
        self.git(self.c, "remote", "set-url", "origin", forward(self.tmp / "no-existe.git"))
        rc, out, _ = self.run_tool("check_update.py", "--repo", forward(self.c), "--hook", "--pull")
        self.assertEqual(rc, 0)
        self.assertEqual(len(out.strip().splitlines()), 1)
        self.assertIn("sin conexión", out)

    def test_hook_with_broken_repo_path(self):
        rc, out, _ = self.run_tool("check_update.py", "--repo", forward(self.tmp / "nada"), "--hook", "--pull")
        self.assertEqual(rc, 0)
        self.assertEqual(len(out.strip().splitlines()), 1)

    # ---------------------------------------------------------------- pending contributions
    def make_pending(self, name="aporte/tester/2026-01-02-x"):
        self.git(self.c, "checkout", "-q", "-b", name)
        self.edit(self.c)
        self.git(self.c, "commit", "-qam", "aporte local", "--no-verify")
        self.git(self.c, "checkout", "-q", "main")
        return name

    def test_pending_branch_warning_keeps_first_token(self):
        name = self.make_pending()
        lines = self.check("--quiet", "--pull").splitlines()
        self.assertEqual(lines[0], "AL_DIA")
        self.assertEqual(len(lines), 2)
        self.assertIn(f"hay aportes sin publicar: {name}", lines[1])
        self.assertIn("publish_job.py", lines[1])
        self.assertIn("--reintentar", lines[1])

    def test_pending_warning_in_hook_line(self):
        name = self.make_pending()
        rc, out, _ = self.run_tool("check_update.py", "--repo", forward(self.c), "--hook", "--pull")
        self.assertEqual(rc, 0)
        self.assertEqual(len(out.strip().splitlines()), 1, out)
        self.assertIn(name, out)
        self.assertIn("--reintentar", out)

    def test_pending_warning_also_when_behind_and_updated(self):
        self.make_pending()
        self.push_from_other()
        lines = self.check("--quiet", "--pull").splitlines()
        self.assertEqual(lines[0], "ACTUALIZADA 1")
        self.assertIn("hay aportes sin publicar", lines[1])

    def test_no_warning_once_pushed(self):
        name = self.make_pending()
        self.git(self.c, "push", "-q", "-u", "origin", name)
        self.assertEqual(self.check("--quiet"), "AL_DIA")

    def test_two_pending_branches_are_listed(self):
        a = self.make_pending("aporte/tester/a")
        b = self.make_pending("aporte/tester/b")
        out = self.check("--quiet")
        self.assertIn(f"{a}, {b}", out)

    def test_ahead_of_its_remote_counterpart_is_pending(self):
        name = self.make_pending()
        self.git(self.c, "push", "-q", "-u", "origin", name)
        self.git(self.c, "checkout", "-q", name)
        self.edit(self.c, text="\nmás\n")
        self.git(self.c, "commit", "-qam", "otro", "--no-verify")
        self.git(self.c, "checkout", "-q", "main")
        self.assertIn(name, self.check("--quiet"))

    def test_branch_merged_and_deleted_on_github_is_not_pending(self):
        name = self.make_pending()
        self.git(self.c, "push", "-q", "-u", "origin", name)
        # the maintainer squash-merges it (same content, different commit) and deletes the branch
        other = self.clone("mantenedor")
        self.git(other, "fetch", "-q", "origin")
        self.git(other, "merge", "-q", "--squash", f"origin/{name}")
        self.git(other, "commit", "-q", "-m", "squash", "--no-verify")
        self.git(other, "push", "-q", "origin", "main")
        self.git(other, "push", "-q", "origin", f":{name}")
        self.git(self.c, "config", "fetch.prune", "true")
        out = self.check("--quiet", "--pull")
        self.assertEqual(out.splitlines()[0], "ACTUALIZADA 1")
        self.assertEqual(len(out.splitlines()), 1, out)


if __name__ == "__main__":
    unittest.main()
