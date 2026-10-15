import os
import unittest

from base import RAIZ, RUTA_HISTORIA
from cargador import cargar_historia
from motor import Sesion

RUTA_FARO = os.path.join(RAIZ, "contenido", "el_faro.json")


def ids_habilitados(sesion):
    return {o["id"] for o in sesion.opciones_habilitadas()}


class TestSegundaHistoria(unittest.TestCase):

    def test_carga_valida_sin_errores(self):
        historia = cargar_historia(RUTA_FARO)
        self.assertEqual(historia["inicio"], "F1")

    def test_condicion_cambia_las_opciones(self):
        casos = [
            ("con linterna", "tomar_linterna", {"subir_con_luz"}),
            ("sin linterna", "entrar_sin_linterna", {"subir_a_oscuras"}),
        ]
        for nombre, eleccion, esperado in casos:
            with self.subTest(nombre):
                s = Sesion(cargar_historia(RUTA_FARO))
                self.assertTrue(s.elegir(eleccion))
                self.assertEqual(s.escena_id, "F2")
                self.assertEqual(ids_habilitados(s), esperado)

    def test_finales(self):
        casos = [
            ("con linterna", ["tomar_linterna", "subir_con_luz"], "F3"),
            ("sin linterna", ["entrar_sin_linterna", "subir_a_oscuras"], "F4"),
        ]
        for nombre, camino, final in casos:
            with self.subTest(nombre):
                s = Sesion(cargar_historia(RUTA_FARO))
                for oid in camino:
                    self.assertTrue(s.elegir(oid))
                self.assertEqual(s.escena_id, final)
                self.assertTrue(s.es_final)

    def test_motor_no_contiene_datos_de_las_historias(self):
        """RNF03: el motor no conoce IDs ni variables de ninguna historia."""
        with open(os.path.join(RAIZ, "src", "motor.py"), encoding="utf-8") as f:
            codigo = f.read()
        for ruta in (RUTA_HISTORIA, RUTA_FARO):
            historia = cargar_historia(ruta)
            nombres = [e["id"] for e in historia["escenas"]]
            nombres += list(historia["variables"])
            for nombre in nombres:
                with self.subTest(nombre):
                    self.assertNotIn(f'"{nombre}"', codigo)
                    self.assertNotIn(f"'{nombre}'", codigo)


if __name__ == "__main__":
    unittest.main()