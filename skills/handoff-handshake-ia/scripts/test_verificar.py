import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from verificar import revisar, FIELDS

SKILL = Path(__file__).resolve().parents[1]

class VerificadorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.hs = '# Estado\nEstado: en curso\nFecha: 2026-11-22\nFirma: IA\nÚltimo trabajo real: IA, fecha y evidencia\nContradicciones y qué manda: ninguna conocida\n'
        self.ho = '# Ficha\n' + ''.join(x + ': dato\n' for x in FIELDS)
        self.save()

    def save(self):
        (self.root / 'HANDSHAKE.md').write_text(self.hs, encoding='utf-8')
        (self.root / 'HANDOFF.md').write_text(self.ho, encoding='utf-8')

    def levels(self, **kwargs):
        return [item['nivel'] for item in revisar(self.root, **kwargs)]

    def test_sano_con_tildes_y_ene(self):
        self.hs += 'Objetivo: diseño y revisión de documentación.\n'
        self.save()
        self.assertEqual(self.levels(), ['OK'])

    def test_tope_argumento_cli(self):
        result = subprocess.run([sys.executable, str(SKILL / 'scripts/verificar.py'), str(self.root), '--tope', '2'], capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn(b'BLOQUEA', result.stdout)

    def test_tope_marcador_y_comentarios(self):
        self.hs = '<!-- handshake-tope: 6 -->\n<!-- guía que no cuenta -->\n' + self.hs
        self.save()
        self.assertEqual(self.levels(), ['OK'])
        self.hs += 'Una línea más\n'
        self.save()
        self.assertIn('BLOQUEA', self.levels())

    def test_tope_opcion_sobrescribe_marcador(self):
        self.hs = '<!-- handshake-tope: 2 -->\n' + self.hs
        self.save()
        self.assertEqual(self.levels(tope=6), ['OK'])

    def test_fecha_iso_con_zona(self):
        self.hs = self.hs.replace('2026-11-22', '2026-11-22T21:30:00-05:00')
        self.save()
        self.assertEqual(self.levels(), ['OK'])

    def test_fecha_malformada_bloquea(self):
        self.hs = self.hs.replace('2026-11-22', '2026-11-22T21:30')
        self.save()
        self.assertIn('BLOQUEA', self.levels())

    def test_ficha_sin_ultimo_trabajo_bloquea(self):
        self.ho = self.ho.replace('Último trabajo real: dato\n', 'Último trabajo real:\n')
        self.save()
        self.assertIn('BLOQUEA', self.levels())

    def test_campos_nuevos_del_estado_ausentes_avisan(self):
        self.hs = self.hs.replace('Último trabajo real: IA, fecha y evidencia\n', '').replace('Contradicciones y qué manda: ninguna conocida\n', '')
        self.save()
        mensajes = [x['mensaje'] for x in revisar(self.root)]
        self.assertEqual(sum('Falta campo' in x for x in mensajes), 2)

    def test_estado_largo_avisa(self):
        self.hs = self.hs.replace('Estado: en curso', 'Estado: ' + 'a' * 201)
        self.save()
        self.assertTrue(any('200 caracteres' in x['mensaje'] for x in revisar(self.root)))

    def test_combinado_cli_fecha_y_tope(self):
        combined = self.root / 'combinado.md'
        combined.write_text(self.hs.replace('2026-11-22', '2026-11-22T21:30:00-05:00'), encoding='utf-8')
        (self.root / 'HANDSHAKE.md').unlink()
        (self.root / 'HANDOFF.md').unlink()
        cmd = [sys.executable, str(SKILL / 'scripts/verificar.py'), str(self.root), '--combinado', 'combinado.md']
        result = subprocess.run(cmd, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn(b'AVISA', result.stdout)
        result = subprocess.run(cmd + ['--tope', '2'], capture_output=True)
        self.assertEqual(result.returncode, 1)
        combined.write_text(self.hs.replace('2026-11-22', 'NO CONSTA'), encoding='utf-8')
        result = subprocess.run(cmd, capture_output=True)
        self.assertEqual(result.returncode, 1)

    def test_ruta_existente(self):
        (self.root / 'evidencia.md').write_text('prueba', encoding='utf-8')
        self.ho += 'Ruta: `evidencia.md`\n'
        self.save()
        self.assertEqual(self.levels(rutas=True), ['OK'])

    def test_ruta_inexistente(self):
        self.ho += 'Ruta: `no/existe.md`\n'
        self.save()
        self.assertIn('BLOQUEA', self.levels(rutas=True))

    def test_contradiccion(self):
        self.ho += 'Estado: terminado\n'
        self.save()
        self.assertIn('AVISA', self.levels())

    def test_orden_correcto_con_tilde(self):
        self.ho += 'más nuevo arriba\n### 2026-11-22\n### 2026-11-21\n'
        self.save()
        self.assertEqual(self.levels(), ['OK'])

    def test_orden_incorrecto_con_tilde(self):
        self.ho += 'más nuevo arriba\n### 2026-11-21\n### 2026-11-22\n'
        self.save()
        self.assertIn('AVISA', self.levels())

    def test_orden_incorrecto_sin_tilde(self):
        self.ho += 'mas nuevo arriba\n| 2026-11-21 |\n| 2026-11-22 |\n'
        self.save()
        self.assertIn('AVISA', self.levels())

    def test_archivos_sin_corrupcion(self):
        damaged = re.compile(r'[A-Za-zñáéíóúÑÁÉÍÓÚ]\?[a-zñáéíóú]')
        for path in SKILL.rglob('*'):
            if path.is_file() and path.suffix in {'.md', '.py'}:
                data = path.read_text(encoding='utf-8')
                self.assertNotRegex(data, damaged, str(path))
                self.assertNotIn('\ufffd', data, str(path))

    def test_campo_sin_rellenar_avisa(self):
        self.hs += 'Objetivo: NO CONSTA\nPróximo paso: NO CONSTA\n'
        self.save()
        resultados = [item for item in revisar(self.root) if item['nivel'] == 'AVISA' and 'sin rellenar' in item['mensaje']]
        self.assertEqual(len(resultados), 2)

    def test_fecha_iso_con_hora_y_zona(self):
        self.hs = self.hs.replace('Fecha: 2026-11-22', 'Fecha: 2026-11-22T22:05:00-05:00')
        self.hs += 'Objetivo: diseño\n'
        self.save()
        self.assertEqual(self.levels(), ['OK'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
