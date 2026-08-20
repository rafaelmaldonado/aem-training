# Plan de entrenamiento AEM — borrador

## Resultado esperado

En siete semanas, el equipo remoto debe poder trabajar de extremo a extremo en una solución AEM as a Cloud Service: comprender la arquitectura y el flujo de contenido, desarrollar en su especialidad, revisar trabajo, interpretar el ciclo de entrega y explicar las decisiones tomadas. El arquitecto debe poder demostrar ese progreso con evidencia individual.

El curso utiliza el mismo proyecto integrador para seis desarrolladores, pero cada persona realiza las prácticas en su propio repositorio y SDK local. La profundidad se ajusta después del diagnóstico; no se intenta que cada persona sea especialista en todo.

Cloud Manager se enseña con diagramas y evidencia anonimizada, sin acceso ni despliegues. Ese tiempo práctico se concentra en Dispatcher/caché local, decisiones HTL y Sling Models, seguridad, accesibilidad, rendimiento, regresión y troubleshooting.

## Ritmo diario (30 minutos en línea)

- 0–3 min: recuperación sin apuntes.
- 3–5 min: objetivo y escenario.
- 5–17 min: cuatro o cinco slides de concepto.
- 17–25 min: demo o ejemplo resuelto por el arquitecto.
- 25–28 min: ejercicio posterior y criterio de aceptación.
- 28–30 min: preguntas y exit prompt.

Después de la sesión, cada participante dedica 60–120 minutos al ejercicio esencial y entrega evidencia asíncrona. Si dispone de la ventana completa de 2–4 horas, usa el tiempo restante en el proyecto integrador, lectura oficial o PR review. No se requieren breakout rooms.

## Programa de siete semanas

| Semana | Fundamento común | Práctica y evidencia |
|---|---|---|
| 1. Orientación y base | Diagnóstico; arquitectura Author/Publish; repositorio JCR; Sling; OSGi; ciclo petición–contenido–render; diferencias relevantes de AEM Cloud | Entorno listo, recorrido de contenido y alcance de mantenimiento confirmado con el proyecto real |
| 2. Autoría y modelado | Sites, Assets, páginas, templates editables, políticas, componentes y modelo de contenido | Los alumnos construyen una sección authorable sin código innecesario y explican la experiencia del autor |
| 3. Frontend AEM | HTL, Core Components y proxy pattern, client libraries, diálogos, estilos, accesibilidad, responsive y frontend testing | Primer componente vertical integrado y authorable |
| 4. Backend AEM | Sling Models, delegación, Model Exporter, servlets sólo cuando hagan falta, servicios OSGi, configuración, Resource API, inyección, JUnit 5 y AEM Mocks | Componente con lógica de servidor, configuración por ambiente y prueba pequeña |
| 5. Reutilización y mantenimiento | MSM, Experience Fragments, Content Fragments para Sites tradicional, paquetes, diagnóstico, workflows/jobs y publicación de referencias | Relación de contenido y cambio de mantenimiento diagnosticados con evidencia |
| 6. Calidad y restricciones de entrega | Búsqueda/tags, Cloud Manager teórico, Dispatcher/caché local, ACLs, service users, Repo Init y seguridad | Auditoría local, corrección prioritaria y defensa del flujo cloud suministrado |
| 7. Entrega y transferencia | Accesibilidad, rendimiento, pruebas por riesgo, capstone, hardening, regresión, documentación mínima, demo y retrospectiva | Capstone individual, demo y defensa técnica |

## Rutas por perfil

Todos completan el fundamento común y al menos una tarea vertical. Desde la semana 3:

- Frontend: HTL, Core Components, CSS/JS, authorability, accesibilidad y rendimiento.
- Backend: Sling Models, OSGi, APIs, seguridad, configuración y pruebas.
- AEM/tech lead: modelado, templates/policies, integración, Dispatcher/CDN, lectura del flujo Cloud Manager y decisiones transversales.

Una persona puede tomar una ruta principal y otra secundaria. No se obliga al frontend a memorizar APIs Java ni al backend a especializarse en CSS para aprobar.

## Proyecto integrador

Mantener y extender el repositorio oficial WKND con una sección `Weekend Guides`:

- páginas y navegación administrables;
- Guide Page, Guide Card y Guide List basados en capacidades nativas o Core Components;
- contenido estructurado para al menos un caso real;
- una integración pequeña y auténtica del negocio;
- permisos, caché, accesibilidad, pruebas y compatibilidad con el pipeline;
- README operativo corto y demo final.

Cada persona elige uno de dos baselines aprobados —clonar el tutorial público WKND o generar el proyecto con AEM Project Archetype— y completa la misma práctica semanal en su propio repositorio y SDK. La práctica se publica el lunes, se entrega el jueves y se revisa el viernes, sin dependencias entre participantes. Evitar microservicios, SPA, personalización, Forms o Commerce salvo que el trabajo real los necesite.

La guía de siete prácticas individuales está en `reference/wknd-project-backlog.html`.

## Evaluación

- Antes del Día 1, diagnóstico asíncrono sin calificación: conceptos, lectura de código y una tarea corta; clasifica apoyo necesario, no personas.
- Cada viernes, sesión de revisión de 30 min: recuperación, dos demos rotativas, hallazgos comunes, comprobación de entendimiento y siguiente reto.
- Las seis entregas se revisan de forma asíncrona antes de la sesión; la revisión en vivo usa muestras representativas.
- Semana 7: capstone individual, demo y defensa técnica. Una presentación no sustituye demostrar el código.

Rúbrica estable: funcionamiento 30%, authorability/modelado 20%, calidad y seguridad 20%, explicación técnica 15%, colaboración y entrega 15%.

## Evidencia individual

Cada participante deja sólo tres evidencias por semana:

1. Recuperación: respuesta breve sin consultar apuntes.
2. Aplicación: PR, commit, prueba, configuración o diagnóstico verificable.
3. Explicación: comentario de revisión, demo breve o defensa de una decisión y su riesgo.

El arquitecto registra el resultado como `no demostrado`, `con apoyo`, `independiente` o `puede guiar`, además del siguiente tema a comprobar. La similitud entre soluciones orienta la revisión, pero el entendimiento se confirma al explicar, ejecutar y modificar el código. Usar la [hoja de seguimiento](reference/seguimiento-evidencias.html); no usar asistencia, cámara encendida, horas conectadas ni cantidad de commits como sustitutos de aprendizaje.

Los enlaces se entregan el jueves antes del cierre. El arquitecto dedica aproximadamente cinco minutos por persona a revisarlos de forma asíncrona; el viernes discute patrones, observa dos demos rotativas y comprueba lo dudoso.

## Revisión del viernes

La sesión usa 3 minutos de recuperación, 12 minutos para dos demos rotativas, 10 minutos para hallazgos comunes y una variación técnica, y 5 minutos para feedback y siguiente comprobación.

No revisar las seis entregas en vivo ni convertir la sesión en estatus. Las demos y preguntas confirman algo ya practicado; el feedback individual restante queda en cada PR.

## Cadencia remota

- Lunes: objetivo semanal, concepto inicial y publicación de la práctica.
- Martes a jueves: recuperación, microlección, demo y ejercicio posterior.
- Viernes: recuperación, dos demos rotativas, hallazgos comunes, comprobación y cierre.
- Seguimiento asíncrono: `hecho / siguiente / bloqueo / evidencia`.
- Instructor: un bloque opcional de oficina de 30 min por semana.

No hay breakout rooms, daily adicional ni reunión de estatus separada. La colaboración ocurre mediante PR reviews y comentarios asíncronos.

## Primera sesión (30 minutos)

La primera clase construye el mapa Author → distribución → Publish → Dispatcher/CDN → navegador y lo contrasta con Git → pipeline → AEM. Incluye recuperación, contenido listo para slides, demo, ejercicio y exit prompt. El guion completo está en `lessons/0003-aem-foundations.html`.

## Condiciones confirmadas e información por levantar

1. Identificar la especialidad y experiencia real de cada participante mediante el diagnóstico.
2. Usar el AEM as a Cloud Service SDK ya disponible; Cloud Manager no es requisito del entrenamiento.
3. Crear el repositorio individual desde una de las dos rutas aprobadas: clonar WKND o ejecutar AEM Project Archetype.
4. Obtener dos o tres tipos de cambio reales que el equipo deberá resolver después del entrenamiento.
