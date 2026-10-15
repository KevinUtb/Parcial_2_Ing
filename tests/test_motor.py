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

        # U6: deshacer restaura escena y variables y consume el retroceso
    def test_u6_deshacer_restaura_y_consume(self):
        casos = [
            ("desde E2 tras investigar", ["revisar", "investigar"], "E2",
             {"conoce_origen": False, "confia_en_la_voz": False}),
            ("desde E2 tras continuar", ["revisar", "continuar"], "E2",
             {"conoce_origen": False, "confia_en_la_voz": False}),
            ("tras la primera elección", ["revisar"], "E1",
             {"conoce_origen": False, "confia_en_la_voz": False}),
            ("desde el final E4", ["revisar", "investigar", "activar_codigo"], "E3",
             {"conoce_origen": True, "confia_en_la_voz": False}),
            ("desde el final E5",
             ["revisar", "continuar", "activar_sin_verificar"], "E3",
             {"conoce_origen": False, "confia_en_la_voz": False}),
            ("desde el final E6", ["revisar", "investigar", "cortar"], "E3",
             {"conoce_origen": True, "confia_en_la_voz": False}),
        ]
        for nombre, camino, escena, variables in casos:
            with self.subTest(nombre):
                s = Sesion(historia_base())
                jugar(s, *camino)
                self.assertTrue(s.puede_deshacer)
                self.assertTrue(s.deshacer())
                self.assertEqual(s.escena_id, escena)
                self.assertEqual(s.variables, variables)
                # consume la posibilidad de retroceder
                self.assertFalse(s.puede_deshacer)
                self.assertFalse(s.deshacer())
                self.assertEqual(instantanea(s), (escena, variables))

    def test_u6_sin_retroceso_al_comenzar(self):
        s = Sesion(historia_base())
        self.assertFalse(s.puede_deshacer)
        antes = instantanea(s)
        self.assertFalse(s.deshacer())
        self.assertEqual(instantanea(s), antes)

    def test_u6_entrada_invalida_preserva_historial(self):
        invalidas = ["no_existe", "activar_sin_verificar", "revisar"]
        for oid in invalidas:
            with self.subTest(oid):
                s = Sesion(historia_base())
                jugar(s, "revisar", "investigar")
                antes = instantanea(s)
                self.assertFalse(s.elegir(oid))
                self.assertEqual(instantanea(s), antes)
                self.assertTrue(s.puede_deshacer)
                self.assertTrue(s.deshacer())
                self.assertEqual(s.escena_id, "E2")
                self.assertEqual(s.variables["conoce_origen"], False)

    def test_u6_nueva_eleccion_rehabilita_retroceso(self):
        s = Sesion(historia_base())
        jugar(s, "revisar", "investigar")
        self.assertTrue(s.deshacer())
        self.assertFalse(s.puede_deshacer)
        # ejemplo de la solicitud: continuar sin investigar
        jugar(s, "continuar")
        self.assertEqual(s.escena_id, "E3")
        self.assertEqual(ids_habilitados(s), {"activar_sin_verificar", "cortar"})
        self.assertTrue(s.puede_deshacer)
        self.assertTrue(s.deshacer())
        self.assertEqual(s.escena_id, "E2")

    # U5 extendido: reiniciar elimina el historial
    def test_u5_reiniciar_elimina_historial(self):
        caminos = [
            ("tras una elección", ["revisar"]),
            ("tras un final", ["revisar", "investigar", "activar_codigo"]),
            ("tras deshacer", ["revisar", "investigar"]),
        ]
        for nombre, camino in caminos:
            with self.subTest(nombre):
                s = Sesion(historia_base())
                jugar(s, *camino)
                if nombre == "tras deshacer":
                    s.deshacer()
                s.reiniciar()
                self.assertEqual(s.escena_id, "E1")
                self.assertFalse(s.puede_deshacer)
                self.assertFalse(s.deshacer())
                self.assertEqual(s.escena_id, "E1")
                
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