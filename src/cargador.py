"""Carga y validación de historias interactivas (RF01, RF02, RF10)."""
import json


class ErrorContenido(Exception):
    """La historia no es válida. `errores` contiene un mensaje por problema."""

    def __init__(self, errores):
        self.errores = list(errores)
        super().__init__("\n".join(self.errores))


def cargar_historia(ruta):
    """Lee un archivo JSON, lo valida y devuelve la historia como dict."""
    try:
        with open(ruta, encoding="utf-8-sig") as f:
            datos = json.load(f)
    except FileNotFoundError:
        raise ErrorContenido([f"Archivo no encontrado: '{ruta}'."])
    except json.JSONDecodeError as e:
        raise ErrorContenido(
            [f"Archivo ilegible, JSON mal formado en '{ruta}': "
             f"{e.msg} (línea {e.lineno}, columna {e.colno})."])
    except (OSError, UnicodeDecodeError) as e:
        raise ErrorContenido([f"No se pudo leer '{ruta}': {e}."])

    errores = validar_historia(datos)
    if errores:
        raise ErrorContenido(errores)
    return datos


def _es_bool_map(valor):
    return isinstance(valor, dict) and all(isinstance(k, str) for k in valor)


def validar_historia(datos):
    """Devuelve una lista de mensajes de error; vacía si la historia es válida."""
    errores = []

    if not isinstance(datos, dict):
        return ["Estructura incorrecta: la raíz del archivo debe ser un objeto."]

    # Campos obligatorios de la historia
    tipos = {"titulo": str, "inicio": str, "variables": dict, "escenas": list}
    for campo, tipo in tipos.items():
        if campo not in datos:
            errores.append(f"Campo obligatorio ausente: '{campo}'.")
        elif not isinstance(datos[campo], tipo):
            errores.append(f"Campo '{campo}' con tipo incorrecto: "
                           f"se esperaba {tipo.__name__}.")
    if errores:
        return errores

    variables = datos["variables"]
    for nombre, valor in variables.items():
        if not isinstance(valor, bool):
            errores.append(f"Valor no booleano en variable inicial '{nombre}'.")

    # Escenas: estructura e IDs únicos
    ids_escenas = set()
    escenas_validas = []
    for i, esc in enumerate(datos["escenas"]):
        if not isinstance(esc, dict):
            errores.append(f"Escena en posición {i}: estructura incorrecta.")
            continue
        faltan = [c for c in ("id", "texto", "final", "opciones") if c not in esc]
        eid = esc.get("id", f"#{i}")
        for c in faltan:
            errores.append(f"Escena '{eid}': campo obligatorio ausente '{c}'.")
        if faltan:
            continue
        if not isinstance(esc["id"], str):
            errores.append(f"Escena en posición {i}: 'id' debe ser texto.")
            continue
        if not isinstance(esc["final"], bool):
            errores.append(f"Escena '{eid}': 'final' debe ser booleano.")
            continue
        if not isinstance(esc["opciones"], list):
            errores.append(f"Escena '{eid}': 'opciones' debe ser una lista.")
            continue
        if eid in ids_escenas:
            errores.append(f"ID de escena duplicado: '{eid}'.")
        ids_escenas.add(eid)
        escenas_validas.append(esc)

    if datos["inicio"] not in ids_escenas:
        errores.append(f"Escena inicial inexistente: '{datos['inicio']}'.")

    # Opciones, destinos, condiciones y efectos
    for esc in escenas_validas:
        eid = esc["id"]
        if esc["final"] and esc["opciones"]:
            errores.append(f"Escena final '{eid}' debe tener cero opciones "
                           f"(tiene {len(esc['opciones'])}).")
        if not esc["final"] and not esc["opciones"]:
            errores.append(f"Escena no final '{eid}' debe tener al menos una opción.")

        ids_opciones = set()
        for j, op in enumerate(esc["opciones"]):
            if not isinstance(op, dict):
                errores.append(f"Escena '{eid}', opción en posición {j}: "
                               f"estructura incorrecta.")
                continue
            oid = op.get("id", f"#{j}")
            ref = f"Escena '{eid}', opción '{oid}'"
            faltan = [c for c in ("id", "texto", "destino", "condiciones", "efectos")
                      if c not in op]
            for c in faltan:
                errores.append(f"{ref}: campo obligatorio ausente '{c}'.")
            if faltan:
                continue
            if oid in ids_opciones:
                errores.append(f"ID de opción duplicado en escena '{eid}': '{oid}'.")
            ids_opciones.add(oid)
            if op["destino"] not in ids_escenas:
                errores.append(f"{ref}: destino inexistente '{op['destino']}'.")
            for campo in ("condiciones", "efectos"):
                mapa = op[campo]
                if not _es_bool_map(mapa):
                    errores.append(f"{ref}: '{campo}' debe ser un mapa.")
                    continue
                for var, valor in mapa.items():
                    if var not in variables:
                        errores.append(f"{ref}: variable no declarada '{var}' "
                                       f"en '{campo}'.")
                    if not isinstance(valor, bool):
                        errores.append(f"{ref}: valor no booleano para '{var}' "
                                       f"en '{campo}'.")
    return errores