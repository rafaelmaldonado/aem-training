# Práctica 9 · Solución del instructor sobre el ejemplo de la sesión 41

**Material interno del instructor.** El enunciado para participantes no enlaza este directorio. Los participantes trabajan con los seis archivos que ya recibieron en la sesión 41; no reciben un starter nuevo.

La extensión cambia **tres archivos existentes** del proyecto local:

| Archivo de la sesión 41 | Sustitución de referencia |
| --- | --- |
| `GuideBatchJobConsumer.java` | [Consumidor para 300 Guides](instructor/core/src/main/java/com/adobe/aem/guides/wknd/core/training/GuideBatchJobConsumer.java) |
| `GuideBatchJobConsumerTest.java` | [Prueba de lotes, reintento y replay](instructor/core/src/test/java/com/adobe/aem/guides/wknd/core/training/GuideBatchJobConsumerTest.java) |
| `RepositoryInitializer~training-session-41.cfg.json` | [ACL ampliada sólo bajo `/guides`](instructor/ui.config/src/main/content/jcr_root/apps/wknd/osgiconfig/config.author/org.apache.sling.jcr.repoinit.RepositoryInitializer~training-session-41.cfg.json) |

`QueueGuidesProcess.java`, el service-user mapping, la configuración de la cola `ORDERED`, el workflow model y el launcher **son exactamente los de la sesión 41**. Conserva el topic, el subservice y el payload `/content/session-41-demo/control`. Instala la versión nueva de Repo Init antes de ejecutar el job para que el service user pueda crear nodos bajo `/guides`.

## Demo de recuperación

1. Parte de la fixture de la sesión 41 con `requestedVersion=v0`. Si ya ejecutaste la práctica, deshabilita el launcher, borra sólo los `guide-0001`…`guide-0300` y las propiedades `processedVersion`, `completed`, `lastGuide` del nodo `/guides`; conserva `guide-a` y `guide-b`. Vuelve a habilitar el launcher.
2. Cambia `requestedVersion` a `v1` en `/content/session-41-demo/control`. El launcher `Modified` inicia el mismo modelo y el Process Step encola el mismo topic de Sling Job.
3. El consumidor crea 25 nodos por commit y persiste `processedVersion`, `completed` y `lastGuide` en `/guides` con cada lote. Tras `guide-0100` devuelve `FAILED` en el primer intento. La cola espera 10 segundos y lo reintenta; los 100 existentes se omiten y el avance llega a `300`.
4. Inicia manualmente el mismo workflow con el mismo payload. Los 300 nodos numerados permanecen únicos, `applyCount=1` y el replay no hace commits adicionales. Los dos nodos originales `guide-a` y `guide-b` siguen presentes: en total hay **302** hijos bajo `/guides`, de los cuales **300** son `guide-0001`…`guide-0300`.

La respuesta inmediata que se observa es el final del **Process Step al encolar**, no una respuesta HTTP de una página. Inspecciona Workflow Instances/Archive, `/system/console/slingevent`, el log `Week 9` y `/content/session-41-demo/guides`. No se añade componente, servlet ni clientlib.

## Verificación realizada

`QueueGuidesProcess.java` de la sesión 41 y el consumidor/prueba de esta carpeta compilaron con Java 11 y AEM SDK API `2025.3.19823.20250304T101418Z-250300`. La prueba de 300 nodos, checkpoint en 100, reanudación y replay pasó mediante un ejecutor local; Maven compiló las pruebas, pero el plugin Surefire no pudo ejecutarlas sin red porque faltaba una dependencia de ese plugin en la caché. El JSON de Repo Init pasó validación sintáctica. El launcher, los permisos efectivos y la cola aún requieren comprobarse en Author SDK local.
