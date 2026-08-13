# Plan de entrenamiento AEM — borrador

## Resultado esperado

En ocho semanas, el equipo remoto debe poder trabajar de extremo a extremo en una solución AEM as a Cloud Service: comprender la arquitectura y el flujo de contenido, desarrollar en su especialidad, revisar el trabajo de otra persona, operar el ciclo de entrega y explicar las decisiones tomadas. El arquitecto debe poder demostrar ese progreso con evidencia individual.

El curso utiliza un solo proyecto integrador para seis desarrolladores y simula el mantenimiento evolutivo de AEM Sites tradicional. La profundidad se ajusta después del diagnóstico; no se intenta que cada persona sea especialista en todo.

## Ritmo diario (30 minutos en línea)

- 0–3 min: recuperación sin apuntes.
- 3–5 min: objetivo y escenario.
- 5–17 min: cuatro o cinco slides de concepto.
- 17–25 min: demo o ejemplo resuelto por el arquitecto.
- 25–28 min: ejercicio posterior y criterio de aceptación.
- 28–30 min: preguntas y exit prompt.

Después de la sesión, cada participante dedica 60–120 minutos al ejercicio esencial y entrega evidencia asíncrona. Si dispone de la ventana completa de 2–4 horas, usa el tiempo restante en el proyecto integrador, lectura oficial o PR review. No se requieren breakout rooms.

## Programa de ocho semanas

| Semana | Fundamento común | Práctica y evidencia |
|---|---|---|
| 1. Orientación y base | Diagnóstico; arquitectura Author/Publish; repositorio JCR; Sling; OSGi; ciclo petición–contenido–render; diferencias relevantes de AEM Cloud | Entorno listo, recorrido de contenido y alcance de mantenimiento confirmado con el proyecto real |
| 2. Autoría y modelado | Sites, Assets, páginas, templates editables, políticas, componentes y modelo de contenido | Los alumnos construyen una sección authorable sin código innecesario y explican la experiencia del autor |
| 3. Frontend AEM | HTL, Core Components y proxy pattern, client libraries, diálogos, estilos, accesibilidad, responsive y frontend testing | Primer componente vertical integrado y authorable |
| 4. Backend AEM | Sling Models, servlets sólo cuando hagan falta, servicios OSGi, configuración, Resource API, inyección y pruebas unitarias | Componente con lógica de servidor, configuración por ambiente y prueba pequeña |
| 5. Mantenimiento e integraciones | Workflows, búsqueda, Content Fragments cuando apliquen, APIs, autenticación, caché e integración segura | Cambio de mantenimiento real e integración con contrato probado |
| 6. Cloud, entrega y calidad | SDK local, Git, Cloud Manager, ambientes, pipelines, quality gates, Dispatcher/CDN, caché, logs, secretos y troubleshooting | Cambio desplegado por pipeline; ejercicio de fallo, diagnóstico y corrección |
| 7. Calidad de producción | Rendimiento, seguridad, permisos, accesibilidad, SEO, observabilidad, pruebas y revisión de código | Auditoría cruzada del proyecto; corrección de los riesgos prioritarios |
| 8. Entrega y transferencia | Hardening, documentación mínima, operación, demo y retrospectiva | Evaluación práctica individual, demo grupal y defensa técnica del proyecto |

## Rutas por perfil

Todos completan el fundamento común y al menos una tarea vertical. Desde la semana 3:

- Frontend: HTL, Core Components, CSS/JS, authorability, accesibilidad y rendimiento.
- Backend: Sling Models, OSGi, APIs, seguridad, configuración y pruebas.
- AEM/tech lead: modelado, templates/policies, integración, Dispatcher/CDN, Cloud Manager y decisiones transversales.

Una persona puede tomar una ruta principal y otra secundaria. No se obliga al frontend a memorizar APIs Java ni al backend a especializarse en CSS para aprobar.

## Proyecto integrador

Mantener y extender el repositorio oficial WKND con una sección `Weekend Guides`:

- páginas y navegación administrables;
- Guide Page, Guide Card y Guide List basados en capacidades nativas o Core Components;
- contenido estructurado para al menos un caso real;
- una integración pequeña y auténtica del negocio;
- permisos, caché, accesibilidad, pruebas y pipeline;
- README operativo corto y demo final.

Cada semana produce un incremento demostrable. Evitar microservicios, SPA, personalización, Forms o Commerce salvo que el trabajo real los necesite.

El backlog operativo de 48 historias está en `reference/wknd-project-backlog.html`.

## Evaluación

- Antes del Día 1, diagnóstico asíncrono sin calificación: conceptos, lectura de código y una tarea corta; clasifica apoyo necesario, no personas.
- Cada viernes, sesión de 30 min: recuperación, una presentación de participante, muestra de evidencia y siguiente reto.
- Fin de semanas 2, 4 y 6: checkpoint de proyecto con rúbrica común.
- Semana 8: tarea práctica individual y proyecto grupal. Una presentación no sustituye demostrar el código.

Rúbrica estable: funcionamiento 30%, authorability/modelado 20%, calidad y seguridad 20%, explicación técnica 15%, colaboración y entrega 15%.

## Evidencia individual

Cada participante deja sólo tres evidencias por semana:

1. Recuperación: respuesta breve sin consultar apuntes.
2. Aplicación: PR, commit, prueba, configuración o diagnóstico verificable.
3. Explicación: comentario de revisión, demo breve o defensa de una decisión y su riesgo.

El arquitecto registra el resultado como `no demostrado`, `con apoyo`, `independiente` o `puede guiar`, además del siguiente tema a comprobar. El proyecto grupal aporta contexto, pero no reemplaza estas tres evidencias individuales. Usar la [hoja de seguimiento](reference/seguimiento-evidencias.html); no usar asistencia, cámara encendida, horas conectadas ni cantidad de commits como sustitutos de aprendizaje.

Los enlaces se entregan antes del jueves al cierre. El arquitecto dedica aproximadamente cinco minutos por persona a revisarlos de forma asíncrona; el viernes sólo hace una comprobación breve y aclara lo dudoso.

## Presentaciones de participantes

Una presentación semanal de 8 minutos, más 7 de preguntas, preparada por una persona. Debe incluir una demostración o ejemplo, una decisión y un error frecuente. Temas posibles: Sling resolution, HTL context-aware escaping, Core Components, configuración OSGi, Dispatcher caching, Content Fragments, Cloud Manager quality gates y accesibilidad.

No usar exposiciones para introducir contenido crítico; sirven para recuperar, enseñar y discutir algo ya practicado.

## Cadencia remota

- Lunes: objetivo semanal, concepto inicial y ejercicio.
- Martes a jueves: recuperación, microlección, demo y ejercicio posterior.
- Viernes: presentación de 8 min, 7 min de preguntas, 10 min de evidencia/demo y 5 min de cierre.
- Seguimiento asíncrono: `hecho / siguiente / bloqueo / evidencia`.
- Instructor: un bloque opcional de oficina de 30 min por semana.

No hay breakout rooms, daily adicional ni reunión de estatus separada. La colaboración ocurre mediante PR reviews y comentarios asíncronos.

## Primera sesión (30 minutos)

La primera clase construye el mapa Author → distribución → Publish → Dispatcher/CDN → navegador y lo contrasta con Git → pipeline → AEM. Incluye recuperación, contenido listo para slides, demo, ejercicio y exit prompt. El guion completo está en `lessons/0003-aem-foundations.html`.

## Confirmaciones de la primera semana

1. Identificar la especialidad y experiencia real de cada participante mediante el diagnóstico.
2. Verificar acceso al SDK, repositorio y, si corresponde a sus funciones, Cloud Manager.
3. Confirmar que el trabajo es mantenimiento de AEM Sites tradicional y conocer la versión/plataforma del proyecto.
4. Obtener dos o tres tipos de cambio reales que el equipo deberá resolver después del entrenamiento.
