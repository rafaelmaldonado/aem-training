# Sesión 20 · Revisión práctica de backend AEM

**Guía de preparación · Viernes 11 de septiembre de 2026 · Español**

[Versión HTML](session-20-study-guide.html) · [Sesión y práctica](../lessons/0020-backend-practice-review.html)

La revisión cierra la semana 4: Java y Resource API, Sling Models, servicios OSGi y pruebas. Se usa el componente de las sesiones 18 y 19 para demostrar un recorrido completo. Como las otras revisiones de viernes, esta sesión no lleva slides ni introduce un tema nuevo.

## Qué debes poder explicar

1. Qué recurso aporta el contenido y qué propiedad lee el modelo.
2. Qué configuración recibe el servicio y cómo se identifica su PID.
3. Cómo llega el valor del servicio hasta HTL.
4. Qué hace el componente cuando el título o la configuración están vacíos.
5. Qué aserción detecta una regresión y qué queda fuera de AEM Mocks.

## Recorrido de repaso

```text
Recurso authored → ValueMap → Sling Model → getter → HTL → HTML
                                 ↑
                        servicio OSGi ← configuración
```

Un resource resolver permite acceder a recursos según sus permisos; no convierte el request del usuario en acceso administrativo. Para este componente basta el recurso que ya está renderizando AEM. No abras otro resolver para leer su propio título.

El modelo adapta ese recurso para la vista. La inyección del título es opcional porque existe un fallback explícito; la del servicio es obligatoria porque el párrafo depende de él. Volver opcional una dependencia que falta podría cambiar un diagnóstico claro por una página incompleta.

El servicio define una capacidad reutilizable y aplica su configuración al activarse o modificarse. Una instancia creada con `new` en un test no tiene, por sí sola, el ciclo DS; por eso la práctica usa `registerInjectActivateService`. El PID y los archivos por run mode se comprueban en la instancia, no quedan probados por pasar propiedades directamente al mock.

HTL consume getters y escapa texto. El test protege la salida Java, pero no demuestra que el diálogo persista, que el componente esté permitido ni que el navegador muestre el HTML esperado. La demo une esas evidencias sin confundirlas.

## Agenda de 30 minutos

| Minutos | Actividad |
| --- | --- |
| 0–3 | Quick recap de contenido, configuración, servicio y vista. |
| 3–15 | Dos demos rotativas de seis minutos con evidencia individual. |
| 15–25 | Hallazgos comunes y una variación técnica sobre el mismo componente. |
| 25–30 | Feedback y siguiente comprobación individual. |

Cada participante entrega antes de la revisión su commit, prueba y explicación breve. La sesión no intenta revisar seis repositorios completos en vivo. Una demo debe mostrar el cambio y su resultado, no sólo recorrer archivos.

## Repaso con respuestas

<details><summary>¿Por qué el título del componente no se guarda en ConfigMgr?</summary><p>Porque es contenido de cada instancia authored. ConfigMgr representa configuración de servicios; usarlo para títulos de páginas cambia innecesariamente la responsabilidad del dato.</p></details>

<details><summary>¿Qué demuestra el test rojo de la práctica?</summary><p>Que, al retirar el fallback del mensaje, la misma aserción de salida detecta la regresión. Un fallo de compilación no demuestra ese contrato.</p></details>

<details><summary>¿Por qué no añadimos un servlet?</summary><p>El consumidor es una página HTL y el Sling Model ya entrega lo necesario. No existe un consumidor HTTP adicional que justifique otra ruta.</p></details>

<details><summary>¿Dos implementaciones parecidas demuestran el mismo nivel de comprensión?</summary><p>No. Cada persona debe ejecutar, predecir y explicar una variación del componente y señalar la evidencia que la confirma.</p></details>

## Evidencia mínima

- Recuperación: explica el recorrido sin apuntes.
- Aplicación: commit y salida de las pruebas, más una captura en Preview.
- Explicación: distingue lo demostrado por mocks de lo observado en Author.

El siguiente objetivo se registra como una comprobación concreta: por ejemplo, “puede identificar el PID efectivo sin ayuda”. No se sustituye por horas conectadas o cantidad de commits.

## Referencias del curso

[Java y Resource API](session-16-study-guide.html), [Sling Models](session-17-study-guide.html), [OSGi](session-18-study-guide.html), [JUnit y AEM Mocks](session-19-study-guide.html) y [guía de revisión semanal](weekly-practice-review-instructions.html).

<a id="practica-local"></a>

## Práctica local · Demo verificable de la semana 4 (15–20 min)

**Preparación:** termina el componente de la [sesión 18](session-18-study-guide.html#practica-local) y el test de la [19](session-19-study-guide.html#practica-local). Usa tu propio repo y Author local; esta revisión no introduce clases nuevas.

1. En una terminal, desde tu proyecto AEM, ejecuta `mvn -pl core -Dtest=TrainingMessageTest test`. Enseña el resultado con dos tests, cero fallos y cero errores.
2. En el editor de tu página local, configura el título como `Friday review`, guarda y abre Preview. Enseña ese título junto al mensaje OSGi.
3. Señala la propiedad `title` del recurso de ese componente en CRXDE Lite y el PID de `TrainingMessage` en ConfigMgr. Explica cuál pertenece al autor y cuál a configuración de la aplicación.
4. Vacía el título en el diálogo, guarda y recarga Preview. Antes de hacerlo, predice `Weekend Guides`. Comprueba que el párrafo de configuración no cambió.
5. Abre el segundo test y señala exactamente la aserción que protege el mensaje vacío. Enseña tu evidencia roja de la sesión 19 y la implementación ya restaurada.
6. Ejecuta `mvn -pl core test`. Si falla otro test, registra nombre y causa; no presentes la suite como verde por haber pasado únicamente el test nuevo.
7. Registra ruta de página, commit, resultado Maven y captura del estado final. Termina explicando por qué el componente no necesita un servlet.

**Aceptación:** otra persona puede repetir el cambio de título y observar el fallback; el alumno distingue contenido, configuración, servicio, modelo y HTL, y sabe qué no cubren los mocks. No se pide una segunda implementación del componente.

**Variación durante la demo:** escribe sólo espacios en el título; debe volver al fallback. Si aparece un título vacío, identifica el getter responsable y añade una aserción de ese caso antes de corregirlo.

**Limpieza:** deja el título en un estado legible y conserva la página para revisiones posteriores. No borres el repositorio ni reinstales WKND para repetir la demo.
