# Sesión 41 · Hacer una tarea asíncrona reintentable

**Lunes 12 de octubre de 2026 · Semana 9 · 30 minutos**

[Versión HTML](session-41-study-guide.html) · [Slides en inglés](../lessons/0041-retryable-asynchronous-work.html#slide-deck) · [Demo local y archivos copiables](examples/session-41/README.md)

**Código:** [Process Step](examples/session-41/core/src/main/java/com/adobe/aem/guides/wknd/core/training/QueueGuidesProcess.java) · [Sling Job consumer](examples/session-41/core/src/main/java/com/adobe/aem/guides/wknd/core/training/GuideBatchJobConsumer.java) · [prueba y tres configuraciones](examples/session-41/README.md#código-y-configuración-del-ejemplo). El modelo y el launcher se crean en Author siguiendo ese README.

## Objetivo observable

En un Author SDK local, seguir **un cambio de repositorio → launcher → workflow → Sling Job → dos actualizaciones de contenido**, observar un fallo controlado después del primer lote, comprobar el reintento y repetir la operación sin duplicar el efecto. El grupo debe poder decir qué estado permitió reanudar y por qué la escritura del job no inició otro workflow.

La sesión 23 presentó las tres piezas por separado. En las slides 2–6 se explican sus responsabilidades, la entrega al menos una vez, la idempotencia, los resultados del job y los checkpoints. La slide 7 aplica esas ideas en una demo real de AEM local; la 8 verifica la prevención de bucles. La sesión 42 estudiará HTTP saliente, timeouts y credenciales: **esta sesión no necesita un servidor HTTP externo**. Tampoco requiere Cloud Manager, RDE ni Publish.

## Seis ideas para recordar

1. El **launcher** observa sólo `/content/session-41-demo/control`; el **workflow** encola la operación; el **Sling Job** ejecuta y reintenta el trabajo. Que el workflow llegue a End sólo demuestra que terminó el paso de envío.
2. Sling Jobs ofrece procesamiento **al menos una vez**. El consumidor lee el estado antes de escribir porque puede recibir la misma operación de nuevo.
3. La identidad estable es la pareja **fixture + versión**. El Job ID identifica una entrega, no el efecto de negocio.
4. Cada Guide es un lote pequeño. `processedVersion` y `applyCount` se confirman juntos; el siguiente intento salta el lote ya confirmado.
5. `FAILED` solicita otro intento según la cola; `OK` termina; `CANCEL` evita repetir datos o configuración inválidos. El ejemplo introduce `FAILED` deliberadamente tras el primer commit.
6. El job escribe bajo `/guides`; el launcher mira `/control`. Esa separación evita que la propia escritura del consumidor vuelva a disparar el workflow.

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–4 | 1–2 | Plantear la meta y las responsabilidades de launcher, workflow y job. |
| 4–9 | 3–4 | Explicar entrega al menos una vez e idempotencia. |
| 9–15 | 5–6 | Comparar resultados del job, política de cola y checkpoints durables. |
| 15–25 | 7–8 | Ejecutar el demo local y verificar replay y prevención de bucles. |
| 25–28 | 9 | Recuperar las cinco conclusiones. |
| 28–30 | 10 | Preguntas y cierre. |

## Caso guiado · Dos Guides en Author

La [fixture local](examples/session-41/README.md) crea `/content/session-41-demo/control` y `/content/session-41-demo/guides/{guide-a,guide-b}`. El instructor cambia `requestedVersion` de `v0` a `v1` **después** de preparar el modelo y el launcher. El launcher sólo coincide con el nodo `control` y la condición `requestedVersion==v1`. El Process Step encola un job con `version=v1`; el consumidor usa un service user de escritura limitado a las propiedades bajo `/guides`.

| Momento | `guide-a` | `guide-b` | Resultado del job |
| --- | --- | --- | --- |
| Antes | Sin `processedVersion` | Sin `processedVersion` | Pendiente. |
| Intento 0 | Guarda `v1`, `applyCount=1` | Sin cambio | `FAILED` inyectado **después** del commit de `guide-a`. |
| Intento 1 | Lee `v1` y salta | Guarda `v1`, `applyCount=1` | `OK`. |
| Replay manual | Lee `v1` y salta | Lee `v1` y salta | `OK`; ambos contadores siguen en `1`. |

No se simula una caída real ni un HTTP `503`: se devuelve `FAILED` de manera controlada para poder enseñar el mismo punto de reanudación. `getRetryCount()` vale cero en la primera ejecución; la cola de esta demo admite dos reintentos, separados por diez segundos. La prueba de que el efecto no se duplicó está en las propiedades persistidas de los Guides, no en que el workflow aparezca archivado. [Job y retry count — Apache Sling](https://sling.apache.org/apidocs/sling9/org/apache/sling/event/jobs/Job.html) · [Colas y resultados — Apache Sling](https://sling.apache.org/documentation/bundles/apache-sling-eventing-and-job-handling.html).

### Qué hace idempotente la escritura local

Antes de actualizar cada Guide, el consumidor compara `processedVersion` con la versión del job. Si ya es `v1`, no escribe. Si difiere, guarda `processedVersion=v1` y suma uno a `applyCount` **en el mismo commit del nodo**. El siguiente intento vuelve a leer el repositorio y continúa donde quedó. Una marca separada del efecto o sólo en memoria no serviría. La cola `ORDERED` evita concurrencia entre estos jobs del ejemplo, pero otro escritor externo seguiría requiriendo coordinación adicional. [Guías de tareas Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/development-guidelines#background-tasks-and-long-running-jobs).

El launcher observa `/control`; el job sólo modifica `/guides/guide-a` y `/guides/guide-b`. Una nueva instancia de workflow causada por esas escrituras indicaría una regla más amplia u otro launcher coincidente. Esta separación es la comprobación concreta de prevención de bucles. [Launchers — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-65/content/sites/administering/operations/workflows-starting#creating-a-launcher-configuration).

## Demo del instructor · 7–9 minutos en el SDK local

Prepara el código, la cola, el service user, el modelo y el launcher **antes** de la reunión siguiendo [las instrucciones completas y los archivos copiables](examples/session-41/README.md). Usa WKND como ruta exacta; para Archetype adapta package Java, raíz `/apps` y Bundle-SymbolicName como indica el README. Este repositorio de formación no contiene el proyecto Maven ni una instancia AEM en ejecución, por lo que los resultados siguientes son **esperados, no una ejecución registrada**.

1. Abre la fixture en CRXDE Lite: `control/@requestedVersion=v0`; ambos Guides aún no tienen `processedVersion` ni `applyCount`.
2. Cambia `requestedVersion` a `v1` y guarda. Localiza la instancia de `Training queue Guide batches` en Workflow y confirma que el payload es `/content/session-41-demo/control`.
3. En `error.log`, correlaciona el Job ID: `queued`, `applied=guide-a`, `deliberate failure`, y tras ~10 segundos `skip=guide-a`, `applied=guide-b`, `complete`.
4. Comprueba en CRXDE Lite que ambos Guides tienen `processedVersion=v1` y `applyCount=1`.
5. Inicia **manualmente el mismo workflow** con el mismo payload para reproducir la operación. El log muestra `skip` para ambos; los contadores permanecen en `1`.
6. Confirma que no apareció una instancia adicional iniciada por la escritura bajo `/guides`. Si aparece, inspecciona la ruta y condiciones del launcher.

Si el launcher no inicia nada, comprueba primero su evento `Modified`, tipo `nt:unstructured`, ruta exacta, condición `requestedVersion==v1` y run mode Author. Si el workflow termina pero no cambian los Guides, busca el job por ID y revisa consumidor, topic, service mapping y ACL. El [README](examples/session-41/README.md) contiene la tabla completa de diagnóstico y los pasos de restablecimiento.

## Repaso con respuestas

1. **¿Qué demuestra un workflow en Archive?** Que completó sus pasos; no que el Sling Job ya terminó de modificar las dos Guides.
2. **¿Por qué vuelve a mirar `guide-a` el intento 1?** El trabajo se reentrega después de `FAILED`; debe leer el checkpoint persistido y reconocer que ese lote ya quedó confirmado.
3. **¿Por qué `applyCount` no llega a 2 en el replay?** La comparación de `processedVersion` evita una segunda escritura para la misma versión.
4. **¿Dónde está el checkpoint?** En `processedVersion` de cada Guide, guardado junto con el efecto observable de ese lote.
5. **¿Qué evita el bucle del launcher?** La regla observa sólo `/control` y el job escribe sólo bajo `/guides`.
6. **¿Por qué no basta la cola `ORDERED` para prometer exactamente una vez?** Coordina estos jobs, pero la entrega puede repetirse tras un fallo y otros escritores podrían modificar el mismo contenido.

## Fuentes oficiales

- [Apache Sling Eventing and Job Handling](https://sling.apache.org/documentation/bundles/apache-sling-eventing-and-job-handling.html)
- [Job.getRetryCount — Apache Sling](https://sling.apache.org/apidocs/sling9/org/apache/sling/event/jobs/Job.html)
- [AEM Cloud Development Guidelines — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/development-guidelines)
- [Starting Workflows y launchers — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-65/content/sites/administering/operations/workflows-starting)
- [Service Users — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/developing/advanced/service-users)
