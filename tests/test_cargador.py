import copy
import json
import os
import tempfile
import unittest

from base import historia_base
from cargador import cargar_historia, validar_historia, ErrorContenido


def esc(d, eid):
    return next(e for e in d["escenas"] if e["id"] == eid)


def op(d, eid, oid):
    return next(o for o in esc(d, eid)["opciones"] if o["id"] == oid)


def sin_titulo(d):
    del d["titulo"]

def opcion_sin_destino(d):
    del op(d, "E1", "revisar")["destino"]

def inicio_inexistente(d):
    d["inicio"] = "E99"

def escena_duplicada(d):
    d["escenas"].append(copy.deepcopy(esc(d, "E1")))

def opcion_duplicada(d):
    esc(d, "E2")["opciones"].append(copy.deepcopy(op(d, "E2", "investigar")))

def destino_inexistente(d):
    op(d, "E3", "cortar")["destino"] = "E99"

def variable_no_declarada(d):
    op(d, "E1", "revisar")["efectos"]["variable_fantasma"] = True

def valor_no_booleano(d):
    op(d, "E2", "investigar")["efectos"]["conoce_origen"] = "si"

def final_con_opciones(d):
    esc(d, "E4")["opciones"].append(
        {"id": "extra", "texto": "x", "destino": "E1",
         "condiciones": {}, "efectos": {}})

def no_final_sin_opciones(d):
    esc(d, "E1")["opciones"] = []


# (nombre, función que daña la historia, fragmentos que debe contener UN mensaje)
CASOS_ERROR = [
    ("campo ausente", sin_titulo, ["ausente", "titulo"]),
    ("campo ausente en opcion", opcion_sin_destino, ["ausente", "destino"]),
    ("inicio inexistente", inicio_inexistente, ["inexistente", "E99"]),
    ("escena duplicada", escena_duplicada, ["duplicado", "E1"]),
    ("opcion duplicada", opcion_duplicada, ["duplicado", "investigar"]),
    ("destino inexistente", destino_inexistente, ["destino inexistente", "E99"]),
    ("variable no declarada", variable_no_declarada,
     ["no declarada", "variable_fantasma"]),
    ("valor no booleano", valor_no_booleano, ["no booleano", "conoce_origen"]),
    ("final con opciones", final_con_opciones, ["E4", "cero opciones"]),
    ("no final sin opciones", no_final_sin_opciones, ["E1", "al menos una"]),
]


class TestCargador(unittest.TestCase):

    def test_historia_valida_no_tiene_errores(self):
        self.assertEqual(validar_historia(historia_base()), [])

    # U4: errores de contenido, un caso por variante
    def test_u4_errores_de_contenido(self):
        for nombre, danar, fragmentos in CASOS_ERROR:
            with self.subTest(nombre):
                datos = historia_base()
                danar(datos)
                errores = validar_historia(datos)
                self.assertTrue(errores, "debía reportar al menos un error")
                self.assertTrue(
                    any(all(f in m for f in fragmentos) for m in errores),
                    f"ningún mensaje contiene {fragmentos}: {errores}")

    def test_u4_estructura_incorrecta(self):
        errores = validar_historia([])
        self.assertTrue(any("Estructura incorrecta" in m for m in errores))

    def _cargar_texto(self, texto, encoding="utf-8"):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "historia.json")
            with open(ruta, "w", encoding=encoding) as f:
                f.write(texto)
            return cargar_historia(ruta)

    def test_u4_archivo_ilegible(self):
        with self.assertRaises(ErrorContenido) as cm:
            self._cargar_texto("{ esto no es json")
        self.assertIn("ilegible", cm.exception.errores[0])

    def test_u4_archivo_inexistente(self):
        with self.assertRaises(ErrorContenido) as cm:
            cargar_historia("no_existe.json")
        self.assertIn("no encontrado", cm.exception.errores[0])

    # CA03: destino E99 rechaza la carga y no devuelve sesión jugable
    def test_ca03_destino_inexistente_rechaza_carga(self):
        datos = historia_base()
        destino_inexistente(datos)
        with self.assertRaises(ErrorContenido) as cm:
            self._cargar_texto(json.dumps(datos, ensure_ascii=False))
        self.assertTrue(any("E99" in m for m in cm.exception.errores))

    # Defecto encontrado: JSON guardado con BOM por editores de Windows
    def test_archivo_con_bom_se_carga(self):
        datos = historia_base()
        historia = self._cargar_texto(json.dumps(datos, ensure_ascii=False),
                                      encoding="utf-8-sig")
        self.assertEqual(historia["inicio"], "E1")


if __name__ == "__main__":
    unittest.main()