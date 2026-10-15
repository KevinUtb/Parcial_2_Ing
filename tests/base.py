import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))
RUTA_HISTORIA = os.path.join(RAIZ, "contenido", "la_ultima_transmision.json")


def historia_base():
    """Devuelve una copia nueva de la historia real, lista para modificar."""
    with open(RUTA_HISTORIA, encoding="utf-8-sig") as f:
        return json.load(f)


def jugar(sesion, *ids_opciones):
    """Elige opciones en orden; falla si alguna no se puede ejecutar."""
    for oid in ids_opciones:
        assert sesion.elegir(oid), f"No se pudo elegir '{oid}' en {sesion.escena_id}"