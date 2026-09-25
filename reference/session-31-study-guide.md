# Sesión 31 · Trazar una publicación hasta Publish

**Lunes 28 de septiembre de 2026 · Semana 7 · Núcleo de 30 minutos, ampliable a 60**

[Versión HTML](session-31-study-guide.html) · [Slides en inglés](../lessons/0031-check-publication.html#slide-deck) · [Demo local](#demo-local)

## Objetivo observable

Ante una página que cambió en Author pero no refleja el cambio en Publish, reconstruir **la ruta de un path concreto**: acción y destino, alcance y referencias, estado de replicación, colas de distribución y recurso en Publish. El resultado es un diagnóstico con la primera capa que falta y la evidencia que lo respalda. La sesión termina en Publish; la petición que atraviesa Apache y Dispatcher se estudia en la sesión 32.

El instructor proporciona una página, un asset y las capturas de estado de Cloud. No hace falta una práctica previa ni acceso a Cloud Manager. El ejemplo de Author y Publish locales muestra el efecto observable, pero su agente clásico no reproduce las colas de Sling Content Distribution (SCD) de Cloud. [Replicación en AEM Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/replication) · [SDK local — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/aem-runtime).

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–4 | 1–2 | Formular el incidente como un path, un destino y una versión esperada. |
| 4–10 | 3–5 | Seguir SCD, sus dos colas y el grafo de dependencias. |
| 10–16 | 6–8 | Preparar el cambio y leer correctamente `ReplicationStatus` por agente. |
| 16–26 | 9–10 | Resolver una cola pendiente y contrastarla con la demo local. |
| 26–30 | 11–12 | Decidir si el problema sigue en publicación o pasa a la sesión 32. |

Si se dispone de 60 minutos, añade 20 de ejecución guiada en Author/Publish local y 10 de discusión del caso de cola. La extensión profundiza la misma capacidad, sin tareas obligatorias.

## 1. Cuatro puntos de control para un path

```text
Author: acción, destino y paths seleccionados
  → SCD: solicitud aceptada y encolada
  → Publish: contenido importado en el destino
  → Comprobación: el path sirve la versión esperada
```

En Cloud, SCD mueve el contenido a través de un servicio externo al runtime AEM. El agente `publish` está habilitado por defecto; `preview` dirige al entorno de Preview cuando está configurado. Una notificación de que se inició la publicación no demuestra que el último punto de control haya concluido. [Replicación en AEM Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/replication).

La selección de paths importa. Quick Publish publica las páginas seleccionadas de forma superficial y puede añadir referencias no publicadas. Manage Publication permite revisar páginas hijas, referencias, destino, acción y programación. Antes de confirmar, anota el path de la página y de cada referencia incluida. Una imagen compartida puede servir a otras páginas; despublicarla por error cambia más que la página bajo diagnóstico. [Publicación desde Sites — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/authoring/sites-console/publishing-pages).

## 2. Dos colas con significados distintos

En **Tools → Deployment → Distribution → publish**, el agente presenta dos colas consolidadas; no hay una cola por cada pod de Publish:

| Cola | Si el elemento sale de la cola | Qué revisar si permanece pendiente |
| --- | --- | --- |
| `persisted` | El cambio quedó almacenado de forma duradera en el nivel Publish; los pods convergen con el tiempo. | Path de *Items Pending*, estado, último elemento procesado y log del agente. |
| `fully published` | El cambio está activo en todos los pods de Publish; la invalidación asociada termina para los paths afectados. | Path pendiente, diferencia entre último elemento procesado y la acción esperada, log del agente. |

La consola muestra **Items Pending**, **Last Item Processed**, **Test Connection** y **Logs**. Si una cola aparece roja, registra el primer path que la bloquea y su error antes de intervenir. Vaciar una cola destruye evidencia y puede descartar cambios de otras personas; en esta clase sólo se inspecciona. [Colas y monitorización — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/replication#replication-queues).

No uses el estado de Sites como sustituto de esta inspección. Tampoco infieras que un path está disponible por un solo timestamp: necesitas ubicar la acción en la ruta y, finalmente, verificar el recurso en el destino.

## 3. Leer `ReplicationStatus` sin prometer más de lo que sabe

La Replication API sigue disponible en Cloud. Para **un** recurso puede adaptarse a `ReplicationStatus`; para muchos recursos Adobe recomienda `ReplicationStatusProvider.getBatchReplicationStatus(...)`. El siguiente fragmento es una lectura de diagnóstico, no un servlet ni una operación de publicación:

```java
Resource page = resolver.getResource(pagePath);
ReplicationStatus status = page == null ? null : page.adaptTo(ReplicationStatus.class);
ReplicationStatus live = status == null ? null : status.getStatusForAgent("publish");
if (live != null) {
    LOG.info("action={}, pending={}, delivered={}",
        live.getLastReplicationAction(), live.isPending(), live.isDelivered());
}
```

`isActivated()` indica que la última acción fue Activate; **no** dice que todas las etapas hayan terminado. `isPending()` indica que la última acción todavía está en alguna cola. `isDelivered()` se calcula desde los logs de acciones de replicación y **no comprueba que el contenido exista físicamente en el servidor**. Un `null` exige revisar si hay recurso o estado del agente; no se transforma en “despublicado”. [ReplicationStatus — Javadoc de Adobe](https://developer.adobe.com/experience-manager/reference-materials/cloud-service/javadoc/com/day/cq/replication/ReplicationStatus.html) · [Replicación en Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/replication#replication-api).

El estado general se actualiza cuando participa un agente habilitado por defecto. Una publicación **sólo a Preview** puede dejar `status.isActivated()` sin cambio. Consulta `getStatusForAgent("preview")` o `getStatusForAgent("publish")` para el destino concreto y comprueba su URL por separado. Que el editor de Author esté en modo Preview no equivale a publicar al servicio Preview. [Estado por agente — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/replication#replication-api) · [Preview de Sites — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/authoring/sites-console/previewing-content).

## 4. Caso guiado de cola en Cloud

**Evidencia didáctica simulada, no un incidente real ni una captura del entorno del equipo.** Se solicitó Activate a `publish` para `/content/wknd/us/en/training-publication` a las 10:04. La selección también incluía `/content/dam/wknd/training/cover.png`.

| Señal suministrada | Lectura |
| --- | --- |
| Estado de la página: última acción Activate; `isPending() = true` | Existe una acción pendiente; `isActivated()` por sí solo no resolvería el incidente. |
| Cola `persisted`: 1 elemento pendiente, path del asset | Buscar ese path y el primer error en Logs. No atribuir todavía el fallo a la página o al navegador. |
| Cola `fully published`: 1 elemento pendiente | La ruta todavía no llegó a la confirmación final para todos los pods. |
| Página de Publish todavía muestra la versión anterior | Es coherente con distribución pendiente; aún no prueba un problema de Dispatcher. |

**Pregunta al grupo:** ¿qué evidencia buscarías después? Respuesta: abre el elemento pendiente del asset, registra el path y el error asociado en Logs; revisa si *Last Item Processed* avanza. Una falla del import de una referencia puede bloquear trabajos posteriores. No borres la cola para “probar” sin diagnóstico y coordinación. [Monitorización y resolución — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/replication#troubleshooting).

**Segundo corte del caso:** ambas colas quedan sanas y sin elementos pendientes, y la versión nueva ya aparece en Publish. Si una URL pública aún responde con contenido anterior, la publicación hasta Publish quedó demostrada; lleva la petición y sus encabezados a la sesión 32. No se enseña configuración de Dispatcher aquí.

<a id="demo-local"></a>

## 5. Demo local: la misma pregunta, otro transporte

**Preparación del instructor.** Usa Author desechable en `http://localhost:4502` y Publish desechable en `http://localhost:4503`, con el mismo proyecto WKND o Archetype instalado. Conecta ambas instancias siguiendo la [guía oficial del SDK](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/aem-runtime). El agente local hacia `/bin/receive` reproduce la publicación local, no las dos colas consolidadas de SCD en Cloud. Ten preparada una página de prueba y un asset propio, sin cambiar contenido compartido.

1. Anota los paths reales de la página y del asset. Si existe el árbol WKND, puedes usar una hija bajo `/content/wknd/us/en/`; no presupongas que todos los proyectos tienen esa ruta. Inserta el asset en la página. Publica la página con una marca visible **Versión A** y comprueba ambos paths en Publish `:4503`.
2. En Author cambia la marca a **Versión B**. Antes de publicar, compara la modificación con la última publicación en Sites y abre el mismo path en Publish: allí debe seguir **Versión A**.
3. En Author abre **Manage Publication → Publish → Now**. Revisa y anota la página, el asset incluido, el destino y la hora. Confirma. Si el asset no aparece entre las referencias, comprueba cómo está enlazado y añádelo explícitamente si el ejemplo lo necesita.
4. Inspecciona el estado de la página en Sites. En el SDK local comprueba el agente de Author y su cola local siguiendo la guía del SDK; **no presentes esa pantalla como SCD Cloud**. Abre de nuevo los paths de la página y del asset en Publish `:4503` y comprueba **Versión B**.
5. Si el tiempo alcanza, despublica **sólo la página de prueba**, conserva el asset compartido y verifica que Author mantiene la página mientras Publish deja de servirla.

| Evidencia mínima a guardar | Ejemplo de registro |
| --- | --- |
| Acción y destino | Activate → publish, no preview. |
| Paths del alcance | Página y asset con rutas completas. |
| Hora y estado en Author | Última acción, pendiente o no, fecha de modificación. |
| Transporte | Agente/cola local; en Cloud, agente SCD y dos colas. |
| Resultado en Publish | URL exacta, versión visible y asset. |

**Resultados esperados, no ejecución registrada en este repositorio.** Si Publish `:4503` muestra la versión correcta, el tramo de publicación local funcionó. Si no la muestra, inspecciona acción, path, referencia, agente y logs antes de mirar una URL pública. En Cloud, la cola `fully published` es una señal adicional que el SDK local no reproduce. [SDK local — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/aem-runtime) · [SCD y colas — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/replication#replication-queues).

## 6. Diagnóstico al cierre

| Evidencia | Primera hipótesis comprobable | Siguiente paso |
| --- | --- | --- |
| No hay acción para el path o el destino era Preview | Selección, destino o permiso de publicación. | Revisa Manage Publication y el estado por agente. |
| `isPending()` y path en `persisted` | Distribución/importación aún no termina. | Inspecciona primer elemento pendiente y Logs. |
| `persisted` despejada, `fully published` pendiente | La convergencia final no terminó. | Observa cola, último elemento y Logs; no republiques en bucle. |
| Colas sanas, asset ausente en Publish | La referencia pudo quedar fuera del alcance o fallar por separado. | Verifica el path del asset y su propio estado. |
| Página y asset correctos en Publish, URL pública distinta | Publicación hasta Publish demostrada. | Lleva la petición a la sesión 32: Apache y Dispatcher. |

## Repaso con respuestas

1. **¿Qué demuestra `isActivated()`?** Que la última acción fue Activate; no demuestra importación física ni respuesta correcta.
2. **¿Qué diferencia hay entre `persisted` y `fully published`?** La primera confirma almacenamiento duradero en Publish; la segunda confirma disponibilidad en todos los pods y finalización del tramo de publicación.
3. **¿Por qué importa el path del primer elemento pendiente?** Puede señalar el recurso que bloquea la cola, incluso si el síntoma se ve en otra página.
4. **¿Cómo distingues Preview de Publish en la API?** Con `getStatusForAgent("preview")` o `getStatusForAgent("publish")` y comprobando el destino elegido.
5. **¿Qué prueba el SDK local y qué no?** Prueba contenido servido por Publish local mediante el agente configurado; no reproduce las colas SCD de Cloud.
6. **Si Publish tiene la versión correcta y la URL pública no, ¿dónde continúa el curso?** En la sesión 32, siguiendo la petición por Apache y Dispatcher.

## Fuentes oficiales

- [Replicación, agentes, API y colas — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/replication)
- [ReplicationStatus — Javadoc de Adobe](https://developer.adobe.com/experience-manager/reference-materials/cloud-service/javadoc/com/day/cq/replication/ReplicationStatus.html)
- [Publicación y alcance en Sites — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/authoring/sites-console/publishing-pages)
- [Preview de Sites — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/authoring/sites-console/previewing-content)
- [SDK Author/Publish local — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/aem-runtime)
