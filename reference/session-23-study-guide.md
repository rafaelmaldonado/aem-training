# Sesión 23 · Diagnóstico del runtime y procesamiento asíncrono

**Resumen de preparación · Miércoles 16 de septiembre de 2026 · Español**

[Versión HTML](session-23-study-guide.html) · [Diapositivas](../lessons/0023-runtime-diagnostics-async-processing.html#slide-deck) · [Ejemplo Java y pasos en Author](#ejemplos-locales)

La sesión 22 separó el contenido de un paquete de su efecto al instalarse. La 23 continúa en la instancia en ejecución: el build puede terminar bien mientras un servicio no está disponible, un workflow espera a una persona o un job reintenta una operación. Cada caso tiene una explicación distinta y una vista que ayuda a comprobarla.

> **Síntoma → contexto → estado del responsable → causa → comprobación.** Una línea ERROR, un bundle Active o un workflow RUNNING no explican por sí solos todo el recorrido.

El resumen desarrolla los conceptos de las slides. Al final encontrarás un ejemplo pequeño con una sola clase Java y las instrucciones de consola para verlo funcionar; no necesitas construir otro componente ni depender del ejemplo de la sesión 18.

## Índice

1. [Localizar el síntoma](#sintoma)
2. [Leer logs con contexto](#logs)
3. [Bundle y componente DS](#osgi)
4. [Configuración efectiva](#configuracion)
5. [Workflow: modelo, payload e instancia](#workflow)
6. [Process Step y Participant Step](#pasos)
7. [Qué selecciona un launcher](#launcher)
8. [Sling Jobs y resultados](#jobs)
9. [Reintentos e idempotencia](#reintentos)
10. [Repaso con respuestas](#repaso)
11. [Ejemplo simple: Java, logger y workflow](#ejemplos-locales)
12. [Lectura de un launcher](#ejemplo-launcher)
13. [Glosario y fuentes](#fuentes)

<a id="sintoma"></a>

## 1. Localizar el síntoma

Empieza por precisar qué esperabas, dónde y cuándo. «AEM no funciona» puede describir una petición que falla, contenido que no se ha publicado o una tarea que todavía no ha empezado.

| Observación | Siguiente comprobación útil |
| --- | --- |
| Falta una implementación en el selector de Process Step. | Registro OSGi del servicio y su etiqueta. |
| El paso dejó una línea en el log, pero la ejecución sigue abierta. | Paso actual, historial y reglas de avance. |
| El resultado está bien en Author y falta en Publish. | Publicación y estado en la instancia afectada. |
| Una operación aparece repetida. | Identidad de ejecución, intentos y eventos que la iniciaron. |

Anota la instancia, una franja horaria y una ruta o identificador. A partir de esa información puedes reducir una búsqueda. Reiniciar todo antes de mirar puede borrar la oportunidad de reconocer el estado que causó el fallo.

<a id="logs"></a>

## 2. Leer logs con contexto

En el SDK, el log Java habitual está en `crx-quickstart/logs/error.log`. Su nombre no implica que contenga sólo errores: también puede incluir INFO, WARN y DEBUG según la configuración.

Lee la hora, el nivel, la categoría del logger y el mensaje. Para una excepción, conserva su cadena de causas y las líneas cercanas de la misma operación. La última excepción impresa puede ser sólo la envoltura de un error anterior. Dos líneas contiguas pueden venir de peticiones distintas.

En procesos asíncronos, el hilo de la petición inicial puede haber terminado. Un ID de workflow o job permite correlacionar mejor que suponer continuidad de hilo. Una ruta ayuda, pero varias ejecuciones pueden procesar esa misma ruta.

En Cloud, usa el acceso soportado a logs y considera el pod además de la instancia lógica. Los logs Java personalizados deben enviarse a `error.log` para quedar disponibles mediante Cloud Manager o Adobe I/O CLI; un archivo personalizado local no prueba esa disponibilidad. [Logs en AEM Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/debugging/debugging-aem-as-a-cloud-service/logs).

**En el ejemplo:** la clase registra ID de instancia, tipo y ruta del payload. No registra propiedades de contenido ni argumentos. Usa contenido ficticio; en una aplicación real selecciona identificadores que no expongan secretos o datos personales.

<a id="osgi"></a>

## 3. Bundle y componente DS son niveles diferentes

El bundle transporta clases y declara paquetes importados/exportados. Declarative Services administra componentes dentro de ese bundle. Ambos participan en el runtime, pero sus estados no son intercambiables.

| Nivel | Estado | Lectura inicial |
| --- | --- | --- |
| Bundle | Installed | Inspecciona si hay imports que impiden resolverlo. |
| Bundle | Resolved | Dependencias de paquetes resueltas; bundle no activo. Puede estar detenido deliberadamente. |
| Bundle | Active | Bundle iniciado; todavía hay que comprobar cada componente relevante. |
| DS | Unsatisfied | Revisa referencias obligatorias o configuración requerida. |
| DS | Satisfied | Dependencias satisfechas; un servicio diferido puede esperar a su primer consumidor. |
| DS | Active | El componente se activó; eso no garantiza que toda operación de negocio vaya a terminar bien. |

Un `@Reference` apunta a un servicio OSGi. Un import de paquete permite resolver clases. Si falta el primero, cambiar versiones de dependencias Java sin más evidencia no es una corrección demostrada.

**Vistas locales:** `/system/console/bundles` para el bundle, `/system/console/components` para el componente DS y sus referencias. Si falla una activación, acompaña el estado con el mensaje del log. Estas URL describen el SDK; no presupongas las mismas operaciones de consola en Cloud.

<a id="configuracion"></a>

## 4. Comprobar la configuración efectiva

El PID identifica la configuración de un componente o una factory. Una factory puede tener varias instancias, así que «encontré el PID» todavía no identifica qué valores usa el caso que estás mirando.

Sigue este orden: nombre del componente, PID o instancia de factory, run modes aplicables y propiedades actuales. Un `.cfg.json` correcto en Git no demuestra que esté instalado, seleccionado o libre de un override local. La configuración de un run mode más específico no debe interpretarse como una suma automática de campos del documento menos específico. [Configuración OSGi — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi).

El logger del ejemplo tiene tres datos visibles: categoría, nivel y archivo. `LogPayloadProcess` es la categoría de log; no es el factory PID de Sling LogManager. Cambiar el nivel no ejecuta la clase: sólo cambia qué mensajes futuros quedan registrados.

No eleves a DEBUG el logger raíz para encontrar una única clase. Una categoría estrecha permite leer su comportamiento sin inundar la salida de toda la instancia. [Configuración de loggers — Apache Sling](https://sling.apache.org/documentation/development/logging.html).

<a id="workflow"></a>

## 5. Workflow: modelo, payload e instancia

| Concepto | Ejemplo de esta sesión |
| --- | --- |
| Modelo | Definición `Training log payload`, con Start, Process Step y End. |
| Payload | Página seleccionada al iniciar el workflow. |
| Instancia | Una ejecución concreta sobre esa página. |
| Work item | Trabajo asociado al paso que se está ejecutando o atendiendo. |
| Historial | Registro de los pasos y acciones de esa ejecución. |

Guardar un cambio de diseño y ejecutarlo son operaciones distintas. **Sync** prepara el modelo de runtime; inicia una instancia nueva para observar la definición actualizada. Una instancia ya iniciada no se convierte automáticamente en una ejecución nueva por volver a pulsar Sync. [Modelo y runtime — referencia Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-65-lts/content/implementing/developing/extending-aem/extending-workflows/workflows).

Desde **Tools → Workflow**, Instances muestra ejecuciones en curso; Archive permite abrir historial; Failures reúne información para investigar fallos. Un proceso muy corto puede desaparecer de Instances antes de que abras la consola. Busca por modelo, payload y hora. En Archive también pueden aparecer terminaciones solicitadas por un usuario: estar archivado no basta para concluir que completó su objetivo. [Administrar instancias en Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/workflows-administering).

<a id="pasos"></a>

## 6. Process Step y Participant Step

Un **Process Step** ejecuta una implementación; un **Participant Step** asigna trabajo a una persona o grupo. Una instancia RUNNING puede estar esperando una decisión legítima, no necesariamente bloqueada por un error.

Para un proceso Java, AEM localiza el servicio `WorkflowProcess` por su registro OSGi y muestra su `process.label` en el selector. La opción **Handler Advance** permite avanzar cuando termina ese proceso; sin ella, la implementación tendría que gestionar el avance. [Process Step — referencia Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-65-lts/content/implementing/developing/extending-aem/extending-workflows/workflows-step-ref).

En nuestro ejemplo, `execute` sólo emite un mensaje. Por eso se activa Handler Advance y se deja al motor llevar la instancia a End. Si hubiera un Participant Step adicional, ver el log del proceso no demostraría que alguien completó la tarea humana.

<a id="launcher"></a>

## 7. Qué selecciona un launcher

Un launcher escucha cambios del repositorio y decide si debe iniciar un workflow. Combina el tipo de evento, tipo de nodo, ruta, condiciones y estado habilitado; su lista de exclusiones puede descartar ciertos cambios. [Launchers — referencia Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-65-lts/content/sites/administering/operations/workflows-starting).

```text
Evento del repositorio
  → ¿coinciden los criterios del launcher?
  → iniciar el modelo seleccionado
  → nueva instancia sobre el payload
```

Guardar una página puede producir varios eventos. Si el workflow modifica el mismo contenido que observa el launcher, puede volver a dispararlo. Limita el ámbito y comprende las exclusiones antes de habilitar una regla.

No confundas `Nodetype` con `sling:resourceType`: el primero es un tipo JCR; el segundo participa en la resolución Sling. Tampoco un launcher es un cron ni una implementación del proceso. La lectura paso a paso al final permite ver esos campos sin cambiar una regla instalada.

<a id="jobs"></a>

## 8. Sling Jobs: envío, cola y resultado

Un productor entrega un topic y propiedades serializables a `JobManager`; un consumidor registrado para ese topic procesa el trabajo. La cola separa el envío de la ejecución. El consumidor que usa `JobConsumer` devuelve uno de estos resultados:

| Resultado | Significado |
| --- | --- |
| `OK` | El consumidor terminó con éxito. |
| `FAILED` | Fallo que puede reintentarse según la política de la cola. |
| `CANCEL` | Fallo permanente; no solicitar otro intento de esa ejecución. |

La garantía de procesamiento es **al menos una vez**: la aplicación debe tolerar ejecuciones repetidas. Retardo, número de intentos y concurrencia son decisiones de configuración; devolver FAILED no promete reintentos infinitos. [Sling Eventing and Job Handling — Apache](https://sling.apache.org/documentation/bundles/apache-sling-eventing-and-job-handling.html).

Para diagnosticar, sigue el ID/topic, las propiedades necesarias, la cola, el consumidor disponible y el resultado. No pases el request ni un ResourceResolver abierto como si fueran datos persistibles de un trabajo futuro. Si luego hace falta acceder al repositorio, el consumidor debe gestionar su propio contexto de acceso autorizado.

**Comparación útil:** un workflow representa pasos y decisiones; un launcher decide cuándo iniciarlo por un evento; un Sling Job representa trabajo en cola. No son tres nombres para el mismo objeto, aunque una solución pueda relacionarlos internamente.

<a id="reintentos"></a>

## 9. Reintentos e idempotencia

Idempotencia significa que repetir la misma operación lógica no repite indebidamente su efecto de negocio. Volver a establecer el mismo estado y añadir otro elemento a una lista no tienen el mismo comportamiento.

Antes de reintentar, identifica qué paso falló y qué alcanzó a modificar. Si una llamada externa agotó el tiempo de espera, el destino podría haber procesado la solicitud antes de perderse la respuesta. Repetirla sin comprobar identidad/estado puede duplicar el efecto.

Una marca booleana de «procesado» no garantiza por sí sola idempotencia frente a concurrencia o a un fallo entre el efecto y la marca. El mecanismo correcto depende de la operación: clave estable de negocio, restricciones/actualizaciones atómicas o soporte de deduplicación del receptor.

En la consola de workflow, Retry Step vuelve al paso, mientras Terminate and Retry crea otra instancia con los datos de inicio. Primero corrige la causa y revisa el historial; no son botones equivalentes a deshacer. [Acciones sobre fallos — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/workflows-administering).

El ejemplo de esta sesión no escribe contenido. Si lo inicias dos veces, habrá dos instancias y posiblemente dos mensajes. Eso permite observar la identidad sin introducir un efecto de negocio duplicado.

<a id="repaso"></a>

## 10. Repaso con respuestas

<details><summary>1. El build pasa, pero no aparece el proceso Java. ¿Qué miro?</summary><p>Bundle realmente instalado, componente DS, servicio WorkflowProcess y process.label. El build no prueba el registro en la instancia.</p></details>

<details><summary>2. ¿Satisfied implica que el servicio está roto?</summary><p>No. Un componente DS diferido puede estar satisfecho antes de que un consumidor lo active. Revisa el tipo de componente y sus referencias.</p></details>

<details><summary>3. ¿Sync ejecuta el workflow sobre una página?</summary><p>No. Prepara el modelo de runtime. Después inicia una instancia indicando el payload.</p></details>

<details><summary>4. ¿Una línea del Process Step demuestra que el workflow terminó?</summary><p>Demuestra que ese código se ejecutó. El avance y la finalización se comprueban en el historial y estado de la instancia.</p></details>

<details><summary>5. ¿Un workflow RUNNING siempre está fallando?</summary><p>No. Puede estar esperando un Participant Step. Identifica el paso actual antes de actuar.</p></details>

<details><summary>6. ¿Un launcher se configura sólo con la ruta?</summary><p>No. También intervienen evento, tipo de nodo, condiciones, exclusiones y estado habilitado. Guardar contenido puede producir más de un evento.</p></details>

<details><summary>7. ¿FAILED y CANCEL son equivalentes en JobConsumer?</summary><p>No. FAILED permite reintento conforme a la cola; CANCEL indica un fallo permanente. No concluyas que se reintentará sin revisar la política.</p></details>

<details><summary>8. ¿Un timeout prueba que no hubo efecto externo?</summary><p>No. La operación pudo completarse antes de perderse la respuesta. Comprueba estado e identidad antes de repetirla.</p></details>

<a id="ejemplos-locales"></a>

## Ejemplo simple · Un workflow que escribe una línea en el log

El ejemplo une tres piezas: **un servicio Java**, **un logger** y **un modelo con un único Process Step**. No modifica ni publica el payload. Puedes usarlo para ver qué diferencia hay entre instalar código, ejecutar un paso y completar un workflow.

Necesitas tu proyecto WKND Sites tradicional o Archetype, un build base que funcione y Author SDK en `http://localhost:4502`, con permisos para ConfigMgr y Workflow Models. Los pasos de consola se refieren al SDK local. Usa una página de prueba sin datos sensibles; el ejemplo registra su ruta.

### 1. Copiar una sola clase

Crea este archivo en **tu proyecto AEM**, no en el repositorio de documentación:

`core/src/main/java/com/adobe/aem/guides/wknd/core/training/LogPayloadProcess.java`

```java
package com.adobe.aem.guides.wknd.core.training;

import com.adobe.granite.workflow.WorkflowSession;
import com.adobe.granite.workflow.exec.WorkItem;
import com.adobe.granite.workflow.exec.WorkflowProcess;
import com.adobe.granite.workflow.metadata.MetaDataMap;
import org.osgi.service.component.annotations.Component;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Component(
        service = WorkflowProcess.class,
        property = "process.label=Training: log payload")
public class LogPayloadProcess implements WorkflowProcess {
    private static final Logger LOG = LoggerFactory.getLogger(LogPayloadProcess.class);

    @Override
    public void execute(WorkItem item, WorkflowSession session, MetaDataMap args) {
        LOG.info("Training workflow: instance={}, payloadType={}, payload={}",
                item.getWorkflow().getId(),
                item.getWorkflowData().getPayloadType(),
                item.getWorkflowData().getPayload());
    }
}
```

En Archetype, cambia la declaración `package` y la carpeta Java al prefijo de tu proyecto; usa también ese nombre en la categoría del logger. Mantén los imports `com.adobe.granite.workflow`: no los mezcles con la API antigua `com.day.cq.workflow`. Las dependencias del SDK, OSGi y SLF4J ya deben estar en el baseline. Conserva el plugin Bnd que genera `OSGI-INF`; no basta copiar un `.class` a AEM.

Desde la raíz de tu proyecto:

```sh
mvn -pl core -am package
```

Instala con el perfil local de tu baseline. En WKND/Archetype, si tu POM define `autoInstallSinglePackage` para Author en 4502:

```sh
mvn clean install -PautoInstallSinglePackage
```

Abre `/system/console/bundles` y comprueba la versión y el estado Active de tu bundle. En `/system/console/components`, busca el nombre completo de `LogPayloadProcess`: puede aparecer **Satisfied** antes de que un consumidor solicite el servicio. La propiedad `process.label` es la etiqueta que debe aparecer en el selector del Process Step.

### 2. Configurar el logger en la instancia

1. Abre `http://localhost:4502/system/console/configMgr`.
2. Busca **Apache Sling Logging Logger Configuration**. Crea una instancia con **+**, o edita la que ya cubra exactamente esta clase; evita duplicarla.
3. Configura estos campos y conserva los demás valores existentes:

| Campo | Valor |
| --- | --- |
| Log Level | `INFO` |
| Log File | `logs/error.log` |
| Logger / Loggers | `com.adobe.aem.guides.wknd.core.training.LogPayloadProcess` |

4. Guarda. En `/system/console/slinglog`, confirma que esa categoría tiene el nivel y archivo elegidos. Este logger pertenece a una instancia de la factory `org.apache.sling.commons.log.LogManager.factory.config`; la clase del workflow es la **categoría**, no ese factory PID.
5. Abre `crx-quickstart/logs/error.log` dentro de la carpeta donde arrancaste Author. Puedes verlo en el IDE o, desde esa carpeta, ejecutar:

```sh
tail -f crx-quickstart/logs/error.log
```

Todavía no esperes el mensaje: **guardar el logger o instalar el bundle no ejecuta el workflow**. Usa `Ctrl+C` para salir de `tail` cuando termines.

### 3. Crear y ejecutar el modelo en Author

1. Abre **Tools → Workflow → Models → Create → Create Model**. Usa título `Training log payload` y nombre `training-log-payload`.
2. Selecciona tu modelo y pulsa **Edit**. Si viene con un `Step 1` de ejemplo, elimina sólo ese paso. Conserva **Start** y **End**.
3. Abre el panel lateral de pasos y arrastra un **Process Step** entre Start y End. En sus propiedades, pon título `Log payload`.
4. En la pestaña **Process**, selecciona `Training: log payload`, activa **Handler Advance** y deja **Arguments** vacío. Confirma el diálogo. El flujo debe ser **Start → Log payload → End**.
5. Mantén **Transient Workflow** desactivado en las propiedades del modelo para conservar el historial del ejemplo. Pulsa **Sync** y espera la confirmación. Sync prepara el modelo para nuevas ejecuciones; no inicia ninguna.
6. Regresa a **Models**, selecciona `Training log payload` y pulsa **Start Workflow**. En **Payload**, selecciona con el picker una página de prueba existente en tu sitio. No escribas una ruta del ejemplo si no existe en tu instancia. Inicia el workflow.
7. En el log busca `Training workflow:`. Debe incluir el ID real de la instancia, el tipo de payload y la ruta seleccionada. En **Tools → Workflow → Archive**, localiza la ejecución por modelo/payload y abre **History** para confirmar que llegó a End. Puede completarse tan rápido que no alcances a verla en Instances.

**Qué significa el resultado:** la línea confirma que entró a `execute`; el historial confirma el avance del workflow. El método Java no llama a `session.complete`: el avance se delegó a **Handler Advance**.

| Si observas esto | Revisa esto |
| --- | --- |
| No aparece `Training: log payload` en el selector. | Bundle instalado, componente DS, interfaz `WorkflowProcess` y propiedad `process.label`. |
| No aparece la línea. | Instancia iniciada, modelo sincronizado, paso elegido y categoría/nivel del logger. |
| Aparece la línea, pero no termina. | Paso actual e historial; Handler Advance y posibles pasos Participant que hayan quedado en el modelo. |
| La ejecución no aparece en Archive. | Instances y Failures; filtro de búsqueda, retención y que el modelo no sea transient. |

Cuando termines, puedes conservar la clase y el modelo para consultar el ejemplo. Si creaste una configuración de logger sólo para verlo, elimínala o restaura sus valores anteriores. La configuración Cloud se entrega por el mecanismo soportado del proyecto; no depende de cambios manuales en la consola local.

<a id="ejemplo-launcher"></a>

## Ejemplo de lectura · Inspeccionar un launcher sin cambiarlo

Este ejemplo permite reconocer la configuración existente sin automatizar nuevas ejecuciones:

1. Abre **Tools → Workflow → Launchers** en tu SDK.
2. Selecciona un launcher existente y abre **View Properties**, o **Edit** si ésa es la opción disponible. Al terminar usa **Cancel**, sin guardar.
3. Localiza **Event Type**, **Nodetype**, **Path/Glob**, **Condition**, **Workflow Model**, estado **Enabled** y **Exclude List**, según los nombres de tu versión.
4. Lee la regla como una frase: «si ocurre este evento en este tipo de nodo y ruta, cumple estas condiciones y el launcher está habilitado, inicia este modelo». El `Nodetype` JCR no es `sling:resourceType`.
5. Si **Exclude List** nombra propiedades o `event-user-data`, identifica qué cambios se ignoran. No guardes una página para probar una regla amplia que pertenezca al sistema. El ejemplo anterior ya permite iniciar tu workflow manualmente.

Un launcher no contiene la implementación del proceso ni es un temporizador. Si la consola está vacía en tu baseline, no hay una regla instalada que inspeccionar; la ejecución manual del ejemplo anterior sigue siendo válida.

<a id="fuentes"></a>

## Glosario y fuentes

| Término | Lectura rápida |
| --- | --- |
| Logger/category | Nombre al que se aplica un nivel y destino de log. |
| Bundle | Unidad OSGi que contiene clases y dependencias de paquetes. |
| DS component | Componente administrado por Declarative Services. |
| PID / factory PID | Identidad de configuración / fábrica de instancias de configuración. |
| Payload | Objeto o referencia sobre el que trabaja una ejecución. |
| Workflow instance | Ejecución individual de un modelo. |
| Launcher | Regla de eventos que inicia workflows. |
| Topic | Nombre que conecta productores y consumidores de un job. |
| Idempotencia | Repetición de una operación sin duplicar su efecto de negocio. |

Fuentes consultadas el 9 de septiembre de 2026:

- [Logs en AEM Cloud](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/debugging/debugging-aem-as-a-cloud-service/logs), [configuración OSGi](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi) y [administración de instancias](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/workflows-administering) — Adobe, documentación Cloud.
- [Aplicar workflows a páginas](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/authoring/workflows/applying) — Adobe, documentación Cloud.
- [Modelos y API de workflow](https://experienceleague.adobe.com/en/docs/experience-manager-65-lts/content/implementing/developing/extending-aem/extending-workflows/workflows), [Process Step](https://experienceleague.adobe.com/en/docs/experience-manager-65-lts/content/implementing/developing/extending-aem/extending-workflows/workflows-step-ref) y [launchers](https://experienceleague.adobe.com/en/docs/experience-manager-65-lts/content/sites/administering/operations/workflows-starting) — referencias Adobe 6.5 LTS para vocabulario y controles compartidos; no trasladar rutas de despliegue ni operaciones administrativas de 6.5 a Cloud.
- [Logging](https://sling.apache.org/documentation/development/logging.html) y [Sling Jobs](https://sling.apache.org/documentation/bundles/apache-sling-eventing-and-job-handling.html) — Apache Sling.

**Comprobación del código:** `LogPayloadProcess.java` compiló contra AEM SDK API `2025.4.20626.20250425T133017Z-250400`, con JDK 21 y source/target Java 11. Bnd `5.1.2` generó el descriptor DS con la interfaz y etiqueta esperadas. Son las versiones usadas para comprobar el ejemplo, no una indicación de actualizar tu baseline. Los pasos en Author se describen para ejecutarlos en tu SDK; no se presentan como una ejecución ya observada.
