# Requisitos del motor de historias interactivas: "La última transmisión"

## Requisitos funcionales

| ID | Requisito | Criterio de aceptación | Necesidad |
|---|---|---|---|
| RF01 | El sistema carga una historia desde un archivo JSON. | Con un archivo válido, la carga devuelve una historia con escena inicial y variables. | N01 |
| RF02 | El sistema toma la escena inicial y las variables iniciales desde el archivo. | Con `la_ultima_transmision.json`, la partida inicia en E1 con `conoce_origen = falso` y `confia_en_la_voz = falso`. | N01 |
| RF03 | El sistema muestra el texto de la escena actual. | Al iniciar o avanzar, se muestra el texto de la escena activa. | N02 |
| RF04 | El sistema muestra solo las opciones habilitadas por sus condiciones. | Con `conoce_origen = falso` en E3, no aparece "Activar con código". | N02 |
| RF05 | Al elegir una opción habilitada, el sistema aplica sus efectos y avanza a su destino. | Desde E2, "Investigar archivo" lleva a E3 con `conoce_origen = verdadero`. | N03 |
| RF06 | Una opción inexistente o no habilitada no modifica el estado. | Enviar un ID no habilitado deja escena y variables iguales. | N03 |
| RF07 | El sistema conserva las variables modificadas durante la partida. | Tras un efecto, la siguiente elección evalúa el valor actualizado. | N04 |
| RF08 | El sistema identifica los finales y termina la partida al alcanzarlos. | Al llegar a E4, E5 o E6, la sesión queda terminada sin opciones. | N05 |
| RF09 | El sistema reinicia la partida restaurando escena y variables iniciales. | Tras un final y un reinicio, la sesión vuelve a E1 con variables en falso. | N05 |
| RF10 | El sistema rechaza un archivo inválido e indica causa y campo o ID. | Una copia con destino `E99` falla con un mensaje que nombra `E99`. | N06 |
| RF11 | El sistema informa cuando una escena no final no tiene opciones habilitadas. | Se muestra el bloqueo y la opción de reiniciar. | N06 |

## Requisitos no funcionales

| ID | Atributo | Medida | Meta | Procedimiento de verificación | Evidencia |
|---|---|---|---|---|---|
| RNF01 | Confiabilidad | Número de excepciones no controladas durante partidas simuladas | 0 en 1 000 partidas | Script `tests/simular_partidas.py` que juega 1 000 partidas aleatorias con `random.seed(42)` sobre la historia de referencia y la segunda historia. Cada elección se toma entre las opciones habilitadas. Cuenta las excepciones no capturadas y los bloqueos no reportados. | `evidencia/rnf01.txt` con la salida del script |
| RNF02 | Claridad de errores | Porcentaje de errores de contenido que generan mensaje con causa y campo o ID | 100 % de las 9 categorías | Pruebas parametrizadas de U4 con un caso por categoría (archivo ilegible, campo ausente, inicio inexistente, ID de escena duplicado, ID de opción duplicado, destino inexistente, variable no declarada, valor no booleano, opciones incompatibles con el final). Cada prueba verifica que el mensaje contenga la causa y el identificador. | Registro de la última ejecución de `pytest` o `unittest` en `evidencia/rnf02.txt` |
| RNF03 | Modificabilidad | Líneas de código del motor modificadas para cargar la segunda historia | 0 líneas | Etiquetar el commit de la versión final (`git tag version-final`). Añadir la segunda historia en `contenido/` y ejecutar `git diff --stat version-final -- src/`. El resultado debe estar vacío. | Salida de `git diff --stat` en `evidencia/rnf03.txt` |