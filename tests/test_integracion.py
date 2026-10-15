import unittest

from base import RUTA_HISTORIA
from cargador import cargar_historia
from motor import Sesion


class TestIntegracion(unittest.TestCase):

        # I1 extendido: deshacer desde cada final tras cargar el archivo real
    def test_i1_deshacer_desde_cada_final(self):
        casos = [
            ("rescate", ["revisar", "investigar", "activar_codigo"], True),
            ("eco", ["revisar", "continuar", "activar_sin_verificar"], False),
            ("silencio", ["revisar", "continuar", "cortar"], False),
        ]
        for nombre, camino, conoce in casos:
            with self.subTest(nombre):
                sesion = Sesion(cargar_historia(RUTA_HISTORIA))
                for oid in camino:
                    self.assertTrue(sesion.elegir(oid))
                self.assertTrue(sesion.es_final)
                self.assertTrue(sesion.deshacer())
                self.assertEqual(sesion.escena_id, "E3")
                self.assertEqual(sesion.variables,
                                 {"conoce_origen": conoce,
                                  "confia_en_la_voz": False})
                self.assertFalse(sesion.es_final)
                self.assertFalse(sesion.puede_deshacer)
                # tras deshacer se puede elegir otro camino
                self.assertTrue(sesion.elegir("cortar"))
                self.assertEqual(sesion.escena_id, "E6")

if __name__ == "__main__":
    unittest.main()