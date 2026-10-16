import re
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from helpers import ALIAS, MockGitHub, Sandbox, forward  # noqa: E402
import publish_job  # noqa: E402

FECHA = "2026-01-02"
BRANCH = f"aporte/{ALIAS}/{FECHA}-demo-uno"
FAKE_TOKEN = "token-de-prueba-123"


class ParseRemoteTests(unittest.TestCase):
    def test_github_urls(self):
        p = publish_job.parse_github_remote
        self.assertEqual(p("https://github.com/dueno/repo.git"), ("dueno", "repo"))
        self.assertEqual(p("https://github.com/dueno/repo"), ("dueno", "repo"))
        self.assertEqual(p("https://github.com/dueno/repo/"), ("dueno", "repo"))
        self.assertEqual(p("https://usuario@github.com/dueno/repo.git"), ("dueno", "repo"))  # privacy-scan: ignore
        self.assertEqual(p("git@github.com:dueno/repo.git"), ("dueno", "repo"))
        self.assertEqual(p("ssh://git@github.com/dueno/repo.git"), ("dueno", "repo"))

    def test_non_github_is_none(self):
        p = publish_job.parse_github_remote
        for url in ("", "C:/ruta/remote.git", "/tmp/remote.git", "file:///tmp/remote.git",
                    "https://gitlab.com/a/b.git", "https://github.com/solo-uno", None):
            self.assertIsNone(p(url), url)


class PublishBase(Sandbox):
    def setUp(self):
        super().setUp()
        self.c = self.clone()

    def publish(self, *args, env=None, repo=None):
        return self.run_tool("publish_job.py", "--repo", forward(repo or self.c), "--fecha", FECHA, *args, env=env)

    def as_github(self, owner="fake", name="repo"):
        """Make origin look like a GitHub URL while pushes still go to the local bare repo."""
        fake = f"https://github.com/{owner}/{name}.git"
        self.git(self.c, "remote", "set-url", "origin", fake)
        self.git(self.c, "config", f"url.{forward(self.remote)}.insteadOf", fake)
        return fake

    def assertBackOnCleanMain(self, repo=None):
        repo = repo or self.c
        self.assertEqual(self.branch(repo), "main")
        self.assertEqual(self.status(repo), "")


class PublishTests(PublishBase):
    def test_skills_change_branch_commit_push_and_manual_pr(self):
        self.edit(self.c)
        main_before = self.git(self.remote, "rev-parse", "main")
        rc, out, err = self.publish("--tema", "demo-uno", "--mensaje", "Registro de prueba")
        self.assertEqual(rc, 0, out + err)
        self.assertTrue(out.startswith("PR_MANUAL"), out)
        self.assertIn(BRANCH, self.remote_branches())
        self.assertEqual(self.git(self.remote, "rev-parse", "main"), main_before)  # main untouched
        self.assertBackOnCleanMain()
        msg = self.git(self.remote, "log", "-1", "--format=%B", BRANCH)
        self.assertTrue(msg.startswith("Registro de prueba"))
        self.assertTrue(msg.rstrip().endswith(f"Aporte de {ALIAS} vía gui-skills"), msg)
        changed = self.git(self.remote, "diff", "--name-only", f"main..{BRANCH}").split()
        self.assertEqual(changed, ["skills/demo/HANDOFF.md"])
        self.assertNotIn("sin commits", self.git(self.c, "branch", "--list", BRANCH) + "")

    def test_default_message(self):
        self.edit(self.c)
        self.publish("--tema", "demo-uno")
        self.assertEqual(self.git(self.remote, "log", "-1", "--format=%s", BRANCH), "Registro de trabajo: demo-uno")

    def test_sin_cambios(self):
        rc, out, _ = self.publish("--tema", "demo-uno")
        self.assertEqual(rc, 0)
        self.assertTrue(out.startswith("SIN_CAMBIOS"), out)
        self.assertEqual(self.remote_branches(), ["main"])

    def test_change_outside_skills_is_refused(self):
        self.edit(self.c, "README.md", "\notra línea\n")
        self.edit(self.c)
        rc, out, _ = self.publish("--tema", "demo-uno")
        self.assertEqual(rc, 1)
        self.assertTrue(out.startswith("ERROR"), out)
        self.assertIn("README.md", out)
        self.assertEqual(self.remote_branches(), ["main"])
        self.assertEqual(self.branch(self.c), "main")
        self.assertIn("M README.md", self.status(self.c))  # untouched
        self.assertEqual(self.git(self.c, "branch", "--list", "aporte/*"), "")

    def test_incluir_todo_allows_docs_and_tools(self):
        self.edit(self.c, "README.md", "\notra línea\n")
        self.edit(self.c, "tools/nuevo.py", "# hola\n")
        self.edit(self.c)
        rc, out, err = self.publish("--tema", "demo-uno", "--incluir-todo")
        self.assertEqual(rc, 0, out + err)
        changed = set(self.git(self.remote, "diff", "--name-only", f"main..{BRANCH}").split())
        self.assertEqual(changed, {"README.md", "tools/nuevo.py", "skills/demo/HANDOFF.md"})

    def test_incluir_todo_still_refuses_hooks(self):
        self.edit(self.c, ".githooks/pre-commit", "\n# trampa\n")
        rc, out, _ = self.publish("--tema", "demo-uno", "--incluir-todo")
        self.assertEqual(rc, 1)
        self.assertIn(".githooks/pre-commit", out)
        self.assertEqual(self.remote_branches(), ["main"])

    def test_not_on_main_is_refused(self):
        self.git(self.c, "checkout", "-q", "-b", "otra")
        self.edit(self.c)
        rc, out, _ = self.publish("--tema", "demo-uno")
        self.assertEqual(rc, 1)
        self.assertTrue(out.startswith("ERROR"), out)
        self.assertEqual(self.branch(self.c), "otra")

    def test_bad_tema_is_usage_error(self):
        rc, _, err = self.publish("--tema", "Tiene Espacios")
        self.assertEqual(rc, 2)
        rc, _, err = self.publish()
        self.assertEqual(rc, 2)

    def test_privacy_hook_blocks_and_state_is_restored(self):
        self.edit(self.c, text="\nTrabajo para ClienteSecreto terminado\n")
        head = self.head(self.c)
        rc, out, _ = self.publish("--tema", "demo-uno")
        self.assertEqual(rc, 1)
        self.assertTrue(out.startswith("BLOQUEADO"), out)
        self.assertIn("ClienteSecreto", out)  # the hook output is shown
        self.assertBranchless(head)
        self.assertIn("ClienteSecreto", (self.c / "skills/demo/HANDOFF.md").read_text(encoding="utf-8"))
        self.assertEqual(self.git(self.c, "diff", "--cached", "--name-only"), "")  # nothing staged
        self.assertEqual(self.remote_branches(), ["main"])

    def assertBranchless(self, head):
        self.assertEqual(self.branch(self.c), "main")
        self.assertEqual(self.head(self.c), head)
        self.assertEqual(self.git(self.c, "branch", "--list", "aporte/*"), "")
        self.assertEqual(self.git(self.c, "status", "--porcelain"), "M skills/demo/HANDOFF.md")

    def test_private_term_in_message_is_blocked_before_anything(self):
        self.edit(self.c)
        rc, out, _ = self.publish("--tema", "demo-uno", "--mensaje", "Para ClienteSecreto")
        self.assertEqual(rc, 1)
        self.assertTrue(out.startswith("BLOQUEADO"), out)
        self.assertEqual(self.git(self.c, "branch", "--list", "aporte/*"), "")

    def test_untracked_new_file_is_published_and_binary_ok(self):
        self.edit(self.c, "skills/demo/memoria/nota.md", "# nota\n")
        rc, out, _ = self.publish("--tema", "demo-uno")
        self.assertEqual(rc, 0, out)
        self.assertEqual(self.git(self.remote, "diff", "--name-only", f"main..{BRANCH}").split(), ["skills/demo/memoria/nota.md"])
        self.assertBackOnCleanMain()

    def test_branch_name_collision_adds_suffix(self):
        self.edit(self.c)
        self.publish("--tema", "demo-uno")
        self.edit(self.c, text="\nsegunda\n")
        rc, out, _ = self.publish("--tema", "demo-uno")
        self.assertEqual(rc, 0, out)
        self.assertIn(f"{BRANCH}-2", self.remote_branches())
        self.edit(self.c, text="\ntercera\n")
        self.publish("--tema", "demo-uno")
        self.assertIn(f"{BRANCH}-3", self.remote_branches())

    # ---------------------------------------------------------------- push failure / retry
    def test_push_failure_is_pending_then_retry_pushes(self):
        self.edit(self.c)
        moved = self.tmp / "remote-movido.git"
        self.remote.rename(moved)
        rc, out, _ = self.publish("--tema", "demo-uno")
        self.assertEqual(rc, 0, out)
        self.assertTrue(out.startswith(f"PENDIENTE {BRANCH}"), out)
        self.assertIn("--reintentar", out)
        self.assertBackOnCleanMain()
        self.assertEqual(self.git(self.c, "branch", "--list", BRANCH).strip(" *"), BRANCH)  # commit kept locally
        # the next check warns about it
        rc, chk, _ = self.run_tool("check_update.py", "--repo", forward(self.c), "--quiet")
        self.assertIn(f"hay aportes sin publicar: {BRANCH}", chk)
        # restore the remote and retry
        moved.rename(self.remote)
        rc, out, err = self.publish("--reintentar")
        self.assertEqual(rc, 0, out + err)
        self.assertTrue(out.startswith("PR_MANUAL"), out)
        self.assertIn(BRANCH, self.remote_branches())
        rc, chk, _ = self.run_tool("check_update.py", "--repo", forward(self.c), "--quiet")
        self.assertEqual(chk.strip(), "AL_DIA")
        # nothing left to retry
        rc, out, _ = self.publish("--reintentar")
        self.assertTrue(out.startswith("SIN_CAMBIOS"), out)

    def test_retry_dry_run_changes_nothing(self):
        self.edit(self.c)
        self.remote.rename(self.tmp / "remote-movido.git")
        self.publish("--tema", "demo-uno")
        (self.tmp / "remote-movido.git").rename(self.remote)
        rc, out, _ = self.publish("--reintentar", "--dry-run")
        self.assertIn("[dry-run]", out)
        self.assertIn(BRANCH, out)
        self.assertNotIn(BRANCH, self.remote_branches())

    # ---------------------------------------------------------------- main behind
    def test_main_behind_fast_forwards_with_stash(self):
        new = self.push_from_other(rel="skills/demo/SKILL.md")
        self.edit(self.c)
        self.edit(self.c, "skills/demo/memoria/nuevo.md", "# nuevo\n")  # untracked file travels in the stash too
        rc, out, err = self.publish("--tema", "demo-uno")
        self.assertEqual(rc, 0, out + err)
        self.assertIn("se actualizó antes de publicar", out)
        self.assertBackOnCleanMain()
        self.assertEqual(self.head(self.c), new)  # main fast-forwarded
        self.assertEqual(self.git(self.remote, "merge-base", "main", BRANCH), new)  # branch starts from the new main
        changed = set(self.git(self.remote, "diff", "--name-only", f"main..{BRANCH}").split())
        self.assertEqual(changed, {"skills/demo/HANDOFF.md", "skills/demo/memoria/nuevo.md"})
        self.assertEqual(self.git(self.c, "stash", "list"), "")

    def test_main_behind_with_conflict_aborts_and_restores(self):
        base = self.head(self.c)
        self.push_from_other(rel="skills/demo/HANDOFF.md", text="\nlínea de la otra persona\n")
        self.edit(self.c, text="\nlínea mía\n")
        self.edit(self.c, "skills/demo/memoria/nuevo.md", "# nuevo\n")
        rc, out, _ = self.publish("--tema", "demo-uno")
        self.assertEqual(rc, 1)
        self.assertTrue(out.startswith("ERROR"), out)
        self.assertEqual(self.head(self.c), base)  # not advanced
        self.assertEqual(self.branch(self.c), "main")
        self.assertEqual(self.git(self.c, "stash", "list"), "")
        status = self.status(self.c).splitlines()
        self.assertIn("M skills/demo/HANDOFF.md", status)
        self.assertIn("?? skills/demo/memoria/", status)
        self.assertTrue((self.c / "skills/demo/memoria/nuevo.md").is_file())
        text = (self.c / "skills/demo/HANDOFF.md").read_text(encoding="utf-8")
        self.assertIn("línea mía", text)
        self.assertNotIn("<<<<<<<", text)
        self.assertNotIn("otra persona", text)
        self.assertEqual(self.git(self.c, "branch", "--list", "aporte/*"), "")
        self.assertEqual(self.remote_branches(), ["main"])

    # ---------------------------------------------------------------- dry run
    def test_dry_run_prints_steps_and_changes_nothing(self):
        self.edit(self.c)
        fake = self.as_github("dueno", "gui")
        status, head = self.status(self.c), self.head(self.c)
        rc, out, _ = self.publish("--tema", "demo-uno", "--dry-run")
        self.assertEqual(rc, 0)
        self.assertIn("[dry-run]", out)
        self.assertIn(BRANCH, out)
        self.assertIn(f"https://github.com/dueno/gui/compare/main...{BRANCH}?expand=1", out)
        self.assertIn("skills/demo/HANDOFF.md", out)
        self.assertTrue(out.strip().endswith("DRY_RUN - no se cambió nada."), out)
        self.assertEqual(self.status(self.c), status)
        self.assertEqual(self.head(self.c), head)
        self.assertEqual(self.git(self.c, "branch", "--list", "aporte/*"), "")
        self.assertEqual(self.remote_branches(), ["main"])
        self.assertEqual(self.git(self.c, "config", "--get", "remote.origin.url"), fake)

    def test_dry_run_merge_prints_merge_steps(self):
        self.edit(self.c)
        self.as_github()
        rc, out, _ = self.publish("--tema", "demo-uno", "--merge", "--dry-run")
        self.assertEqual(rc, 0)
        self.assertIn("--merge", out)
        self.assertIn("gh pr merge", out)
        self.assertIn("PUBLICADO <url>", out)
        self.assertEqual(self.remote_branches(), ["main"])

    # ---------------------------------------------------------------- GitHub flows (mock API)
    def api_env(self, mock, token=True):
        env = dict(self.env)
        env["GUI_SKILLS_API_URL"] = mock.url
        if token:
            env["GH_TOKEN"] = FAKE_TOKEN
        return env

    def test_github_url_creates_pr_through_api(self):
        self.as_github()
        self.edit(self.c)
        rc, out, err = self.run_tool("log_job.py", "--repo", forward(self.c), "--skill", "demo", "--caso", "caso-demo-01",
                                     "--hecho", "Se hizo la prueba", "--bien", "Salió bien", "--mal", "nada relevante", "--fecha", FECHA)
        self.assertEqual(rc, 0, out + err)
        with MockGitHub(self.remote) as mock:
            rc, out, err = self.publish("--tema", "demo-uno", "--mensaje", "Registro de prueba", env=self.api_env(mock))
        self.assertEqual(rc, 0, out + err)
        self.assertTrue(out.startswith("PR_CREADO https://github.com/fake/repo/pull/7"), out)
        self.assertNotIn(FAKE_TOKEN, out + err)
        post = mock.calls("POST")
        self.assertEqual(len(post), 1)
        _, path, headers, body = post[0]
        self.assertEqual(path, "/repos/fake/repo/pulls")
        self.assertEqual(headers.get("Authorization"), f"Bearer {FAKE_TOKEN}")
        self.assertEqual((body["head"], body["base"], body["title"]), (BRANCH, "main", "Registro de prueba"))
        self.assertIn("skills/demo/HANDOFF.md", body["body"])
        self.assertIn("caso-demo-01", body["body"])  # new "Registro de trabajos" entry extracted from the diff
        self.assertIn("Se hizo la prueba", body["body"])
        self.assertIn(BRANCH, self.remote_branches())
        self.assertBackOnCleanMain()

    def test_github_url_without_token_gives_compare_url(self):
        self.as_github()
        self.edit(self.c)
        rc, out, err = self.publish("--tema", "demo-uno")
        self.assertEqual(rc, 0, out + err)
        self.assertTrue(out.startswith(f"PR_MANUAL https://github.com/fake/repo/compare/main...{BRANCH}?expand=1"), out)
        self.assertIn(BRANCH, self.remote_branches())
        self.assertBackOnCleanMain()

    def test_api_rejection_falls_back_to_manual(self):
        self.as_github()
        self.edit(self.c)
        with MockGitHub(self.remote, pr_status=403) as mock:
            rc, out, err = self.publish("--tema", "demo-uno", env=self.api_env(mock))
        self.assertEqual(rc, 0, out + err)
        self.assertTrue(out.startswith("PR_MANUAL https://github.com/fake/repo/compare/"), out)
        self.assertIn("rechazó la credencial", out)
        self.assertNotIn(FAKE_TOKEN, out + err)

    def test_existing_pr_is_reused(self):
        self.as_github()
        self.edit(self.c)
        with MockGitHub(self.remote, pr_status=422, existing_pr=True) as mock:
            rc, out, err = self.publish("--tema", "demo-uno", env=self.api_env(mock))
        self.assertTrue(out.startswith("PR_CREADO https://github.com/fake/repo/pull/7"), out + err)

    def test_merge_publishes_and_cleans_up(self):
        self.as_github()
        self.edit(self.c)
        with MockGitHub(self.remote) as mock:
            rc, out, err = self.publish("--tema", "demo-uno", "--merge", env=self.api_env(mock))
        self.assertEqual(rc, 0, out + err)
        self.assertTrue(out.startswith("PUBLICADO https://github.com/fake/repo/pull/7"), out)
        self.assertNotIn(FAKE_TOKEN, out + err)
        self.assertEqual([r[0] for r in mock.requests if r[0] != "GET"], ["POST", "PUT", "DELETE"])
        self.assertBackOnCleanMain()
        self.assertEqual(self.head(self.c), self.git(self.remote, "rev-parse", "main"))  # main now has the change
        self.assertIn("línea nueva", (self.c / "skills/demo/HANDOFF.md").read_text(encoding="utf-8"))
        self.assertEqual(self.git(self.c, "branch", "--list", "aporte/*"), "")
        self.assertEqual(self.remote_branches(), ["main"])

    def test_merge_refused_keeps_pr_open(self):
        self.as_github()
        self.edit(self.c)
        with MockGitHub(self.remote, merge_status=405) as mock:
            rc, out, err = self.publish("--tema", "demo-uno", "--merge", env=self.api_env(mock))
        self.assertEqual(rc, 0, out + err)
        self.assertTrue(out.startswith("PR_CREADO https://github.com/fake/repo/pull/7"), out)
        self.assertIn("no se pudo fusionar", out)
        self.assertBackOnCleanMain()
        self.assertIn(BRANCH, self.remote_branches())

    def test_retry_creates_pr_for_pending_branch_through_api(self):
        self.as_github()
        self.edit(self.c)
        moved = self.tmp / "remote-movido.git"
        self.remote.rename(moved)
        rc, out, _ = self.publish("--tema", "demo-uno")
        self.assertTrue(out.startswith("PENDIENTE"), out)
        moved.rename(self.remote)
        with MockGitHub(self.remote) as mock:
            rc, out, err = self.publish("--reintentar", env=self.api_env(mock))
        self.assertEqual(rc, 0, out + err)
        self.assertTrue(out.startswith("PR_CREADO https://github.com/fake/repo/pull/7"), out)
        self.assertEqual(mock.calls("POST")[0][3]["head"], BRANCH)


if __name__ == "__main__":
    unittest.main()
