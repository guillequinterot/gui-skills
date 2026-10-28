"""Pruebas de tools/install_agente.py (unittest, solo biblioteca estándar)."""
import io
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "tools"))
import install_agente as ia  # noqa: E402


def hacer_repo(raiz):
    for n, extra in (("skill-a", {"references/r.md": "r"}), ("skill-b", {}), ("seo-content-system-web-hosted", {})):
        base = os.path.join(raiz, "skills", n)
        os.makedirs(base)
        open(os.path.join(base, "SKILL.md"), "w", encoding="utf-8").write(f"---\nname: {n}\n---\n")
        for rel, txt in extra.items():
            os.makedirs(os.path.dirname(os.path.join(base, rel)), exist_ok=True)
            open(os.path.join(base, rel), "w", encoding="utf-8").write(txt)
    os.makedirs(os.path.join(raiz, "skills", "sin-skill-md"))   # carpeta sin SKILL.md: no es una skill


def correr(*args):
    buf = io.StringIO()
    with redirect_stdout(buf):
        codigo = ia.main(list(args))
    return codigo, buf.getvalue()


class Pruebas(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp()
        self.repo = os.path.join(self.t, "repo")
        self.dest = os.path.join(self.t, "ia", "skills")
        hacer_repo(self.repo)
        self._home = os.environ.get("USERPROFILE"), os.environ.get("HOME")
        os.environ["USERPROFILE"] = os.environ["HOME"] = self.t       # los respaldos van a una carpeta temporal

    def tearDown(self):
        for k, v in zip(("USERPROFILE", "HOME"), self._home):
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(self.t, ignore_errors=True)

    def test_lista_solo_skills_instalables(self):
        self.assertEqual(ia.skills_del_repo(self.repo, False, []), ["skill-a", "skill-b"])
        self.assertIn("seo-content-system-web-hosted", ia.skills_del_repo(self.repo, True, []))

    def test_enlaza_y_es_idempotente(self):
        c, s = correr("--destino", self.dest, "--repo", self.repo)
        self.assertEqual(c, 0, s)
        self.assertIn("ENLAZADA skill-a", s)
        self.assertTrue(ia.mismo_sitio(os.path.join(self.dest, "skill-a"), os.path.join(self.repo, "skills", "skill-a")))
        c2, s2 = correr("--destino", self.dest, "--repo", self.repo)
        self.assertEqual(c2, 0)
        self.assertIn("YA_OK skill-a", s2)
        self.assertNotIn("ENLAZADA", s2)

    def test_un_cambio_en_el_repo_se_ve_por_el_enlace(self):
        correr("--destino", self.dest, "--repo", self.repo)
        open(os.path.join(self.repo, "skills", "skill-a", "nuevo.md"), "w").write("x")
        self.assertTrue(os.path.exists(os.path.join(self.dest, "skill-a", "nuevo.md")))

    def test_respalda_una_carpeta_real_antes_de_enlazar(self):
        os.makedirs(os.path.join(self.dest, "skill-a"))
        open(os.path.join(self.dest, "skill-a", "vieja.txt"), "w").write("vieja")
        c, s = correr("--destino", self.dest, "--repo", self.repo, "--skills", "skill-a")
        self.assertEqual(c, 0, s)
        self.assertIn("RESPALDADA skill-a", s)
        respaldos = [r for r, _, fs in os.walk(os.path.join(self.t, ".gui-skills")) if "vieja.txt" in fs]
        self.assertEqual(len(respaldos), 1)
        self.assertTrue(ia.mismo_sitio(os.path.join(self.dest, "skill-a"), os.path.join(self.repo, "skills", "skill-a")))

    def test_reapunta_un_enlace_a_otro_sitio(self):
        otro = os.path.join(self.t, "otro")
        os.makedirs(otro)
        os.makedirs(self.dest)
        ia.crear_enlace(otro, os.path.join(self.dest, "skill-a"))
        c, s = correr("--destino", self.dest, "--repo", self.repo, "--skills", "skill-a")
        self.assertIn("REAPUNTADA skill-a", s)
        self.assertTrue(os.path.isdir(otro))                       # la carpeta a la que apuntaba no se toca
        self.assertTrue(ia.mismo_sitio(os.path.join(self.dest, "skill-a"), os.path.join(self.repo, "skills", "skill-a")))

    def test_copiar_y_detectar_copia_desactualizada(self):
        c, s = correr("--destino", self.dest, "--repo", self.repo, "--copiar", "--skills", "skill-a")
        self.assertIn("COPIADA skill-a", s)
        self.assertFalse(ia.es_enlace(os.path.join(self.dest, "skill-a")))
        self.assertEqual(correr("--destino", self.dest, "--repo", self.repo, "--copiar", "--check", "--skills", "skill-a")[0], 0)
        open(os.path.join(self.repo, "skills", "skill-a", "SKILL.md"), "a").write("cambio")
        c2, s2 = correr("--destino", self.dest, "--repo", self.repo, "--check", "--skills", "skill-a")
        self.assertEqual(c2, 1)
        self.assertIn("DESACTUALIZADA", s2)
        c3, s3 = correr("--destino", self.dest, "--repo", self.repo, "--copiar", "--skills", "skill-a")
        self.assertEqual(c3, 0, s3)
        self.assertEqual(correr("--destino", self.dest, "--repo", self.repo, "--copiar", "--check", "--skills", "skill-a")[0], 0)

    def test_check_informa_lo_que_falta_sin_cambiar_nada(self):
        c, s = correr("--destino", self.dest, "--repo", self.repo, "--check")
        self.assertEqual(c, 1)
        self.assertIn("FALTA skill-a", s)
        self.assertFalse(os.path.exists(self.dest))

    def test_dry_run_no_cambia_nada(self):
        c, s = correr("--destino", self.dest, "--repo", self.repo, "--dry-run")
        self.assertEqual(c, 0)
        self.assertIn("DRY skill-a", s)
        self.assertFalse(os.path.exists(os.path.join(self.dest, "skill-a")))

    def test_repo_incorrecto_es_error_de_uso(self):
        c, _ = correr("--destino", self.dest, "--repo", os.path.join(self.t, "no-existe"))
        self.assertEqual(c, 2)

    def test_la_copia_no_incluye_investigacion_local(self):
        base = os.path.join(self.repo, "skills", "skill-a")
        os.makedirs(os.path.join(base, "investigacion"))
        open(os.path.join(base, "investigacion", "nota.md"), "w").write("privada")
        correr("--destino", self.dest, "--repo", self.repo, "--copiar", "--skills", "skill-a")
        self.assertFalse(os.path.exists(os.path.join(self.dest, "skill-a", "investigacion")))


if __name__ == "__main__":
    unittest.main()
