# Matriz de trazabilidad

Modelos en `docs/modelos/`: 01_contexto, 02_casos_de_uso, 03_clases_dominio, 04_secuencia_elegir_opcion, 05_estados_sesion y 06_componentes (extensión `.mmd`).

| ID | Modelo | Componente o archivo | Prueba | Evidencia |
|---|---|---|---|---|
| RF01 | 02_casos_de_uso, 06_componentes | `src/cargador.py` (`cargar_historia`) | `test_integracion.py::test_i1_deshacer_desde_cada_final` | `evidencia/ultima_ejecucion.txt` |
| RF02 | 03_clases_dominio, 05_estados_sesion | `src/motor.py` (`Sesion.reiniciar`) | `test_motor.py::test_u5_reiniciar` | `evidencia/ultima_ejecucion.txt` |
| RF03 | 04_secuencia_elegir_opcion | `src/consola.py` (`jugar`) | Demostración en video | Video de la demostración |
| RF04 | 04_secuencia_elegir_opcion | `src/motor.py` (`opciones_habilitadas`) | `test_motor.py::test_u1_condiciones`, `test_e3_siempre_dos_opciones` | `evidencia/ultima_ejecucion.txt` |
| RF05 | 04_secuencia_elegir_opcion, 05_estados_sesion | `src/motor.py` (`elegir`) | `test_motor.py::test_u2_eleccion_valida` | `evidencia/ultima_ejecucion.txt` |
| RF06 | 04_secuencia_elegir_opcion | `src/motor.py` (`elegir`) | `test_motor.py::test_u3_opcion_invalida_no_cambia_estado` | `evidencia/ultima_ejecucion.txt` |
| RF07 | 03_clases_dominio | `src/motor.py` (`Sesion.variables`) | `test_motor.py::test_u2_eleccion_valida` | `evidencia/ultima_ejecucion.txt` |
| RF08 | 05_estados_sesion | `src/motor.py` (`es_final`) | `test_integracion.py::test_i1_tres_finales_desde_archivo_real` | `evidencia/ultima_ejecucion.txt` |
| RF09 | 05_estados_sesion | `src/motor.py` (`reiniciar`) | `test_motor.py::test_u5_reiniciar`, `test_u5_reiniciar_elimina_historial` | `evidencia/ultima_ejecucion.txt` |
| RF10 | 02_casos_de_uso, 06_componentes | `src/cargador.py` (`validar_historia`, `ErrorContenido`) | `test_cargador.py::test_u4_errores_de_contenido`, `test_ca03_destino_inexistente_rechaza_carga` | `evidencia/ultima_ejecucion.txt` |
| RF11 | 05_estados_sesion | `src/motor.py` (`bloqueada`), `src/consola.py` | `test_motor.py::test_bloqueo_en_escena_no_final` | `evidencia/ultima_ejecucion.txt` |
| RF12 | 02_casos_de_uso, 04_secuencia_elegir_opcion, 05_estados_sesion | `src/motor.py` (`deshacer`), `src/consola.py` | `test_motor.py::test_u6_deshacer_restaura_y_consume`, `test_integracion.py::test_i1_deshacer_desde_cada_final` | `evidencia/ultima_ejecucion.txt` |
| RF13 | 03_clases_dominio, 05_estados_sesion | `src/motor.py` (`puede_deshacer`) | `test_motor.py::test_u6_sin_retroceso_al_comenzar`, `test_u6_nueva_eleccion_rehabilita_retroceso` | `evidencia/ultima_ejecucion.txt` |
| RF14 | 04_secuencia_elegir_opcion | `src/motor.py` (`elegir`) | `test_motor.py::test_u6_entrada_invalida_preserva_historial` | `evidencia/ultima_ejecucion.txt` |
| RNF01 | 06_componentes | `tests/simular_partidas.py` | 1 000 partidas aleatorias, semilla 42 | `evidencia/rnf01.txt` |
| RNF02 | 06_componentes | `src/cargador.py` | `test_cargador.py::test_u4_errores_de_contenido` (causa e ID en el mensaje) | `evidencia/ultima_ejecucion.txt` |
| RNF03 | 06_componentes | `contenido/el_faro.json`, `src/motor.py`, `docs/decisiones_arquitectura.md` | `test_segunda_historia.py::test_motor_no_contiene_datos_de_las_historias` | `evidencia/rnf03.txt` |
| SC01 | 02_casos_de_uso, 03_clases_dominio, 04_secuencia_elegir_opcion, 05_estados_sesion | `src/motor.py`, `src/consola.py` | U6, U5 e I1 extendidos | `docs/cambio.md`, `docs/solicitud_de_cambio.pdf`, tags `version-inicial` y `version-final` |

## Versiones
- Antes del cambio: tag version-inicial(commitd91efc9)
- Después del cambio: tag version-final(commit0254260)