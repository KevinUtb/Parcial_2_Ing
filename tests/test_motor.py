import unittest

from base import historia_base, jugar
from motor import Sesion


def ids_habilitados(sesion):
    return {o["id"] for o in sesion.opciones_habilitadas()}


def instantanea(sesion):
    return sesion.escena_id, dict(sesion.variables)


class TestMotor(unittest.TestCase):

    # U1: condiciones cumplidas y no cumplidas
    def test_u1_condiciones(self):
        casos = [
            ("sin condiciones", [], {"revisar"}),
            ("con origen", ["revisar", "investigar"], {"activar_codigo", "cortar"}),
            ("sin origen", ["revisar", "continuar"], {"activar_sin_verificar", "cortar"}),
        ]
        for nombre, camino, esperado in casos:
            with self.subTest(nombre):
                s = Sesion(historia_base())
                jugar(s, *camino)
                self.assertEqual(ids_habilitados(s), esperado)

    # D01: en E3 siempre se ven exactamente dos opciones
    def test_e3_siempre_dos_opciones(self):
        for camino in (["revisar", "investigar"], ["revisar", "continuar"]):
            with self.subTest(camino):
                s = Sesion(historia_base())
                jugar(s, *camino)
                self.assertEqual(s.escena_id, "E3")
                self.assertEqual(len(s.opciones_habilitadas()), 2)

    # U2: una elección válida aplica efectos y avanza al destino
    def test_u2_eleccion_valida(self):
        casos = [
            # (camino, escena esperada, variables esperadas)
            (["revisar"], "E2",
             {"conoce_origen": False, "confia_en_la_voz": False}),
            (["revisar", "investigar"], "E3",
             {"conoce_origen": True, "confia_en_la_voz": False}),
            (["revisar", "continuar"], "E3",
             {"conoce_origen": False, "confia_en_la_voz": False}),
            (["revisar", "investigar", "activar_codigo"], "E4",
             {"conoce_origen": True, "confia_en_la_voz": True}),
            (["revisar", "continuar", "cortar"], "E6",
             {"conoce_origen": False, "confia_en_la_voz": False}),
        ]
        for camino, escena, variables in casos:
            with self.subTest(camino):
                s = Sesion(historia_base())
                jugar(s, *camino)
                self.assertEqual(s.escena_id, escena)
                self.assertEqual(s.variables, variables)

    # U3: opción inexistente o no habilitada deja intacto el estado
    def test_u3_opcion_invalida_no_cambia_estado(self):
        casos = [
            ("inexistente", [], "no_existe"),
            ("de otra escena", [], "investigar"),
            ("no habilitada (CA02)", ["revisar", "continuar"], "activar_codigo"),
            ("no habilitada inversa", ["revisar", "investigar"], "activar_sin_verificar"),
        ]
        for nombre, camino, opcion in casos:
            with self.subTest(nombre):
                s = Sesion(historia_base())
                jugar(s, *camino)
                antes = instantanea(s)
                self.assertFalse(s.elegir(opcion))
                self.assertEqual(instantanea(s), antes)

    # U5: reiniciar restaura escena y variables iniciales
    def test_u5_reiniciar(self):
        s = Sesion(historia_base())
        jugar(s, "revisar", "investigar", "activar_codigo")
        self.assertTrue(s.es_final)
        s.reiniciar()
        self.assertEqual(s.escena_id, "E1")
        self.assertEqual(s.variables,
                         {"conoce_origen": False, "confia_en_la_voz": False})
        self.assertFalse(s.es_final)

    # RF11: escena no final sin opciones habilitadas
    def test_bloqueo_en_escena_no_final(self):
        historia = {
            "titulo": "Bloqueo", "inicio": "A", "variables": {"x": False},
            "escenas": [
                {"id": "A", "texto": "a", "final": False, "opciones": [
                    {"id": "ir", "texto": "ir", "destino": "B",
                     "condiciones": {"x": True}, "efectos": {}}]},
                {"id": "B", "texto": "b", "final": True, "opciones": []},
            ],
        }
        s = Sesion(historia)
        self.assertTrue(s.bloqueada)
        self.assertEqual(s.opciones_habilitadas(), [])
        self.assertFalse(s.elegir("ir"))
        s.reiniciar()
        self.assertEqual(s.escena_id, "A")


if __name__ == "__main__":
    unittest.main()