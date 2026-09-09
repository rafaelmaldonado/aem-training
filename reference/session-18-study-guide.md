# Sesión 18 · Servicios OSGi, configuración y servlets en AEM

**Guía profunda de preparación · Miércoles 9 de septiembre de 2026 · Español**

[Abrir la versión HTML](session-18-study-guide.html) · [Ver las diapositivas](../lessons/0018-osgi-services-configuration-servlets.html#slide-deck) · [Notas del presentador](../slides/lesson-18/speech.md)

La sesión 18 continúa el recorrido de la [sesión 17](session-17-study-guide.html): el modelo prepara una vista, pero algunas capacidades deben compartirse y configurarse fuera de ese modelo. Aquí aprenderás a identificar esa frontera, comprobar su configuración efectiva y decidir si necesita una interfaz HTTP propia.

> **Empieza por el consumidor y su necesidad.** Crea una capacidad reutilizable cuando tenga sentido, configura su comportamiento explícitamente y añade sólo la superficie de entrega que ese consumidor necesita.

[Ir a la práctica local completa](#practica-local)

## Cómo estudiar esta guía

- **Primera lectura, 20–25 minutos:** sigue el caso ilustrativo `GuideUrlService` desde su consumidor hasta la configuración observada.
- **Recuperación, 5–10 minutos:** responde las preguntas antes de desplegar sus soluciones.
- **Antes de la sesión:** explica qué archivo gana para Author/dev y qué ocurre si falta una propiedad requerida.
- **Después de la sesión:** completa el mapa de evidencias con un servicio real. Si sólo dispones del material del curso, etiqueta tus resultados como hipótesis, no como observaciones de AEM.

**Resultado esperado:** justificar la existencia del servicio, identificar su PID y estado, distinguir valores versionados de secretos y explicar la elección entre HTL, exporter y servlet. Cloud Manager se estudia de forma conceptual; no necesitas acceso para esta preparación.

## Índice

1. [Cuándo merece existir un servicio](#servicio)
2. [Declarative Services y consumidores](#ds)
3. [Configuración tipada y PID](#configuracion)
4. [Run modes y selección del documento](#runmodes)
5. [Valores de entorno y secretos](#secretos)
6. [Ausencia, validación y actualizaciones](#validacion)
7. [Comprobar la configuración efectiva](#evidencia)
8. [Elegir la superficie de entrega](#superficie)
9. [Un servlet como contrato HTTP](#servlet)
10. [Caso integrado y mapa de evidencias](#caso)
11. [Repaso con respuestas](#repaso)
12. [Glosario y fuentes](#fuentes)

<a id="servicio"></a>

## 1. Cuándo merece existir un servicio

En la sesión anterior, una Guide Card elegía entre `title`, un valor legado y un fallback. Esa decisión pertenece naturalmente al modelo de la tarjeta. Llevarla a un servicio que sólo devuelve el mismo texto no añade una responsabilidad útil.

La situación cambia si varios consumidores deben aplicar una política común para construir enlaces. Entonces `GuideUrlService` puede concentrar esa capacidad y evitar que dos modelos implementen reglas distintas.

| Trabajo | Dueño razonable |
| --- | --- |
| Título calculado y estado vacío de una tarjeta | Sling Model. |
| Política de enlaces compartida entre consumidores | Servicio. |
| Integración con un sistema externo | Servicio con contrato propio. |
| Elementos y atributos HTML | HTL. |
| Recepción y respuesta de una petición HTTP específica | Servlet, si el consumidor lo exige. |

Antes de crear la interfaz, escribe una frase: «Este consumidor necesita esta capacidad y observa este resultado». Si sólo puedes describir un getter de una vista, probablemente todavía estás dentro del modelo.

Una interfaz pequeña resulta útil cuando consumidores reales dependen de la capacidad. No necesitas anticipar varias implementaciones, una fábrica o una jerarquía de servicios. Base: [notas de la sesión, slides 2 y 9](../slides/lesson-18/speech.md).

<a id="ds"></a>

## 2. Declarative Services y consumidores

El recorrido operativo reutiliza lo aprendido en la [sesión 16](session-16-study-guide.html):

```text
Clase de implementación en core
        ↓
Bundle y metadatos DS
        ↓
Requisitos y configuración satisfechos
        ↓
Componente gestionado / servicio disponible según su ciclo de vida
        ↓
Consumidor de la interfaz pública
```

`@Component(service = GuideUrlService.class)` declara la publicación bajo ese contrato. El build debe generar los metadatos y el runtime debe poder satisfacer los requisitos; la anotación por sí sola no demuestra disponibilidad.

| Anotación | Contexto y función |
| --- | --- |
| `@Component` | Declaración del componente DS y sus servicios. |
| `@Reference` | Dependencia de servicio en otro componente DS. |
| `@OSGiService` | Dependencia de servicio dentro de un Sling Model. |
| `@Activate` | Inicialización del componente DS. |
| `@Deactivate` | Limpieza asociada a su desactivación. |

Una referencia obligatoria insatisfecha impide continuar normalmente hacia la activación. Construir manualmente la implementación con `new` no sustituye la inyección ni el ciclo de vida del contenedor.

Recuerda el matiz de activación diferida: servicio registrado y objeto ya activado no siempre significan lo mismo. Comprueba el estado relevante antes de concluir que hay un error.

Los consumidores de un servicio pueden ejecutarse concurrentemente. No guardes datos de una petición como campos compartidos ni conserves su resolver para futuras peticiones. Una configuración preparada y coherente es distinta de estado de negocio mutable por usuario.

<a id="configuracion"></a>

## 3. Configuración tipada y PID

La configuración es un contrato operativo: otra persona debe entender qué significa una propiedad, qué tipo tiene y qué ocurre cuando falta.

| Elemento | Papel |
| --- | --- |
| `@ObjectClassDefinition` | Describe el tipo de configuración. |
| Métodos de la definición | Declaran propiedades, tipos y valores predeterminados. |
| `@AttributeDefinition` | Añade descripción, nombre u opciones para quien configura. |
| `@Designate` | Asocia el componente con la definición Metatype. |
| PID | Identifica la configuración que recibe el componente. |

La definición utiliza un **tipo de anotación Java**, `@interface`. Este ejemplo es ilustrativo y omite imports:

```java
@ObjectClassDefinition(name = "Guide URL")
public @interface GuideUrlConfig {
    boolean enabled() default false;
    String baseUrl();
    int timeoutMs() default 2000;
}
```

En el componente, `@Designate(ocd = GuideUrlConfig.class)` enlaza esa definición, y el método de activación puede recibir `GuideUrlConfig`. La conversión tipada evita parsear todas las propiedades como cadenas; no valida por sí sola la semántica de una URL o un rango operativo. [Metatype — OSGi](https://docs.osgi.org/specification/osgi.cmpn/8.1.0/service.metatype.html).

**El PID no es el nombre de la interfaz del servicio.** Habitualmente coincide con el nombre completo de la implementación, pero puede configurarse explícitamente. El nombre del archivo debe dirigirse al PID real. Renombrar una clase sin revisar su configuración puede romper esa correspondencia.

Tampoco asumas que `@Designate` hace obligatoria la existencia de configuración. Si el componente requiere un objeto de configuración de Configuration Admin, su política DS debe expresarlo, por ejemplo `ConfigurationPolicy.REQUIRE`. La existencia del objeto y la validez de cada propiedad son comprobaciones diferentes. [Declarative Services — OSGi](https://docs.osgi.org/specification/osgi.cmpn/8.1.0/service.component.html).

<a id="runmodes"></a>

## 4. Run modes y selección del documento

El proyecto versiona archivos `<PID>.cfg.json`, normalmente dentro de `ui.config`. Una ruta de código representativa sería:

```text
ui.config/src/main/content/jcr_root/apps/example/config.author.dev/
    com.example.core.services.impl.GuideUrlServiceImpl.cfg.json
```

La ruta es ilustrativa: utiliza el módulo y la estructura ya existentes en tu proyecto. El estado efectivo de configuración cloud se comprueba en Developer Console, no suponiendo que encontrarás ese archivo como contenido editable en `/apps`.

Para un mismo PID en un entorno **Author + dev**:

| Carpeta candidata | Coincide | Resultado entre estas candidatas |
| --- | --- | --- |
| `config` | Sí | General. |
| `config.author` | Sí | Más específica que la general. |
| `config.author.dev` | Sí | Gana por tener más run modes coincidentes. |
| `config.publish` | No | No aplica a Author. |

**La selección ocurre por PID completo, no por propiedad.** Si el archivo general contiene `baseUrl` y `timeoutMs`, y el específico sólo incluye `baseUrl`, no debes asumir que `timeoutMs` se hereda del general. Su resultado dependerá del contrato y los defaults aplicables, no de una mezcla de esos archivos.

Usa los run modes admitidos, como `author`, `publish`, `dev`, `stage` y `prod`; AEM as a Cloud Service no permite inventar run modes personalizados como `cliente-a`. Evita depender de empates de especificidad para expresar prioridades. [Selección de configuración — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi).

<a id="secretos"></a>

## 5. Valores de entorno y secretos

Versiona la forma del contrato y los valores que pueden compartirse. Para valores que cambian entre entornos, usa el mecanismo de interpolación correspondiente:

| Clase de valor | Ejemplo | Tratamiento |
| --- | --- | --- |
| Estable y no sensible | Timeout predeterminado | Puede versionarse. |
| Variable no secreta | URL base por entorno | `$[env:GUIDE_BASE_URL]`. |
| Credencial de una integración real | Token API | `$[secret:GUIDE_API_TOKEN]`. |

Ejemplo de configuración para una capacidad sin credenciales:

```json
{
  "enabled:Boolean": true,
  "baseUrl": "$[env:GUIDE_BASE_URL]",
  "timeoutMs:Integer": 2000
}
```

Los sufijos del formato `.cfg.json` indican tipos. Las propiedades resultantes aquí se llaman `enabled`, `baseUrl` y `timeoutMs`; no copies los sufijos como nombres de métodos Java.

Un servicio que sólo construye URLs no necesita un token por precaución. Si una integración autenticada lo requiere, añade esa propiedad al contrato y utiliza la referencia de secreto, sin guardar su valor resuelto en Git, logs, capturas ni fixtures.

**Un placeholder sin resolver puede seguir siendo texto no vacío.** Si falta la variable y no hay default de interpolación, no basta comprobar `value != null`. Detecta valores sin resolver y aplica la política de ausencia. Un default sólo es correcto si su comportamiento es seguro y deliberado. [Interpolación y defaults — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi).

Las variables de entorno se suministran por el canal operativo y tier correspondientes. No son un mecanismo para sobrescribir configuración OSGi propiedad de Adobe. Tampoco añadas condicionales Java para adivinar si estás en dev o prod cuando la configuración ya expresa la diferencia. [Variables de entorno — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/environment-variables).

<a id="validacion"></a>

## 6. Ausencia, validación y actualizaciones

Clasifica cada propiedad antes de implementar el servicio:

| Situación | Comportamiento que debes definir |
| --- | --- |
| Propiedad opcional ausente | Default documentado y seguro. |
| Capacidad explícitamente apagada | Estado deshabilitado reconocible. |
| Capacidad habilitada sin entrada imprescindible | Rechazo o indisponibilidad deliberada. |
| Valor presente pero inválido | Diagnóstico útil y fallo seguro. |

En una integración, «hay una URL» no demuestra que sea un destino permitido. Valida su forma y las restricciones que exige el contrato, por ejemplo esquema HTTPS, host permitido y ausencia de credenciales incrustadas. Establece límites de tiempo y rangos razonables antes de realizar trabajo remoto. Si el servicio sólo construye enlaces, valida según esa responsabilidad, sin fingir que realiza una integración.

No normalices silenciosamente un destino inseguro hasta convertirlo en otro destino inesperado. Un error de configuración debe ser identificable sin imprimir la configuración completa ni secretos.

### Activación inicial y actualización no son la misma operación

En activación inicial no existe una configuración anterior válida que conservar. Si la inicialización lanza una excepción, el componente no queda activado.

El outline menciona conservar el contrato válido anterior. Debes leerlo como **un comportamiento que requiere diseño explícito**, no como una garantía automática del contenedor. En particular, una excepción de `@Modified` no deshace por sí sola los valores de Configuration Admin. Sin un método de modificación, una actualización puede llevar a desactivación y nueva activación.

Si el requisito permite mantener el comportamiento anterior durante una actualización inválida, valida primero una configuración candidata y sólo después sustituye coherentemente el estado de trabajo. Registra que el comportamiento conservado no coincide con la configuración rechazada. En otros casos, lo correcto será deshabilitar la capacidad. [Activación y modificación en DS — OSGi](https://docs.osgi.org/specification/osgi.cmpn/8.1.0/service.component.html).

<a id="evidencia"></a>

## 7. Comprobar la configuración efectiva

El archivo demuestra intención; el runtime demuestra qué se aplicó. Sigue esta secuencia:

1. Identifica el PID exacto y la versión del componente desplegado.
2. Selecciona el entorno y tier que quieres comprobar.
3. Comprueba el estado del componente y sus referencias.
4. Inspecciona sólo las propiedades efectivas no sensibles necesarias.
5. Ejecuta la capacidad con una entrada conocida y compara el resultado esperado.

En el SDK local, las vistas de Components y Configuration permiten inspección directa. En cloud, usa los status dumps de Developer Console. Verifica Author y Publish de manera independiente si tienen valores distintos. Base: [notas de la sesión, slide 8](../slides/lesson-18/speech.md).

Una captura con el nombre del archivo no demuestra que el PID correcto esté activo. Tampoco la presencia de una propiedad prueba que la lógica la haya aceptado. La evidencia debe unir **PID, tier, estado, valor seguro y resultado observado**.

<a id="superficie"></a>

## 8. Elegir la superficie de entrega

Detente en la primera opción que satisface al consumidor:

| Necesidad | Superficie mínima |
| --- | --- |
| Markup de un componente renderizado en servidor | HTL. |
| Valores preparados para ese markup | Sling Model. |
| Datos ya presentes en un contrato exportado aplicable | Core Component o Model Exporter existente. |
| Petición y respuesta HTTP distintas que lo anterior no cubre | Servlet con contrato explícito. |

HTL y Sling Model colaboran; no son necesariamente alternativas excluyentes. El servlet aparece cuando existe un consumidor HTTP y una responsabilidad adicional concreta.

«Quiero usar JavaScript» no justifica duplicar un endpoint: primero comprueba qué representación necesita y si ya existe. «Quiero ejecutar Java» tampoco basta: el modelo ya lo hace en el servidor.

Todo endpoint añade decisiones sobre entradas, permisos, caché, errores y compatibilidad de respuesta. Esas decisiones forman parte de la implementación, no son tareas posteriores. Base: [slides 9 y 10](../slides/lesson-18/speech.md).

<a id="servlet"></a>

## 9. Un servlet como contrato HTTP

Si hace falta, prefiere registrarlo por tipo de recurso y define los métodos, selectores y extensiones que necesita el consumidor. Este ejemplo de petición es ilustrativo:

```text
GET /content/example/guide.guides.json

Recurso:   /content/example/guide
Selector:  guides
Extensión: json
Método:    GET
```

Un servlet por resource type participa en la resolución de Sling para ese recurso. No confundas la ruta de la instancia con su tipo. Registrar por un path global tiene otras limitaciones y no es el punto de partida recomendado.

Para lectura, `SlingSafeMethodsServlet` es una base apropiada; no convierte por sí sola tu lógica en segura ni impide que programes efectos laterales dentro de un GET.

**Matiz de selectores:** Sling puede aceptar selectores adicionales después de los registrados. Declarar `guides` no significa necesariamente rechazar `guides.extra`. Si el contrato exige una forma estricta, comprueba también la petición completa. [Resolución de servlets — Apache Sling](https://sling.apache.org/documentation/the-sling-engine/servlets.html).

| Aspecto | Decisión que debes poder explicar |
| --- | --- |
| Entradas | Parámetros admitidos, tipos, rangos y límites. |
| Permisos | Quién puede leer esos datos; identidad usada para acceder. |
| Respuesta | Content type explícito, estructura estable y codificación. |
| Errores | Estados HTTP deliberados, sin revelar detalles internos. |
| Caché | Si el resultado varía por usuario o parámetros y cómo se evita reutilizarlo incorrectamente. |
| Resolución | Qué servlet atiende exactamente esa petición. |

Ejemplos de decisiones, no resultados automáticos de Sling: `400` para entrada inválida, `404` para un recurso no disponible según la política, `503` para una capacidad temporalmente indisponible. La autenticación y autorización deben integrarse con el comportamiento de la plataforma.

Registrar por resource type no sustituye comprobar permisos dentro del trabajo que haces. Un resolver de servicio con más permisos no debe convertir un endpoint público en una vía para leer datos privados. Para JSON, utiliza la serialización disponible; no concatenes cadenas con valores del usuario.

<a id="caso"></a>

## 10. Caso integrado y mapa de evidencias

Imagina que dos modelos necesitan la misma política de enlaces y Author/dev debe usar una URL base diferente de Publish/prod. El servicio concentra la política; cada entorno configura sus datos; cada modelo prepara su vista. No aparece un nuevo servlet mientras ningún consumidor necesite otro contrato HTTP.

| Campo | Evidencia que registrar |
| --- | --- |
| Consumidor | Nombre real y necesidad. |
| Capacidad | Operación reutilizada y resultado esperado. |
| Servicio | Interfaz, implementación y bundle desplegado. |
| DS | Referencias, política de configuración y estado. |
| PID | Identidad exacta y archivo correspondiente. |
| Selección | Run modes activos y documento ganador completo. |
| Valores | Estables, variables, secretos y defaults deliberados. |
| Validación | Ausencia, valor inválido y comportamiento definido. |
| Runtime | Tier, estado y resultado observado sin secretos. |
| Entrega | HTL, exporter o servlet; razón y consumidor. |

Si falla el enlace, esta secuencia evita redeploys a ciegas: **consumidor → servicio → PID → documento seleccionado → valor efectivo → validación → resultado**.

<a id="repaso"></a>

## 11. Repaso con respuestas

Responde antes de abrir cada solución. Este repaso es para preparación personal; la slide final permanece reservada a preguntas de la audiencia.

<details>
<summary>1. ¿Toda lógica de un Sling Model debe moverse a un servicio?</summary>
<p>No. El modelo conserva la preparación propia de su vista. El servicio merece existir si concentra una capacidad reutilizable o una integración con responsabilidad clara.</p>
</details>

<details>
<summary>2. ¿Qué diferencia hay entre @Reference y @OSGiService?</summary>
<p>@Reference declara una dependencia en un componente DS; @OSGiService la declara en un Sling Model. Ninguna se sustituye construyendo manualmente una implementación.</p>
</details>

<details>
<summary>3. ¿La configuración tipada valida automáticamente la URL?</summary>
<p>No. Facilita tipos y metadatos, pero el componente debe validar el significado y las restricciones del valor.</p>
</details>

<details>
<summary>4. ¿El PID siempre es la interfaz del servicio?</summary>
<p>No. Suele coincidir con el nombre completo de la implementación, salvo configuración explícita. Verifica el PID real en el descriptor y runtime.</p>
</details>

<details>
<summary>5. ¿config.author.dev completa propiedades de config.author?</summary>
<p>No. Entre candidatas aplicables, la más específica se selecciona para el PID completo. Las propiedades omitidas no se heredan por mezcla del documento anterior.</p>
</details>

<details>
<summary>6. ¿Un placeholder no vacío prueba que la variable existe?</summary>
<p>No. Puede haber quedado sin interpolar. Valida que el valor esté resuelto y sea aceptable antes de usarlo.</p>
</details>

<details>
<summary>7. ¿Lanzar una excepción en @Modified revierte automáticamente la configuración?</summary>
<p>No. La modificación no es una transacción con rollback automático. Conservar estado válido anterior o deshabilitar la capacidad requiere una política explícita.</p>
</details>

<details>
<summary>8. ¿Cuándo necesitas un servlet nuevo?</summary>
<p>Cuando un consumidor HTTP necesita un contrato distinto que las superficies existentes no satisfacen. Debes definir también validación, permisos, errores y caché.</p>
</details>

### Tres casos para aplicar las decisiones

<details>
<summary>Caso A · El timeout general es 2000, pero el archivo específico no lo incluye. ¿Qué debes comprobar?</summary>
<p>El documento efectivo del PID y el default aplicable del contrato. No atribuyas el valor a una mezcla de archivos. Si el entorno necesita explícitamente 2000, asegúralo en su configuración o default documentado.</p>
</details>

<details>
<summary>Caso B · El endpoint HTTPS es correcto, pero el servicio habilitado conserva un placeholder de token. ¿Puede operar?</summary>
<p>Si la integración requiere ese token, no. Trátalo como entrada imprescindible sin resolver y aplica el fallo seguro previsto; no registres el valor ni inventes credenciales.</p>
</details>

<details>
<summary>Caso C · JavaScript necesita exactamente los datos que ya devuelve un Model Exporter. ¿Añadirías un servlet?</summary>
<p>Primero comprobaría que el contrato exportado, sus permisos y caché sirven al consumidor. Si los satisface, reutilizaría esa superficie en vez de duplicar la implementación.</p>
</details>

Si algo no queda claro, pregunta al agente con el consumidor, el PID y la evidencia no sensible. Puedes pedir otro caso de selección de configuración antes de ver su solución.

<a id="fuentes"></a>

## 12. Glosario y fuentes

| Término | Definición de referencia |
| --- | --- |
| Capacidad | Trabajo con una responsabilidad y un consumidor identificables. |
| PID | Identidad persistente a la que se dirige una configuración OSGi. |
| Metatype | Descripción de tipos y atributos de configuración. |
| Configuration Admin | Servicio OSGi que administra configuraciones. |
| Run mode | Condición del entorno usada para seleccionar configuración. |
| Interpolación | Sustitución de un placeholder por un valor operativo. |
| Configuración efectiva | Valores aplicados al PID en el runtime seleccionado. |
| Tier | Servicio del entorno, como Author o Publish. |
| Servlet | Componente que atiende un contrato de petición y respuesta HTTP. |
| Selector | Parte de la URL que participa en la selección de procesamiento Sling. |

Se mantienen las definiciones de [OSGi en la sesión 16](session-16-study-guide.html#fuentes) y [Sling Models en la 17](session-17-study-guide.html#fuentes).

**Lectura principal:** [Configuring OSGi for AEM as a Cloud Service — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi). Prioriza selección por PID, interpolación y comprobación efectiva.

Fuentes de preparación, consultadas el 8 de septiembre de 2026:

- [Sesión 18 y diapositivas](../lessons/0018-osgi-services-configuration-servlets.html), [outline](../slides/lesson-18/outline.md) y [notas del presentador](../slides/lesson-18/speech.md).
- [Environment Variables — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/environment-variables).
- [Metatype — OSGi](https://docs.osgi.org/specification/osgi.cmpn/8.1.0/service.metatype.html).
- [Declarative Services — OSGi](https://docs.osgi.org/specification/osgi.cmpn/8.1.0/service.component.html).
- [Servlets and Scripts — Apache Sling](https://sling.apache.org/documentation/the-sling-engine/servlets.html).

Los nombres y fragmentos son ilustrativos; no representan un servicio instalado por esta guía. Las APIs del proyecto determinan los imports y versiones aplicables. La [guía de la sesión 19](session-19-study-guide.html) muestra cómo proteger estos contratos con pruebas, sin adelantar autenticación personalizada ni operaciones de Cloud Manager.

<a id="practica-local"></a>

## Práctica local · Del servicio OSGi al HTML (35–45 min)

**Objetivo:** ver un título authored y un mensaje de configuración en el mismo componente. El recorrido es configuración → servicio → Sling Model → HTL. Se usan las APIs que ya incluye WKND; no necesitas un servlet para renderizar esta página.

**Requisitos:** proyecto WKND Sites tradicional o Archetype que ya compile, JDK/Maven compatibles con ese proyecto y Author local en `http://localhost:4502`. Este repositorio contiene material del curso, no el reactor Maven de AEM: los archivos se copian a TU proyecto AEM.

Los ejemplos completos usan el package `com.adobe.aem.guides.wknd.core.training` y `/apps/wknd`. En Archetype sustituye ese prefijo por el de tus clases actuales, tanto en Java como en `data-sly-use`, en el nombre del PID `.cfg.json` y en las rutas `/apps`. No sustituyas los imports de Sling/OSGi. Usa el directorio OSGi ya existente de tu `ui.config` si tiene otro nombre.

1. Copia los seis archivos de abajo conservando sus rutas relativas; no reemplaces los POM ni los filtros completos de tu proyecto.
2. Comprueba que el filtro de `ui.apps` cubre `/apps/wknd/components` y el de `ui.config` cubre `/apps/wknd/osgiconfig`. Si ya cubren esos árboles, no añadas raíces duplicadas.
3. El build debe generar descriptores DS (`OSGI-INF`) y metatype, además de registrar el Sling Model. Mantén los plugins Bnd/Sling del baseline. Si tu manifiesto usa `Sling-Model-Packages` limitado a `.models`, añade el package `.training` a esa lista; si usa el escáner Bnd, comprueba `Sling-Model-Classes` en el JAR resultante.
4. Añade también el [test completo de la sesión 19](session-19-study-guide.html#practica-local), para comprobar los fallbacks de este ejemplo.


### Archivo: `core/src/main/java/com/adobe/aem/guides/wknd/core/training/TrainingMessage.java`

```java
package com.adobe.aem.guides.wknd.core.training;

import org.osgi.service.component.annotations.Activate;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Modified;
import org.osgi.service.metatype.annotations.AttributeDefinition;
import org.osgi.service.metatype.annotations.Designate;
import org.osgi.service.metatype.annotations.ObjectClassDefinition;

@Component(service = TrainingMessage.class)
@Designate(ocd = TrainingMessage.Config.class)
public class TrainingMessage {
    @ObjectClassDefinition(name = "AEM Training - Message")
    public @interface Config {
        @AttributeDefinition(name = "Message")
        String message() default "Welcome to Weekend Guides";
    }

    private volatile String message;

    @Activate
    @Modified
    protected void activate(Config config) {
        String value = config.message();
        message = value == null || value.trim().isEmpty()
                ? "Welcome to Weekend Guides" : value.trim();
    }

    public String getMessage() {
        return message;
    }
}
```

### Archivo: `core/src/main/java/com/adobe/aem/guides/wknd/core/training/TrainingMessageModel.java`

```java
package com.adobe.aem.guides.wknd.core.training;

import org.apache.sling.api.resource.Resource;
import org.apache.sling.models.annotations.Model;
import org.apache.sling.models.annotations.injectorspecific.InjectionStrategy;
import org.apache.sling.models.annotations.injectorspecific.OSGiService;
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;

@Model(adaptables = Resource.class)
public class TrainingMessageModel {
    @OSGiService
    private TrainingMessage trainingMessage;

    @ValueMapValue(injectionStrategy = InjectionStrategy.OPTIONAL)
    private String title;

    public String getTitle() {
        return title == null || title.trim().isEmpty() ? "Weekend Guides" : title.trim();
    }

    public String getMessage() {
        return trainingMessage.getMessage();
    }
}
```

### Archivo: `ui.apps/src/main/content/jcr_root/apps/wknd/components/training-message/.content.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:jcr="http://www.jcp.org/jcr/1.0"
    xmlns:cq="http://www.day.com/jcr/cq/1.0"
    jcr:primaryType="cq:Component"
    jcr:title="Training Message"
    componentGroup="WKND Sites Project - Content"/>
```

### Archivo: `ui.apps/src/main/content/jcr_root/apps/wknd/components/training-message/_cq_dialog/.content.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:jcr="http://www.jcp.org/jcr/1.0"
    xmlns:sling="http://sling.apache.org/jcr/sling/1.0"
    jcr:primaryType="nt:unstructured"
    jcr:title="Training Message"
    sling:resourceType="cq/gui/components/authoring/dialog">
    <content jcr:primaryType="nt:unstructured"
        sling:resourceType="granite/ui/components/coral/foundation/container">
        <items jcr:primaryType="nt:unstructured">
            <title jcr:primaryType="nt:unstructured"
                sling:resourceType="granite/ui/components/coral/foundation/form/textfield"
                fieldLabel="Title" name="./title"/>
        </items>
    </content>
</jcr:root>
```

### Archivo: `ui.apps/src/main/content/jcr_root/apps/wknd/components/training-message/training-message.html`

```html
<section data-sly-use.model="com.adobe.aem.guides.wknd.core.training.TrainingMessageModel">
    <h2>${model.title}</h2>
    <p>${model.message}</p>
</section>
```

### Archivo: `ui.config/src/main/content/jcr_root/apps/wknd/osgiconfig/config.author/com.adobe.aem.guides.wknd.core.training.TrainingMessage.cfg.json`

```json
{
  "message": "Hello from local Author"
}
```

### Compilar e instalar

Desde la raíz de TU proyecto AEM, ejecuta primero las pruebas. El segundo comando supone el perfil `autoInstallSinglePackage` del baseline WKND/Archetype y Author en 4502; compruébalo en tu POM antes de usar otro puerto o credenciales.

```sh
mvn -pl core -Dtest=TrainingMessageTest test
mvn clean install -PautoInstallSinglePackage
```

### Pasos en Author y resultado esperado

1. Abre `/system/console/bundles` en tu Author local y confirma que el bundle `core` está Active.
2. En `/system/console/components`, busca `com.adobe.aem.guides.wknd.core.training.TrainingMessage`. Un servicio DS diferido puede estar **Satisfied** antes del primer consumo; después debe activarse al usar el modelo.
3. En `/system/console/configMgr`, busca **AEM Training - Message** y verifica `Hello from local Author`. La configuración fuente está en `config.author`, sin depender de un run mode `dev` adicional.
4. En Sites crea una página de laboratorio dentro de tu sitio, con un template editable que permita un contenedor. En **Edit Template → Structure**, selecciona ese contenedor, abre su política y permite **Training Message**. Usa una política de laboratorio si la actual afecta otras páginas.
5. Regresa a la página, inserta **Training Message**, abre su diálogo y escribe `My local guide`. Guarda y abre Preview: debes ver el título y `Hello from local Author`.
6. Vacía el título: debe aparecer `Weekend Guides`. Cambia el mensaje del `.cfg.json`, vuelve a desplegar y recarga: cambia el párrafo, pero el título authored se conserva.
7. Opcional, sólo en SDK: cambia el mensaje en ConfigMgr y comprueba `@Modified` recargando la página. Vuelve a dejar el valor de Git; verifica configuración efectiva después de desplegar, porque una edición de consola puede dejar un override local.

**Aceptación:** captura del componente, PID efectivo y prueba verde. Si falla la creación del modelo, revisa registro y servicio obligatorio; no lo vuelvas opcional para ocultar la ausencia. El contenido de los getters se escapa con el contexto de texto de HTL: no uses `context='unsafe'`.

**Limpieza:** elimina sólo la página de laboratorio y revierte la política de prueba; conserva el código hasta terminar las sesiones 19 y 20. Las ediciones en ConfigMgr son una comprobación local, no el mecanismo de configuración Cloud.

Fuentes: [inyección y registro de Sling Models](https://sling.apache.org/documentation/bundles/models.html) y [configuración OSGi en AEM Cloud](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi).
