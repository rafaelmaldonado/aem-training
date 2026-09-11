# Rediseño del entrenamiento AEM as a Cloud Service hasta el 30 de octubre

**Propuesta para revisión · 11 semanas · 55 sesiones · 17 de agosto–30 de octubre de 2026**

[Versión HTML](eleven-week-redesign-proposal.html) · [Temario vigente](aem-course-topics.html) · [Prácticas vigentes](wknd-project-backlog.html)

## Decisión recomendada

Conservar íntegramente las semanas 1–5 y sustituir la planificación de las semanas 6–7 por seis semanas nuevas, del 21 de septiembre al 30 de octubre. Cada semana tiene cuatro sesiones técnicas y un viernes exclusivo de recap y demo de la práctica. Todas duran entre 30 y 60 minutos, dentro del tiempo reservado en calendario. El curso queda en 44 sesiones técnicas y 11 encuentros de recap y demo.

Las sesiones 1–20 ya impartidas y el material preparado de las sesiones 21–25 no se reescriben. Las prácticas 1–5 también se conservan. Este documento propone el cambio; todavía no sustituye el temario publicado ni constituye material de clase ya desarrollado.

Se conserva el escenario **Weekend Guides**, seis developers y una práctica semanal común **voluntaria**. Quien decida implementarla puede usar su repositorio y SDK. El brief se publica el lunes; quien quiera feedback puede compartir avances antes del viernes. No hay entregas obligatorias, calificación final ni requisitos de aprobación.

**Restricciones aclaradas por el instructor:** no dispone de Cloud Manager y no se puede contar con acceso utilizable para pruebas por parte de los participantes. Cloud Manager, RDE y CDN se enseñan con documentación pública, diagramas, videos disponibles y casos sintéticos claramente identificados. Sólo se usa evidencia real si ya está disponible; no se presupone una demo Cloud en vivo. El uso laboral de GraphQL es desconocido: queda como lectura opcional fuera del calendario principal.

**Continuidad sin tareas obligatorias:** cada semana incluye un punto de partida suministrado y un ejemplo completo del instructor. Nadie necesita completar las prácticas anteriores para seguir las clases, observar la demo o intentar la práctica actual. Las comprobaciones de este documento describen resultados técnicos para autoevaluación y feedback, no una rúbrica de calificación.

## Qué cambia respecto de la propuesta recibida

| Observación | Ajuste propuesto | Razón |
| --- | --- | --- |
| Los viernes de las semanas 7–10 introducen un lab o tema nuevo. | Los casos se trabajan de lunes a jueves; el viernes se presentan resultados. | Mantener la cadencia de recap y demostración sin estrenar requisitos. |
| Workflows, launchers, Sling Jobs, MSM y CF ya aparecen en la semana 5. | En la semana 9 se resuelven problemas de reintentos, integraciones y evolución del contenido. | La segunda exposición debe exigir una capacidad nueva, no repetir definiciones. |
| Service users aparecen antes de ACLs y Repo Init. | Miércoles: identidades, permisos y Repo Init. Jueves: subservices y ciclo de vida del resolver. | Primero preparar la identidad y sus permisos, después consumirla desde código. |
| Tags y taxonomía desaparecen del nuevo bloque de consultas. | Recuperarlos el lunes de la semana 6 como contrato de clasificación de Guide List. | Ya son parte del proyecto y conectan autoría con búsqueda. |
| La práctica 6 vigente reúne consultas, Cloud Manager, Dispatcher y seguridad. | Repartir sus objetivos entre las prácticas 6, 7, 8 y 10. | Una demo breve puede defender un resultado semanal concreto. |
| La semana 10 concentra a11y, SEO y rendimiento en una sola sesión. | Un día para accesibilidad/SEO y otro para rendimiento; unitarias e integración se comparan el lunes. | JUnit y AEM Mocks ya se estudiaron en la semana 4. |
| GraphQL cambia el alcance y ocupa un viernes. | Lectura opcional fuera del calendario principal. | No hay una necesidad laboral confirmada y no debe desplazar el recap y la demo. |
| El capstone parece comenzar desde cero la última semana. | Caso integrador suministrado y ampliación personal opcional. | La última semana sirve para integrar, diagnosticar y compartir aprendizajes sin examen final. |

## Cobertura comprobada y huecos que conviene atender

“Falta” significa que no encontré un bloque o evidencia práctica explícita en los materiales revisados; no implica que el instructor nunca lo haya mencionado en clase.

| Área | Base conservada en semanas 1–5 | Profundidad nueva |
| --- | --- | --- |
| Repositorio y consultas | JCR/Resource API en sesiones 3 y 16; tags como datos en HTL. | Taxonomía, QueryBuilder/JCR-SQL2, paginación, límites, orden, full-text y lectura del plan. Semana 6. |
| Identidad y seguridad | La sesión 16 menciona acceso administrativo prohibido y cierre de resolvers; HTL seguro y límites de servlet en semanas 3–4. | ACL efectiva, Repo Init, mappings, identidad del solicitante, autorización y diagnóstico de 403. Semana 6; refuerzo en 7 y 10. |
| Entrega | Modelo Author/Publish desde semana 1; dependencias de fragmentos en sesión 24. | Publicación/despublicación, estado en destino, filtros, redirects/rewrites, cachés y contenido privado. Semana 7. |
| Operación Cloud | Paquetes e inmutabilidad en sesión 22; configuración OSGi y secretos en 18; diagnóstico en 23. | Tipo de pipeline, lectura de fallos, compatibilidad entre versiones, configuración efectiva y elección de herramientas Cloud. Semana 8. |
| Integraciones y asincronía | Servicios y criterios de retry ya introducidos en 18 y 23. | HTTP saliente con timeouts y fallos, ejecución repetida, progreso persistido y límites de escalado. Semana 9. |
| Arquitectura de contenido | MSM en 21 y CF/XF en 24. | Casos de localización, acciones de rollout existentes, cambio de modelo y referencias entre fragmentos. Semana 9. |
| Calidad | A11y/responsive/Data Layer en semanas 2–3; JUnit/AEM Mocks en 4. | Comprobaciones con repositorio/HTTP real, flujo UI, SEO y medición comparable de rendimiento. Semana 10. |
| Diagnóstico integral | Varias trazas parciales y una práctica de mantenimiento. | Correlación por capas, descarte de hipótesis, recuperación y explicación del caso. Semana 11. |

Hay cuatro límites técnicos que deben quedar explícitos en el material nuevo:

- **Una consulta que usa un índice todavía puede ser costosa.** Revisar restricciones, ordenamiento, resultados leídos y plan; no aprobar sólo porque aparece el nombre de un índice. Un índice nuevo se justifica con evidencia y sigue el proceso de despliegue Cloud. [Consultas e índices — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/query-and-indexing-best-practices), [indexación en Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/indexing).
- **Un service resolver no sustituye los permisos del visitante.** La lectura que debe respetar al solicitante conserva esa identidad; una tarea técnica usa un subservice con alcance explícito. AEM Mocks no sustituye la comprobación de ACL efectiva en un repositorio real. [Service users — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/developing/advanced/service-users).
- **Publish, Dispatcher y CDN son pruebas distintas.** No atribuir a la replicación clásica local todas las propiedades de Sling Content Distribution ni asumir que un encabezado de privacidad protege por sí solo todas las capas de caché. [Replicación Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/replication), [caché en AEMaaCS — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching).
- **Los fallos de red y reinicios forman parte del caso normal Cloud.** Enseñar estado persistente apropiado, compatibilidad entre versiones y procesamiento reanudable. Un timeout no prueba que el sistema remoto no haya ejecutado la operación. [Guías de desarrollo Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/development-guidelines).

## Calendario propuesto: semanas 6–11

Cada fila tiene un foco principal y una demo preparada por el instructor. Diseñar un núcleo de 30 minutos: 5 de recuperación y objetivo, 12 de explicación, 10 de demo y 3 de cierre. Para sesiones de hasta 60 minutos, ampliar hasta 20 minutos la demo o el diagnóstico guiado y reservar hasta 10 minutos adicionales para preguntas. El margen permite profundizar en el mismo objetivo; no obliga a duplicar temas ni slides. La comprensión de una clase no depende de haber hecho tareas.

### Semana 6 · Repositorio, consultas y acceso seguro · 21–25 de septiembre

| Sesión | Fecha | Tema y capacidad observable |
| --- | --- | --- |
| 26 | Lun 21 sep | **Consultar contenido clasificado.** Tags/taxonomía, QueryBuilder y lectura equivalente en JCR-SQL2; path, tipo, propiedades, full-text, límite y paginación. Explicar qué devuelve Guide List y qué excluye. |
| 27 | Mar 22 sep | **Diagnosticar una consulta costosa.** Traversal, Explain Query, selectividad, ordenamiento y resultados leídos; revisar una definición de índice compatible con Cloud. Corregir primero la consulta cuando sea suficiente. |
| 28 | Mié 23 sep | **Modelar permisos como código.** Usuarios, grupos y service users; ACL efectiva y mínimo privilegio; paths y permisos con Repo Init. Distinguir identidad humana gestionada mediante IMS de identidad técnica del repositorio. |
| 29 | Jue 24 sep | **Acceder al repositorio con la identidad correcta.** ResourceResolverFactory, subservice mappings, cierre/propiedad del resolver y request resolver frente a service resolver. Distinguir un fallo de mapping, ACL y protección HTTP como CSRF. |
| 30 | Vie 25 sep | **Recap y demo de la práctica 6:** Guide List acotada y diagnóstico de un fallo de acceso; mostrar resultado permitido y resultado excluido. |

La práctica implementa una sola vía de consulta; JCR-SQL2 sirve para entender y contrastar el plan, no para construir dos implementaciones del mismo listado. CSRF, autorización y CORS se distinguen como controles diferentes, sin desactivarlos para hacer pasar una prueba. [Protección CSRF — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/developing/advanced/csrf-protection).

### Semana 7 · Publicación, Dispatcher y CDN · 28 de septiembre–2 de octubre

| Sesión | Fecha | Tema y capacidad observable |
| --- | --- | --- |
| 31 | Lun 28 sep | **Comprobar la publicación.** Author → Publish, publicar/despublicar, dependencias, estado y Sling Content Distribution; propósito de Preview. Separar código desplegado de contenido publicado. |
| 32 | Mar 29 sep | **Seguir una petición por Apache y Dispatcher.** Vhost, farm, filtros, rewrite frente a redirect y encabezados. Explicar un 403/404 con la regla y la capa responsables. |
| 33 | Mié 30 sep | **Diagnosticar caché de Dispatcher.** Reglas, invalidación, stat files, TTL y parámetros de URL. Reproducir un miss, un hit y una actualización controlada. |
| 34 | Jue 1 oct | **Separar navegador, CDN y Dispatcher.** Cache-Control, Surrogate-Control, cookies y contenido privado; versionado de assets/clientlibs. Atribuir contenido antiguo a una capa usando evidencia. |
| 35 | Vie 2 oct | **Recap y demo de la práctica 7:** “funciona en Author, falla en Publish” o “se sirve contenido anterior”, resuelto durante la semana. |

El requisito es diagnosticar y probar una política concreta, no memorizar todas las directivas ni borrar globalmente las cachés. La ejecución local demuestra Publish/Dispatcher; los resultados de CDN se analizan en evidencia suministrada cuando no hay acceso Cloud.

### Semana 8 · Desarrollo, despliegue y diagnóstico Cloud · 5–9 de octubre

| Sesión | Fecha | Tema y capacidad observable |
| --- | --- | --- |
| 36 | Lun 5 oct | **Elegir el flujo de entrega.** Cloud Manager: programas, ambientes, repositorios y pipelines de aplicación/frontend/configuración según el cambio. Relacionar commit, artefacto y destino. |
| 37 | Mar 6 oct | **Leer un fallo de pipeline.** Build, calidad, seguridad, pruebas y despliegue; identificar el primer error accionable. Compatibilidad entre código anterior/nuevo y contenido durante una actualización; estrategia de recuperación. |
| 38 | Mié 7 oct | **Explicar la configuración efectiva.** PID/factory, run modes permitidos, .cfg.json, valores de entorno y secretos. Diagnosticar por qué el servicio local y el Cloud difieren sin repetir la introducción OSGi. |
| 39 | Jue 8 oct | **Elegir una herramienta Cloud para una hipótesis.** RDE para iteración; AEM Developer Console, Repository Browser y logs para inspección. Resolver un caso guiado, no recorrer cuatro interfaces sin objetivo. |
| 40 | Vie 9 oct | **Recap y demo de la práctica 8:** diagnóstico de un despliegue/configuración fallido con evidencia proporcionada y corrección local verificable. |

RDE no reemplaza la validación del pipeline. La selección de configuración se estudia con las reglas Cloud, incluidos los run modes soportados y la separación entre valores versionados y secretos. [RDE — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/rapid-development-environments), [configuración OSGi — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi).

### Semana 9 · Integraciones resilientes y evolución del contenido · 12–16 de octubre

| Sesión | Fecha | Tema y capacidad observable |
| --- | --- | --- |
| 41 | Lun 12 oct | **Hacer una tarea asíncrona reintentable.** Aplicar workflows/launchers/Sling Jobs ya conocidos: efectos repetidos, idempotencia, reanudación, lotes y prevención de bucles. Diferenciar coordinación del trabajo de su efecto de negocio. |
| 42 | Mar 13 oct | **Consumir un servicio externo desde AEM.** Servicio OSGi, timeouts, errores HTTP, credenciales y límites de reintento; diagnóstico de conectividad/egress. Usar un stub local; no bloquear el render de una página con trabajo largo. |
| 43 | Mié 14 oct | **Resolver un caso MSM de localización.** Rollout configurations existentes, cancelación/restauración de herencia y referencias localizadas. Diferenciar Live Copy, Language Copy y proceso de traducción. |
| 44 | Jue 15 oct | **Evolucionar un modelo CF sin romper consumidores.** Referencias de contenido frente a referencias entre fragmentos, campos ausentes, profundidad del modelo y dependencias de publicación. Mantener consumo en Sites. |
| 45 | Vie 16 oct | **Recap y demo de la práctica 9:** tarea que tolera fallo/reintento y justificación del impacto sobre contenido compartido. |

No se exige escribir un motor de workflows, una rollout action propia ni una aplicación Headless. La sesión 44 mantiene CF relacionados y evolución del modelo para Sites. GraphQL se ofrece únicamente como lectura opcional; no se reserva una sesión ni se añade a la práctica mientras su necesidad laboral siga sin confirmar.

### Semana 10 · Estrategia de pruebas y calidad observable · 19–23 de octubre

| Sesión | Fecha | Tema y capacidad observable |
| --- | --- | --- |
| 46 | Lun 19 oct | **Elegir la prueba que puede demostrar el riesgo.** Casos negativos de Models/servicios/servlets; límites de AEM Mocks; prueba con repositorio o HTTP real para permisos, resolución o integración. |
| 47 | Mar 20 oct | **Automatizar un recorrido crítico.** Un flujo author → página visible con una sola herramienta UI; datos estables, selectores, aislamiento y diagnóstico de pruebas intermitentes. Relación con ui.tests/Cloud Manager. |
| 48 | Mié 21 oct | **Comprobar accesibilidad y SEO.** Teclado, foco, semántica, nombres accesibles y zoom; título, canonical, indexabilidad y sitemap según el caso. Lighthouse/Experience Audit como evidencia parcial. |
| 49 | Jue 22 oct | **Medir y corregir un cuello de botella.** Separar backend/consulta, caché, imágenes/clientlibs y navegador; baseline comparable, medición repetible, presupuesto acordado y un cambio comprobado. |
| 50 | Vie 23 oct | **Recap y demo de la práctica 10:** regresión detectada y corrección de calidad/rendimiento con evidencia antes/después. |

No se enseñan Cypress, Playwright y Selenium como tres cursos. Se elige la herramienta del baseline o una sola para todos. Tampoco se equipara una puntuación Lighthouse con conformidad completa de accesibilidad ni se exige “100” como aceptación universal. Adobe distingue pruebas funcionales, UI y Experience Audit dentro de su estrategia de validación. [Pruebas funcionales y UI — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/test-results/functional-testing/functional-testing).

### Semana 11 · Troubleshooting y caso integrador · 26–30 de octubre

| Sesión | Fecha | Tema y capacidad observable |
| --- | --- | --- |
| 51 | Lun 26 oct | **Trazar un fallo de extremo a extremo.** Navegador → CDN → Dispatcher → Sling → Model → OSGi → JCR. Delimitar síntoma, petición, tiempo y primera capa divergente. |
| 52 | Mar 27 oct | **Resolver un incidente con evidencia incompleta.** Códigos HTTP, logs, bundles/servicios/configuración, consultas y cachés; priorizar hipótesis y elegir la siguiente prueba. |
| 53 | Mié 28 oct | **Integrar y depurar el caso completo.** Clínica guiada sobre el ejemplo suministrado y, si los hay, avances voluntarios; completar el recorrido y sus comprobaciones. |
| 54 | Jue 29 oct | **Revisar y consolidar.** Code review, regresiones, recuperación y limitaciones del ejemplo; feedback a quienes compartan su trabajo. |
| 55 | Vie 30 oct | **Recap final, demos voluntarias y retrospectiva.** Mostrar el caso integrado y aprendizajes; sin examen, calificación ni defensa obligatoria. |

## Cómo quedan las prácticas

Los materiales de las prácticas 1–5 se conservan intactos; cualquier instrucción previa de obligatoriedad o evaluación deja de aplicarse conforme a esta aclaración. La práctica 6 antigua se descompone; la práctica 7 antigua se reformula como caso integrador opcional en la semana 11. Las nuevas prácticas reutilizan el mismo proyecto, con un punto de partida suministrado por semana para evitar dependencias de tareas anteriores.

Ofrecer dos recorridos voluntarios: **explorar el ejemplo** (30–60 minutos orientativos para ejecutarlo, cambiar un dato y observar) o **implementar la ampliación completa** (4–6 horas estimadas; hasta 6–8 para los casos más extensos de semanas 9 y 11). No son horas exigidas ni criterios de participación. Los pasos siguientes describen la ampliación; cada brief debe identificar también el recorrido breve. Quien no haga práctica puede seguir todas las sesiones y el recap del viernes.

### Práctica 6 · Guide List acotada y acceso de mínimo privilegio

**Resultado:** consultar las Guide Pages correctas, explicar el plan y corregir un fallo de acceso sin ampliar permisos innecesariamente.

- Implementar un listado por path, tipo y tag con límite/paginación; usar un dataset suministrado con páginas incluidas, excluidas y no visibles para la identidad de prueba.
- Comparar consulta y plan antes/después; justificar el índice existente. Revisar un ejemplo de definición Cloud; crear uno sólo si el caso demuestra que hace falta.
- Configurar mediante Repo Init la identidad y ACL de una pequeña operación técnica suministrada, y conectar su subservice mapping. El listado del visitante conserva la identidad que exige su contrato.
- Demostrar lectura permitida, lectura excluida y ausencia de escritura donde no corresponde; distinguir permiso insuficiente de mapping ausente.

**Para compartir si se desea feedback:** PR o diff, consulta, plan, tabla identidad/ruta/operación/resultado y comprobación de regresión. **Demo del viernes:** un resultado correcto, un caso negativo y la causa del fallo original, mostrados por un voluntario o por el instructor. La autoevaluación considera el resultado y el plan, no sólo milisegundos o la presencia de un índice.

### Práctica 7 · Entregar una guía y corregir contenido ausente o desactualizado

**Resultado:** servir una Guide Page con sus dependencias desde Publish a través del Dispatcher local y justificar la política de caché.

- Publicar página y fragmento/asset del escenario; comprobar el destino.
- Validar una petición permitida y otra bloqueada, más una regla concreta de redirect o rewrite.
- Observar hit/miss y actualización tras un cambio; resolver un incidente sembrado durante la semana.
- Leer el caso CDN suministrado y señalar qué se comprobó localmente y qué sólo se deduce de evidencia Cloud. Incluir un caso de contenido que no debe entrar en caché compartida.

**Evidencia:** configuración y comandos HTTP reproducibles, encabezados, resultado antes/después y diagnóstico por capa. **Demo:** reproducir el síntoma, mostrar la corrección y una petición de control. La configuración local de replicación no se presenta como una reproducción del servicio Cloud.

### Práctica 8 · Preparar y diagnosticar una entrega compatible con Cloud

**Resultado:** ubicar un fallo en el flujo de entrega y producir una corrección verificable sin requerir un despliegue real.

- Analizar un paquete de evidencia suministrado: commit, tipo de pipeline, log de fallo, configuración declarada y estado del servicio.
- Corregir un problema de build, paquete o configuración reproducible en el SDK; separar causa de mensajes derivados.
- Documentar valores versionados, variables y referencias de secretos sin credenciales reales.
- Demostrar compatibilidad con el contenido anterior del fixture y explicar recuperación y herramienta de inspección elegida.

**Comprobaciones sugeridas:** PR o diff, comando local y resultado, diagnóstico, mapa commit → pipeline → destino y límite de lo demostrado. **Demo:** primer error accionable y corrección; no simular haber usado Cloud Manager. Al cerrar esta semana el instructor presenta el alcance del caso integrador final; quien quiera una ampliación personal puede elegirla sin compromiso de entrega.

### Práctica 9 · Una actualización asíncrona que tolera fallos

**Resultado principal:** un Sling Job en Author actualiza de forma controlada un dato del escenario, con un servicio HTTP local simulado y un efecto verificable al repetir la operación.

- Partir de un esqueleto suministrado; completar timeout, error transitorio y operación repetida con la misma clave de negocio.
- Usar el subservice de mínimo privilegio y rutas del ejercicio. Verificar progreso/estado según el diseño; no almacenar el estado duradero sólo en memoria.
- Mostrar éxito, fallo transitorio y repetición sin duplicar el efecto. Declarar el límite de la prueba local; no afirmar que demuestra coordinación de todo un clúster.
- Como evidencia secundaria breve, inspeccionar **uno** de los casos preparados de MSM o referencias CF y explicar el impacto de modificar su fuente. No implementar dos subsistemas nuevos adicionales.

**Evidencia:** PR, secuencia de intentos/resultado, prueba del efecto repetido y decisión de contenido. **Demo:** provocar un fallo y recuperarlo de manera controlada. Quedan fuera pagos, grandes importaciones, endpoints externos reales y automatización de publicación masiva.

### Práctica 10 · Proteger el incremento con pruebas y una mejora medida

**Resultado:** una regresión relevante es detectable y una deficiencia concreta de accesibilidad, SEO o rendimiento queda corregida.

- Extender una prueba unitaria existente con un caso negativo que falle sin la corrección.
- Añadir una comprobación real de HTTP/repositorio para algo que AEM Mocks no pueda probar y automatizar un único recorrido UI crítico.
- Revisar teclado/foco y metadatos del recorrido; medir un problema de carga/consulta/render bajo condiciones comparables.
- Corregir el hallazgo prioritario y mantener los demás como riesgos explícitos si exceden el alcance acordado.

**Evidencia:** pruebas ejecutadas, checklist breve, medición comparable y diff. **Demo:** regresión antes/después y razón para elegir cada nivel de prueba. No se pide un framework nuevo, una suite completa ni una cifra arbitraria de cobertura.

### Práctica 11 · Caso integrador opcional

**Resultado:** conectar las capas del caso Weekend Guides y explicar un diagnóstico completo, sobre el ejemplo suministrado o una implementación propia voluntaria.

- Partir del ejemplo suministrado o del proyecto personal; no comenzar una aplicación nueva.
- Explorar el incidente acotado publicado el lunes y, opcionalmente, intentar una variación de requisito.
- Si se desea feedback, compartir antes del viernes el diff, la traza, las comprobaciones y la duda concreta; no hay entrega obligatoria.
- Quien quiera presentar puede llevar una demo breve o una grabación; el instructor prepara una demo completa para asegurar el cierre aunque no haya voluntarios.

**Autoevaluación:** poder seguir la traza, reproducir un resultado y explicar una decisión; pedir ayuda forma parte del aprendizaje. **Demo del viernes:** resultado visible, decisión técnica y comprobación útil. No hay examen, calificación, defensa individual ni requisito de implementar todos los mecanismos vistos.

## Viernes y feedback voluntario

Los viernes 25 de septiembre, 2, 9, 16 y 23 de octubre duran entre 30 y 60 minutos. El formato de 30 minutos reserva 5 para recap, 15 para demos y 10 para preguntas y feedback; el formato de 60 reserva 10, 30 y 20 minutos respectivamente. Se elige según las demos y dudas disponibles. Participan voluntarios si los hay; no se impone rotación ni entrega. Si nadie hizo la práctica o quiere presentar, el instructor demuestra el caso preparado, incluido un fallo y su corrección. No se estrenan temas ni requisitos.

Para el **30 de octubre**, el formato de 30 minutos usa 5 de recap global, 15 de demo integradora o demos voluntarias, 5 de preguntas y 5 de retrospectiva. Si se utilizan los 60 minutos reservados, distribuir 5 de recap, 30 de demos, 15 de preguntas y 10 de retrospectiva. No se exige que las seis personas presenten; si todas quieren, el bloque de 30 minutos permite seis demos breves de 5 minutos. Cualquier material adicional se comparte opcionalmente sin superar la hora.

No se asignan notas ni niveles de desempeño. Las preguntas, ejemplos y comprobaciones sirven para autoevaluación y feedback descriptivo a quien lo solicite. La ausencia de práctica o demo no tiene consecuencias académicas ni impide seguir el curso.

## Preparación que requiere el nuevo diseño

| Antes de | Preparación del instructor | Dependencia y límite |
| --- | --- | --- |
| Semana 6 | Fixture de Guide Pages y tags; query costosa y corregible; usuarios/rutas del ejercicio y servicio técnico mínimo. | Repositorio real para ACL/plan. Si el baseline carece de un índice útil, preparar el fixture o índice de laboratorio antes; no prometer que el mismo plan existe en todos los SDK. |
| Semana 7 | Instrucciones de Publish local, Dispatcher Tools/contenedor, contenido dependiente y casos de caché; ejemplos de headers/logs CDN identificados como reales o sintéticos. | Preparar la demo local del instructor. El entorno de participantes sólo se necesita si eligen ejecutar la práctica; un análisis de logs no se presenta como ejecución Cloud. |
| Semana 8 | Documentación pública, diagramas y caso sintético coherente de pipeline/configuración/runtime, más fallo reproducible localmente. | El instructor no tiene Cloud Manager. No planear capturas nuevas ni demos en vivo de Cloud/RDE; usar material público o evidencia existente autorizada. |
| Semana 9 | Job mínimo, stub HTTP controlable y casos pequeños de contenido localizado/relacionado. | Mantener una sola implementación central; la revisión de arquitectura reutiliza fixtures. |
| Semana 10 | Una herramienta UI acordada, fixture estable y comandos de test/medición del baseline. | Ejecutar pruebas antes de asignarlas; una prueba local no demuestra el gate Cloud. |
| Semana 11 | Ejemplo integrador completo, incidente acotado y demo preparada; espacio para voluntarios. | El cierre funciona sin prácticas entregadas. No hay seis demos obligatorias ni defensa final. |

No se han generado todavía estos fixtures, las clases 26–55 ni sus diapositivas. Son trabajo de preparación posterior a adoptar la secuencia, no evidencia de aprendizaje ya disponible.

## Temas que no convertiría en bloques obligatorios

EDS/Universal Editor, Forms, Commerce, administración profunda de Assets, Dynamic Media, conectores de traducción, configuración avanzada de redes/CDN y desarrollo de rollout actions merecen recorridos propios. En este curso se reconoce su frontera cuando corresponde; no se agregan por disponibilidad de semanas. Assets y localización sí se profundizan en los puntos necesarios para los casos Sites existentes.

GraphQL merece especial cuidado: el alcance original lo excluye y su uso laboral no está confirmado. Queda como lectura opcional fuera de las 55 sesiones. Si posteriormente se confirma una necesidad concreta, se diseña una ampliación específica; no se sobrecarga ahora la sesión 44 ni el viernes.

## Archivos a sincronizar al adoptar la propuesta

Actualizar la portada, el temario público, el temario detallado, las prácticas 6–11 y las instrucciones de cierre. Retirar de las reglas generales las entregas obligatorias, calificaciones, niveles de desempeño y defensas; sustituir el seguimiento evaluativo por feedback voluntario. Revisar las referencias a “7 semanas”, “35 sesiones”, “7 prácticas” y “2 de octubre”, y expresar la duración como “30–60 minutos”. Extender la regla de viernes sin slides a las sesiones 40, 45, 50 y 55. Mantener estable la URL existente `eight-week-syllabus.html` aunque su nombre histórico ya no refleje la duración.

El contenido de las semanas 1–5, sus lecciones, imágenes, resúmenes y prácticas queda congelado. Los bloques futuros del documento de contenido listo para slides se deben reemplazar o marcar como pendientes para evitar enseñar la antigua secuencia. Actualizar la planificación no significa declarar listas las diapositivas ni los ejemplos nuevos.

**Base de la revisión:** temario y prácticas locales enlazados al inicio, sesiones 16–24 y documentación oficial citada junto a cada decisión técnica. La secuencia, carga y distribución de prácticas son recomendaciones pedagógicas para este equipo, no un currículo prescrito por Adobe.
