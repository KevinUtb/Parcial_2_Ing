import unittest

from base import RUTA_HISTORIA
from cargador import cargar_historia
from motor import Sesion


class TestIntegracion(unittest.TestCase):

    # I1: archivo real + motor, desde la carga hasta alcanzar cada final
    def test_i1_tres_finales_desde_archivo_real(self):
        caminos = [
            ("rescate", ["revisar", "investigar", "activar_codigo"], "E4"),
            ("eco", ["revisar", "continuar", "activar_sin_verificar"], "E5"),
            ("silencio", ["revisar", "continuar", "cortar"], "E6"),
        ]
        for nombre, camino, final in caminos:
            with self.subTest(nombre):
                sesion = Sesion(cargar_historia(RUTA_HISTORIA))
                self.assertEqual(sesion.escena_id, "E1")
                for oid in camino:
                    self.assertIn(oid, [o["id"] for o in sesion.opciones_habilitadas()])
                    self.assertTrue(sesion.elegir(oid))
                self.assertEqual(sesion.escena_id, final)
                self.assertTrue(sesion.es_final)
                self.assertEqual(sesion.opciones_habilitadas(), [])


if __name__ == "__main__":
    unittest.main()