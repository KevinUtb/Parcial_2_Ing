"""Interfaz de consola. Uso: python src/consola.py [ruta_historia.json]"""
import sys

from cargador import cargar_historia, ErrorContenido
from motor import Sesion

RUTA_POR_DEFECTO = "contenido/la_ultima_transmision.json"


def _preguntar(texto):
    try:
        return input(texto).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def jugar(sesion):
    while True:
        print(f"\n{sesion.escena['texto']}")

        if sesion.es_final or sesion.bloqueada:
            print("\n--- FIN DE LA PARTIDA ---" if sesion.es_final
                  else "\n--- Bloqueo: no hay opciones disponibles en esta escena. ---")
            resp = _preguntar("¿Jugar de nuevo? (s/n): ")
            if resp and resp.lower() == "s":
                sesion.reiniciar()
                continue
            return

        opciones = sesion.opciones_habilitadas()
        for n, op in enumerate(opciones, start=1):
            print(f"  {n}. {op['texto']}")
        resp = _preguntar("Elige una opción: ")
        if resp is None:
            return
        if resp.isdigit() and 1 <= int(resp) <= len(opciones):
            sesion.elegir(opciones[int(resp) - 1]["id"])
        else:
            print("Opción no válida. Intenta de nuevo.")


def main(argv):
    ruta = argv[1] if len(argv) > 1 else RUTA_POR_DEFECTO
    try:
        historia = cargar_historia(ruta)
    except ErrorContenido as e:
        print(f"No se puede iniciar: la historia tiene {len(e.errores)} error(es):")
        for msg in e.errores:
            print(f"  - {msg}")
        return 1
    print(f"=== {historia['titulo']} ===")
    jugar(Sesion(historia))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))