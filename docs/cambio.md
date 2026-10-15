# Gestión del cambio SC01: deshacer la última decisión

## Versión de partida
- Tag: `version-inicial` (commit: [hash])
- Hora de recepción de la solicitud: [completar]
- Archivo original: `docs/solicitud_de_cambio.pdf`

## Solicitud recibida
El colectivo pide que el lector pueda deshacer su última decisión, revirtiendo
todas sus consecuencias. Reemplaza el acuerdo provisional de no implementar
retroceso (P01). Reglas: restauración exacta de escena y variables, un solo
nivel, sin retroceso al comenzar ni tras reiniciar, entrada inválida que no
altera el historial, y deshacer permitido desde E4, E5 o E6.

## Análisis de impacto
| Artefacto | Impacto | Qué cambia |
|---|---|---|
| Requisitos | Nuevos: RF12, RF13, RF14. Modificado: RF09. | Se agrega el retroceso; el reinicio elimina el historial. P01 queda resuelta. |
| Modelo de casos de uso | Afectado | Nuevo caso de uso "Deshacer decisión". |
| Modelo de clases | Afectado | `Sesion` gana el estado del historial (`_anterior`), `puede_deshacer` y `deshacer()`. |
| Modelo de secuencia | Afectado | Nueva secuencia de "deshacer"; la de "elegir" guarda la instantánea. |
| Modelo de estados | Afectado | La sesión distingue "con retroceso disponible" y "sin retroceso". |
| Diagrama de componentes | Sin cambio estructural | Los mismos componentes; cambian `motor.py` y `consola.py`. |
| Código | `src/motor.py`, `src/consola.py` | Sin cambios en `src/cargador.py` ni en los archivos JSON. |
| Pruebas | U6 nuevo; U5 e I1 extendidos | `tests/test_motor.py`, `tests/test_integracion.py`. |
| RNF | RNF01 se vuelve a ejecutar | El simulador usa deshacer. RNF02 y RNF03 no se ven afectados. |
| README | Afectado | Se añade el comando de deshacer y se quita "sin retroceso" de las limitaciones. |
| Backlog (Trello) | 5 tarjetas nuevas | Ver tablero. |

## Decisión de diseño
Instantánea de un nivel (escena y copia de variables) guardada antes de cada
elección válida. Alternativa descartada: pila de historial, por exceder el
alcance pedido (un solo nivel, sin rehacer).

## Implementación y evidencia
- Commits del cambio: [hashes]
- Versión posterior: tag `version-final`
- Pruebas: `test_u6_*` y `test_u5_reiniciar_elimina_historial` en
  `tests/test_motor.py`; `test_i1_deshacer_desde_cada_final` en
  `tests/test_integracion.py`
- Registro de ejecución: `evidencia/ultima_ejecucion.txt`