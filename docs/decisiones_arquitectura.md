# Decisiones de arquitectura

Diagrama de referencia: `docs/modelos/06_componentes.mmd`. Requisitos citados: `docs/requisitos.md`.

## AD-01. El contenido de las historias vive en archivos JSON, fuera del código

**Contexto.** La escritora principal quiere agregar escenas y cambiar decisiones sin pedir que modifiquen el programa (N01). La guía exige que el motor evalúe condiciones y efectos desde los datos y que una segunda historia funcione sin editar el motor (RNF03). Además, el proyecto se limita a la biblioteca estándar de Python.

**Alternativas.**
1. Historias escritas como estructuras de Python dentro del código. Descartada: cada cambio de contenido exigiría editar código.
2. YAML. Descartada: Python no lo trae en su biblioteca estándar, y la restricción del proyecto es usar solo `json` y `unittest`.
3. Un lenguaje de expresiones o DSL propio. Descartada: la guía lo deja fuera de alcance (solo igualdades booleanas y asignaciones).

**Decisión.** JSON con el contrato de la guía (`titulo`, `inicio`, `variables`, `escenas`; cada escena con `id`, `texto`, `final`, `opciones`; cada opción con `id`, `texto`, `destino`, `condiciones`, `efectos`). `cargador.py` lo lee con `json` y `motor.py` solo recibe el diccionario resultante.

**Consecuencias.**
- (+) Agregar o cambiar una historia no toca `src/` (RNF03). `Sesion` no contiene IDs como E1 o E2.
- (+) El contenido se prueba con datos reales (I1) y se daña a propósito en las pruebas de U4.
- (−) JSON no admite comentarios y es sensible a comas y comillas; por eso la validación debe dar mensajes claros (AD-02).
- (−) Los editores de Windows pueden guardar el archivo con BOM; el cargador abre con `utf-8-sig` y hay una prueba (`test_archivo_con_bom_se_carga`).

## AD-02. Validar todo el contenido al cargar y devolver los errores juntos

**Contexto.** La coordinadora necesita saber qué corregir y el lector no debe ver un cierre inesperado (N06, RF10). La guía pide rechazar el archivo antes de iniciar y que el mensaje indique causa y campo o ID.

**Alternativas.**
1. Fallar en el primer error. Descartada: obliga a corregir y recargar una vez por error.
2. Validar durante la partida, al llegar a cada escena. Descartada: el lector encontraría el error a mitad de la historia.
3. Que `Sesion` valide su propia historia. Descartada: mezcla reglas de partida con formato de archivo y haría que el motor dependa del contrato JSON.

**Decisión.** `validar_historia(datos)` devuelve una lista de mensajes y `cargar_historia(ruta)` lanza `ErrorContenido` (con el atributo `errores`) si la lista no está vacía. `consola.py` captura la excepción, imprime un mensaje por error y termina con código 1, sin crear una `Sesion`.

**Consecuencias.**
- (+) Una historia que llega a `Sesion` ya pasó la validación (CA03). La consola nunca muestra un traceback por contenido inválido que la validación cubre.
- (+) `validar_historia` es una función pura y se prueba sin archivos (un caso por categoría en `CASOS_ERROR`).
- (−) «Todos a la vez» tiene límites en el código actual: si falta un campo de primer nivel o su tipo es incorrecto, la validación se detiene ahí; y las escenas u opciones mal formadas se omiten del resto de las comprobaciones.
- (−) Hay un defecto conocido: un `destino` o un `id` de opción que sea una lista (no texto) lanza `TypeError` en vez de `ErrorContenido`. Ver README, «Limitaciones conocidas».

## Cómo actualizar estas decisiones al llegar la solicitud de cambio
Si el cambio toca reglas (condiciones o efectos), revisar AD-01 y `03_clases_dominio.mmd`, `04_secuencia_elegir_opcion.mmd` y `05_estados_sesion.mmd`. Si toca el formato, revisar AD-02 y `validar_historia`. Si toca la interfaz, revisar `06_componentes.mmd`.
