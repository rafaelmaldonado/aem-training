# Sesión 41 · Demo integral en Author SDK local

Este ejemplo usa **sólo el AEM as a Cloud Service SDK local**. No llama a un servicio HTTP ni necesita Cloud Manager. Copia los archivos `core/` y `ui.config/` a las mismas rutas de tu proyecto AEM; no los instales desde este repositorio de formación, que no es un reactor Maven.

El ejemplo está preparado para WKND (`com.adobe.aem.guides.wknd.core.training`, bundle `wknd.core`, raíz `/apps/wknd`). Si usas un proyecto generado por Archetype, cambia el package Java, la ruta `/apps/<tu-proyecto>` y `wknd.core` por el **Bundle-SymbolicName** real. Conserva iguales el topic, el subservice y la ruta de la fixture en ambas clases y configuraciones. No añadas dependencias nuevas si tu proyecto ya incluye AEM SDK API, anotaciones OSGi, JUnit 5 y Mockito.

## Código y configuración del ejemplo

| Archivo | Función |
| --- | --- |
| [QueueGuidesProcess.java](core/src/main/java/com/adobe/aem/guides/wknd/core/training/QueueGuidesProcess.java) | Process Step que lee la versión y encola el Sling Job. |
| [GuideBatchJobConsumer.java](core/src/main/java/com/adobe/aem/guides/wknd/core/training/GuideBatchJobConsumer.java) | Consumidor que guarda cada Guide, reintenta y evita duplicados. |
| [GuideBatchJobConsumerTest.java](core/src/test/java/com/adobe/aem/guides/wknd/core/training/GuideBatchJobConsumerTest.java) | Prueba del fallo, la reanudación y el replay. |
| [Repo Init](ui.config/src/main/content/jcr_root/apps/wknd/osgiconfig/config.author/org.apache.sling.jcr.repoinit.RepositoryInitializer~training-session-41.cfg.json) | Crea la fixture, el service user y su ACL. |
| [Service user mapping](ui.config/src/main/content/jcr_root/apps/wknd/osgiconfig/config.author/org.apache.sling.serviceusermapping.impl.ServiceUserMapperImpl.amended~training-session-41.cfg.json) | Conecta el subservice con el principal. |
| [Sling Job queue](ui.config/src/main/content/jcr_root/apps/wknd/osgiconfig/config.author/org.apache.sling.event.jobs.QueueConfiguration~training-session-41.cfg.json) | Configura `ORDERED`, dos reintentos y 10 segundos de demora. |

El **modelo y el launcher** se crean en la interfaz de Author con los valores de «Preparación antes de la clase»; no hay archivos de modelo o launcher en este ejemplo.

## Qué se observa

```text
Editar requestedVersion=v1 en /content/session-41-demo/control
  → launcher Modified, sólo sobre /control
  → workflow Training queue Guide batches, Process Step con Handler Advance
  → JobManager añade training/session41/guides, version=v1
  → intento 0: guide-a guarda processedVersion=v1 y applyCount=1; devuelve FAILED
  → intento 1: guide-a ya está completo; guide-b guarda v1 y count=1; devuelve OK
  → replay manual del mismo workflow: ambos se omiten; ambos counts siguen en 1
```

La primera falla es **inyectada deliberadamente después del commit de `guide-a`**; no es un corte real de proceso. Cada Guide actúa como un lote pequeño: `processedVersion` y `applyCount` se guardan juntos en ese nodo. La cola `ORDERED` del ejemplo admite dos reintentos, separados por 10 segundos. El launcher sólo observa `/control`; el consumidor escribe bajo `/guides`, por lo que su escritura queda fuera de la ruta que dispara el workflow. Un workflow archivado prueba que terminó el paso de encolado; consulta el log y el contenido para confirmar el resultado del job.

## Preparación antes de la clase

1. Arranca Author SDK local en `http://localhost:4502` y confirma que tu baseline AEM construye e instala normalmente. Usa una copia local del proyecto; estos nombres y ACL son sólo para formación.
2. Copia los dos `.java` de `core/src/main/java/.../training/`, la prueba de `core/src/test/java/.../training/` y los tres `.cfg.json` de `ui.config/.../config.author/` a tu proyecto. El Repo Init crea `/content/session-41-demo`, `control`, `guides/guide-a`, `guides/guide-b` y el service user; su ACL permite leer `/content` y modificar propiedades **sólo** bajo `/content/session-41-demo/guides`. El mapping liga el subservice al bundle y la cola liga el topic a una cola ordenada. No uses esta fixture en Cloud.
3. Ejecuta `mvn -pl core -Dtest=GuideBatchJobConsumerTest test` en tu proyecto, o el comando equivalente de tu baseline. Después instala el paquete en Author; si tu POM define el perfil habitual, `mvn clean install -PautoInstallSinglePackage`.
4. En `http://localhost:4502/system/console/bundles` verifica el bundle activo y su `Bundle-SymbolicName`. En `/system/console/components` busca `QueueGuidesProcess` y `GuideBatchJobConsumer`. En `/system/console/configMgr` comprueba el mapping, Repo Init y la cola `Training Session 41`. Si no ves los nodos en CRXDE Lite, investiga Repo Init antes de crear el launcher.
5. En CRXDE Lite, bajo `/content/session-41-demo/control`, crea una propiedad String `requestedVersion` con valor `v0`. Comprueba que `guide-a` y `guide-b` no tienen `processedVersion` ni `applyCount`. Haz esta preparación **antes** de habilitar el launcher.
6. En **Tools → Workflow → Models → Create**, crea `Training queue Guide batches`. Edita el modelo: conserva Start y End, agrega un **Process Step**, selecciona `Training: queue Guide batches`, activa **Handler Advance**, deja Arguments vacío y conserva **Transient Workflow** desactivado para ver el historial. Pulsa **Sync**.
7. En **Tools → Workflow → Launchers → Create**, agrega un launcher de prueba: **Event Type = Modified**, **Nodetype = nt:unstructured**, **Path = /content/session-41-demo/control**, **Run Mode = Author**, **Condition = requestedVersion==v1**, **Workflow Model = Training queue Guide batches**, **Enabled = true**. No uses una ruta más amplia. Según la versión del SDK, el campo puede llamarse Path o Path/Glob; comprueba la ruta guardada en View Properties.
8. Para leer la secuencia en `crx-quickstart/logs/error.log`, configura un logger INFO local para `com.adobe.aem.guides.wknd.core.training` si esa categoría no aparece con el nivel actual. La [sesión 23](../../session-23-study-guide.html#ejemplos-locales) muestra los pasos del logger. Filtra por `Session 41`.

## Demo en vivo, 7–9 minutos

1. Muestra la fixture en CRXDE Lite: `requestedVersion=v0`; ambos Guides sin efecto.
2. Cambia **sólo** `/content/session-41-demo/control/@requestedVersion` a `v1` y guarda. En **Workflow → Instances/Archive**, localiza la instancia de `Training queue Guide batches` con payload `/content/session-41-demo/control`. Si el launcher no la inicia, revisa sus cinco campos antes de iniciar el modelo manualmente.
3. En el log, sigue el mismo job ID: `queued`, `applied=guide-a ... count=1`, `deliberate failure`, después de unos 10 segundos `skip=guide-a`, `applied=guide-b ... count=1`, `complete`. No afirmes que el workflow completó el efecto sólo porque llegó a End.
4. En CRXDE Lite, confirma `processedVersion=v1` y `applyCount=1` en **cada** Guide. La propiedad está persistida; no es un contador en memoria.
5. Para simular un replay con la misma clave, selecciona el modelo en **Workflow → Models → Start Workflow** y elige como payload `/content/session-41-demo/control`. En el log deben aparecer `skip=guide-a`, `skip=guide-b` y `complete` sin otra escritura. Los dos `applyCount` siguen en `1`.
6. Comprueba en Workflow que **no** apareció una instancia adicional por las escrituras bajo `/guides`. Es la prueba de que el launcher estrecho no forma un bucle.

| Si falla | Primera comprobación |
| --- | --- |
| No aparecen `control` o `guides` | Repo Init instalado y sintaxis de su configuración. |
| No aparece el proceso en el selector | Bundle, componente DS, `process.label` y Sync del modelo. |
| No arranca al cambiar `requestedVersion` | Launcher habilitado; evento Modified, tipo `nt:unstructured`, path exacto, condición y run mode Author. |
| Workflow llega a End, pero no hay efecto | Job encolado, consumidor activo, topic/cola y log del mismo job ID. |
| `service mapping failed` o fixture no escribible | `Bundle-SymbolicName`, subservice, principal y ACL bajo `/guides`. |
| No aparece el reintento | `queue.retries=2`, topic exacto, resultado `FAILED` y log tras 10 segundos. |
| Aparecen instancias extra | El launcher observa una ruta demasiado amplia o hay otro launcher coincidente. |

## Restablecer y límites

Para repetir desde cero en el SDK, deshabilita el launcher, borra `processedVersion` y `applyCount` en los dos Guides, pon `requestedVersion=v0` y vuelve a habilitar el launcher. Después repite la demo. Al terminar, deshabilita y elimina el launcher/modelo de formación y retira los archivos del proyecto local si ya no los necesitas. No cambies launchers de sistema.

**La ejecución en tu SDK no está registrada aquí.** El Java compiló con AEM SDK API `2025.3.19823.20250304T101418Z-250300` y anotaciones OSGi 1.5.0; las configuraciones JSON se validan en este repositorio. La prueba JUnit pasó (1 prueba, 0 fallos) y verifica el primer fallo, la reanudación y el replay con un resolver simulado. El SDK local aún debe confirmar que Repo Init, launcher, modelo, service mapping y cola se comportan como espera tu baseline. Una cola ordenada y un commit por item no prueban por sí solos coordinación de todos los escritores en un clúster.

Fuentes: [Sling Jobs y configuración de colas](https://sling.apache.org/documentation/bundles/apache-sling-eventing-and-job-handling.html), [Job.getRetryCount](https://sling.apache.org/apidocs/sling9/org/apache/sling/event/jobs/Job.html), [launchers](https://experienceleague.adobe.com/en/docs/experience-manager-65/content/sites/administering/operations/workflows-starting), [service users](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/developing/advanced/service-users) y [cola ORDERED en Author](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/developing/advanced/run-job-on-leader-instance-in-aem-author).
