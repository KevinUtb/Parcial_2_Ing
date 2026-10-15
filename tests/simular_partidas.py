"""RNF01: partidas aleatorias sin excepciones no controladas.

Uso: python tests/simular_partidas.py
"""
import os
import random
import sys
from collections import Counter

from base import RAIZ
from cargador import cargar_historia
from motor import Sesion

HISTORIAS = ["contenido/la_ultima_transmision.json", "contenido/el_faro.json"]
PARTIDAS_POR_HISTORIA = 500
SEMILLA = 42
MAX_PASOS = 100


def simular():
    random.seed(SEMILLA)
    excepciones = bloqueos = sin_final = total = 0
    finales = Counter()

    for ruta in HISTORIAS:
        historia = cargar_historia(os.path.join(RAIZ, ruta))
        for _ in range(PARTIDAS_POR_HISTORIA):
            total += 1
            try:
                s = Sesion(historia)
                pasos = 0
                while not s.es_final and not s.bloqueada and pasos < MAX_PASOS:
                    habilitadas = s.opciones_habilitadas()
                    s.elegir(random.choice(habilitadas)["id"])
                    pasos += 1
                if s.es_final:
                    finales[(ruta, s.escena_id)] += 1
                elif s.bloqueada:
                    bloqueos += 1
                else:
                    sin_final += 1
            except Exception as e:  # noqa: BLE001
                excepciones += 1
                print(f"EXCEPCION en {ruta}: {type(e).__name__}: {e}")

    print("RNF01 - Simulacion de partidas aleatorias")
    print(f"Semilla: {SEMILLA}")
    print(f"Partidas por historia: {PARTIDAS_POR_HISTORIA} (total {total})")
    for (ruta, escena), n in sorted(finales.items()):
        print(f"  {ruta} -> {escena}: {n} partidas")
    print(f"Excepciones no controladas: {excepciones}")
    print(f"Bloqueos: {bloqueos}")
    print(f"Partidas sin terminar en {MAX_PASOS} pasos: {sin_final}")
    ok = excepciones == 0 and sin_final == 0
    print("RESULTADO:", "CUMPLE (0 excepciones)" if ok else "NO CUMPLE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(simular())