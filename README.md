# La última transmisión: motor de historias interactivas

Parcial práctico de Ingeniería de Software (UTB). Un motor de consola que lee historias desde archivos JSON, muestra solo las opciones compatibles con lo ocurrido y detecta errores de contenido antes de jugar.

## Integrantes
- Valery Georgina Aurela Perez
- Kevin Hernando Acuña Luna 

## Versiones requeridas
- Python 3 (probado con 3.12.3).
- Sin bibliotecas externas: solo `json` y `unittest` de la biblioteca estándar. No hay nada que instalar.

## Instalación
```
git clone <URL del repositorio>
cd Parcial_2_Ing
```
O descomprima el ZIP y entre a la carpeta. Todos los comandos se ejecutan desde la raíz del repositorio.

## Ejecución
```
python src/consola.py
python src/consola.py contenido/<otra_historia>.json
```
Sin argumento se carga `contenido/la_ultima_transmision.json`. Para cargar la segunda historia, con el mismo motor y sin editar `src/`:
```
python src/consola.py contenido/el_faro.json
```
En cada escena se escribe el número de la opción y Enter. Al llegar a un final (o a un bloqueo) se pregunta `¿Jugar de nuevo (s), deshacer la última decisión (d) o salir (n)?` cuando hay algo que deshacer, o `¿Jugar de nuevo? (s/n)` si no lo hay; `s` reinicia la partida.

Si la historia tiene errores, el programa no inicia: imprime cuántos errores hay, una línea por cada uno, y termina con código 1.

## Deshacer la última decisión (SC01)
- En una escena jugable, si hay algo que deshacer, el menú muestra `0. Deshacer la última decisión`; se escribe `0` y Enter.
- Desde un final (E4, E5 o E6) o un bloqueo se escribe `d` en la pregunta de fin de partida. En la historia de referencia se regresa a E3 con las variables que tenía antes de esa elección.
- Deshacer restaura la escena y todas las variables anteriores a la última elección válida.
- Es de un solo nivel: después de deshacer no se puede deshacer otra vez hasta hacer una nueva elección válida. No hay rehacer.
- Al comenzar una partida y después de reiniciar no hay retroceso disponible (la opción `0` no aparece).
- Una opción inexistente o no habilitada no modifica la partida ni el historial de la última elección válida.

## Pruebas
```
python -m unittest discover -s tests -v
```
El registro de la última ejecución está en `evidencia/ultima_ejecucion.txt` (23 pruebas, todas OK).

| Archivo | Cubre |
|---|---|
| `tests/test_motor.py` | U1, U2, U3, U5 (incluye que reiniciar elimina el historial), U6 (deshacer restaura y consume el retroceso, entrada inválida conserva el historial, una nueva elección lo rehabilita), D01 (E3 siempre con dos opciones) y bloqueo (RF11) |
| `tests/test_cargador.py` | U4: una variante por categoría de error, archivo ilegible o inexistente, CA03 y archivo con BOM |
| `tests/test_integracion.py` | I1: archivo real y motor hasta alcanzar los tres finales, y deshacer desde cada final |
| `tests/test_segunda_historia.py` | Segunda historia `contenido/el_faro.json`: carga, condición que cambia las opciones, finales y que `src/motor.py` no contiene IDs ni variables de ninguna historia (RNF03) |

Verificación de RNF01 (1 000 partidas aleatorias, semilla 42, con deshacer incluido en la simulación):
```
python tests/simular_partidas.py
```

## Formato de contenido
Se usa el contrato JSON de la guía sin adaptaciones.

```json
{
  "titulo": "texto",
  "inicio": "E1",
  "variables": {"conoce_origen": false, "confia_en_la_voz": false},
  "escenas": [
    {"id": "E2", "texto": "texto visible", "final": false,
     "opciones": [
       {"id": "investigar", "texto": "Investigar archivo", "destino": "E3",
        "condiciones": {}, "efectos": {"conoce_origen": true}}
     ]}
  ]
}
```

- `inicio` es el ID de la escena donde empieza la partida; `variables` son los valores booleanos iniciales.
- Una escena final lleva `"final": true` y `"opciones": []`. Una no final necesita al menos una opción.
- `condiciones` es un mapa `variable: true/false`. Vacío significa que la opción siempre aparece; si no, deben cumplirse todas.
- `efectos` es un mapa `variable: true/false` que se asigna al elegir. Vacío deja las variables igual.
- Toda variable usada en `condiciones` o `efectos` debe estar declarada en `variables`, y todo valor debe ser `true` o `false`.
- Los IDs de escena son únicos en la historia; los IDs de opción son únicos dentro de su escena; todo `destino` debe ser un ID de escena existente.

### Errores que detecta la carga
Archivo inexistente o ilegible (JSON mal formado), estructura incorrecta, campo obligatorio ausente o de tipo incorrecto, escena inicial inexistente, ID de escena duplicado, ID de opción duplicado, destino inexistente, variable no declarada, valor no booleano, escena final con opciones y escena no final sin opciones. Cada mensaje indica la causa y el ID o campo involucrado.

## Rutas para demostrar cada final
Con la historia de referencia, los números que se escriben en la consola son:

| Final | Camino de opciones | Entradas |
|---|---|---|
| E4 Rescate | `revisar`, `investigar`, `activar_codigo` | `1`, `1`, `1` |
| E5 El eco | `revisar`, `continuar`, `activar_sin_verificar` | `1`, `2`, `1` |
| E6 Silencio | `revisar`, `continuar`, `cortar` | `1`, `2`, `2` |

En la tercera escena (E3) las opciones cambian según lo investigado: con `conoce_origen = true` se ofrece «Activar con código»; con `false`, «Activar sin verificar». «Cortar comunicación» aparece siempre.

Para demostrar deshacer (SC01) con la historia de referencia:

| Qué se demuestra | Entradas | Resultado |
|---|---|---|
| Deshacer en mitad de la historia | `1`, `1`, `0`, `2` | Tras `1`, `1` se llega a E3 con `conoce_origen = true`; `0` regresa a E2 con `conoce_origen = false` (ya no aparece la opción `0`); `2` («Continuar sin investigar») lleva a E3, que ofrece «Activar sin verificar» y «Cortar comunicación». |
| Deshacer desde un final | `1`, `1`, `1`, `d` | Tras llegar a E4, `d` regresa a E3 con `conoce_origen = true`, sin retroceso disponible. |

Segunda historia (`python src/consola.py contenido/el_faro.json`):

| Final | Camino de opciones | Entradas |
|---|---|---|
| F3 | `tomar_linterna`, `subir_con_luz` | `1`, `1` |
| F4 | `entrar_sin_linterna`, `subir_a_oscuras` | `2`, `1` |

En F2 la opción depende de `tiene_linterna`: con `true` solo se ofrece «Subir iluminando los peldaños»; con `false`, solo «Subir a tientas».

## Estructura del repositorio
```
src/cargador.py      Lectura y validación del JSON; ErrorContenido
src/motor.py         Sesion: estado de la partida, condiciones, efectos, finales, bloqueo, reinicio y retroceso de un nivel
src/consola.py       Interfaz de consola (incluye deshacer)
contenido/           Historias en JSON: la_ultima_transmision.json (referencia) y el_faro.json (segunda historia)
tests/               Pruebas automatizadas (unittest)
docs/requisitos.md   RF01 a RF14, RNF, preguntas, supuestos y defectos
docs/cambio.md       Solicitud de cambio SC01 (deshacer): impacto, decisión de diseño y evidencia
docs/modelos/        Diagramas Mermaid (.mmd): contexto, casos de uso, clases, secuencia, estados, componentes
docs/decisiones_arquitectura.md   AD-01 y AD-02
evidencia/           Resultados de ejecución
```
Los archivos `.mmd` se visualizan pegándolos en <https://mermaid.live> o con la extensión de Mermaid de VS Code.

## Limitaciones conocidas
- El retroceso es de un solo nivel y no hay rehacer: solo se puede deshacer la última elección válida (SC01, `docs/cambio.md`). Reemplaza el acuerdo provisional de P01 en `docs/requisitos.md`.
- No hay guardado entre ejecuciones; cada ejecución parte de cero.
- La validación se detiene en los campos de primer nivel: si falta `titulo`, `inicio`, `variables` o `escenas`, o tienen un tipo incorrecto, solo se informan esos errores y no los de las escenas.
- Defecto pendiente: un `destino` o un `id` de opción que sea una lista (no texto) provoca un `TypeError` en vez de un `ErrorContenido` controlado.
- No se verifica que todos los finales sean alcanzables ni que no existan bloqueos posibles; el bloqueo solo se informa durante la partida.
- Pendiente: `evidencia/rnf02.txt` no existe y `evidencia/rnf03.txt` está vacío; ambos los cita `docs/requisitos.md`. `evidencia/rnf01.txt` sí existe.

## Herramientas de apoyo
[Completar: bibliotecas (solo estándar de Python), fragmentos reutilizados y herramientas de IA usadas, para qué sirvieron y cómo se verificó el resultado.]
