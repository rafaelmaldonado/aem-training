# Sesión 16 · Java, OSGi y Resource API en AEM

**Guía profunda de preparación · Lunes 7 de septiembre de 2026 · Español**

[Abrir la versión HTML](session-16-study-guide.html) · [Ver las diapositivas](../lessons/0016-java-osgi-resource-api-foundations.html#slide-deck) · [Notas del presentador](../slides/lesson-16/speech.md)

El objetivo de la sesión es que puedas explicar cómo una clase Java llega a funcionar dentro de AEM y cómo lee contenido. Esta guía desarrolla el resumen de preparación de la sesión 16 y conserva su alcance: fundamentos para desarrolladores con experiencia principalmente en frontend y authoring.

> **Que Java compile no demuestra que AEM pueda utilizarlo.** Hay que verificar el empaquetado, las dependencias en ejecución, la disponibilidad del componente y el contenido que consume.

## Cómo estudiar esta guía

- **Primera lectura, 20–25 minutos:** sigue el recorrido completo y detente en las diferencias entre bundle, componente y servicio.
- **Recuperación, 5 minutos:** contesta las preguntas al final antes de desplegar las respuestas.
- **Antes de la sesión, 5 minutos:** resuelve otra vez los casos que te hayan costado y explica el recorrido sin consultar el texto.
- **Después de la sesión:** aplica el mapa de evidencias a una clase real de tu proyecto. Si no tienes el SDK abierto, ensaya con el caso ilustrativo sin inventar estados observados.

**Resultado esperado:** identificar el recurso, la clase, el bundle, el papel OSGi y la evidencia de ejecución de una capacidad concreta. Leer el resumen no sustituye comprobar ese recorrido.

## Índice

1. [Del Java al runtime](#recorrido)
2. [OSGi y Apache Felix](#osgi)
3. [Anatomía de un bundle](#bundle)
4. [Bundle, componente y servicio](#vocabulario)
5. [Declarative Services](#ds)
6. [Estados y diagnóstico](#estados)
7. [Resource API](#resource)
8. [ValueMap y adaptación](#valuemap)
9. [Elección de API y ResourceResolver](#resolver)
10. [Caso integrado y mapa de evidencias](#caso)
11. [Repaso con respuestas](#repaso)
12. [Glosario y fuentes](#fuentes)

<a id="recorrido"></a>

## 1. Del Java al runtime

En el proyecto, el módulo Maven `core` contiene el código Java del backend. Ese código atraviesa varias etapas:

```text
Código fuente en core
        ↓
Compilación a bytecode
        ↓
Empaquetado como bundle OSGi
        ↓
Instalación y resolución de dependencias en Apache Felix
        ↓
Gestión de componentes y servicios, cuando corresponde
        ↓
Ejecución de lógica que consume contenido
```

Cada etapa responde una pregunta distinta:

| Etapa | Qué demuestra | Evidencia |
| --- | --- | --- |
| Compilación | El código compila con las dependencias del build. | Resultado del compilador. |
| Empaquetado | Las clases y metadatos necesarios están en el artefacto. | JAR, manifest y descriptores. |
| Resolución | El entorno satisface los requisitos del bundle. | Imports, proveedores y versiones. |
| Activación de un componente DS | El contenedor pudo crear ese objeto gestionado. | Estado, referencias y errores de activación. |
| Comportamiento | La lógica produce el resultado esperado con datos concretos. | Recurso, propiedades, permisos y resultado. |

Un caso típico: Maven encuentra una biblioteca y compila correctamente, pero AEM no dispone del paquete requerido en una versión compatible. El build pasa y el bundle no resuelve. Repetir el mismo build no cambia lo que falta en el runtime.

**Matiz:** una clase Java normal no necesita convertirse en componente OSGi. La etapa de Declarative Services aplica a las clases declaradas para esa gestión. No todas las clases de `core` necesitan `@Component`.

<a id="osgi"></a>

## 2. OSGi y Apache Felix

**OSGi define el sistema modular y de servicios; Apache Felix implementa ese entorno dentro de AEM.** Los módulos pueden publicar contratos, consumir capacidades y tener ciclos de vida gestionados.

Esto introduce dos preguntas diferentes:

- ¿Puede este módulo acceder a las clases que necesita? Es una cuestión de paquetes y resolución.
- ¿Existe un servicio disponible que proporcione la capacidad que necesita? Es una cuestión del registro de servicios y las referencias entre componentes.

Una dependencia disponible para compilar no garantiza que ambas condiciones se cumplan en ejecución. Separarlas evita investigar una referencia de servicio cuando el bundle todavía no puede resolver sus paquetes.

Base de esta distinción: [notas de la sesión, slides 2–5](../slides/lesson-16/speech.md).

<a id="bundle"></a>

## 3. Anatomía de un bundle

Un bundle es un JAR con contratos de ejecución. Contiene clases Java, recursos y metadatos OSGi. Su archivo `META-INF/MANIFEST.MF` describe cómo participa en el entorno.

| Cabecera | Significado |
| --- | --- |
| `Bundle-SymbolicName` | Identidad del bundle. |
| `Bundle-Version` | Versión del bundle. |
| `Import-Package` | Paquetes externos que necesita. |
| `Export-Package` | Paquetes que ofrece a otros bundles. |
| `Service-Component` | Ubicación de los descriptores DS, cuando existen. |

Si un consumidor requiere un paquete dentro de cierto rango de versiones, Felix debe encontrar un proveedor compatible. La versión del bundle y la versión de un paquete exportado son datos diferentes: al investigar un import, revisa la versión del paquete que satisface ese contrato.

Exportar todas las clases no es una solución. Las implementaciones internas deberían permanecer privadas y los contratos compartidos deberían ser explícitos.

> **Exportar un paquete permite acceder a tipos Java. Registrar un servicio permite obtener una capacidad en ejecución.**

Exportar la interfaz `GuideRepository` no crea ni registra automáticamente un objeto que la implemente. De forma inversa, un componente puede publicar un servicio bajo una interfaz compartida manteniendo privada su clase de implementación.

Referencia del curso: [anatomía del bundle, slide 3](../slides/lesson-16/speech.md).

<a id="vocabulario"></a>

## 4. Bundle, componente y servicio

| Concepto | Qué es | Ejemplo ilustrativo |
| --- | --- | --- |
| Bundle | Módulo desplegable y frontera de carga de clases. | El JAR generado por `core`. |
| Componente DS | Objeto cuyo ciclo de vida gestiona Declarative Services. | `GuideCatalog`. |
| Servicio OSGi | Capacidad registrada bajo uno o varios contratos Java. | Una implementación disponible como `GuideRepository`. |

Un bundle puede contener muchas clases y varios componentes. Un componente puede registrar servicios o realizar trabajo interno sin publicar uno. Una clase normal dentro de un bundle no se convierte automáticamente en componente o servicio.

**“Componente” aquí significa componente OSGi**, no necesariamente un componente visual de AEM con diálogo y HTL. Cuando alguien diga «el componente no funciona», identifica primero a qué objeto se refiere.

Para un desarrollador frontend, la conexión útil es esta: la tarjeta visual consume datos y presenta una interfaz; detrás puede haber código Java con un papel OSGi concreto. La tarjeta y ese objeto Java tienen responsabilidades y ciclos de vida diferentes.

<a id="ds"></a>

## 5. Declarative Services

Declarative Services, abreviado **DS**, permite declarar qué objeto debe gestionar el contenedor y qué servicios necesita. El ejemplo conceptual de la sesión utiliza esta dependencia:

```text
GuideCatalog
    └── referencia obligatoria → servicio GuideRepository
```

| Anotación | Qué declara |
| --- | --- |
| `@Component` | Una clase que participará como componente DS. |
| `@Reference` | Una dependencia de servicio. |
| `@Activate` | Inicialización asociada a la activación. |
| `@Deactivate` | Limpieza asociada a la desactivación. |

Si falta el servicio requerido, DS no puede activar normalmente el componente consumidor. Cuando sus requisitos se cumplen, puede continuar su ciclo de vida. Una referencia no significa «construye una instancia de esta clase»: solicita un servicio compatible.

Por eso `new GuideCatalog()` no sustituye al contenedor. Java crea un objeto, pero esa construcción manual no realiza por sí sola el enlace de referencias ni la gestión de DS.

Durante el build, las herramientas procesan las anotaciones para generar descriptores que el runtime utiliza. Si una clase anotada no aparece como componente, también debes investigar ese empaquetado.

**Satisfecho no siempre significa instanciado inmediatamente.** Un componente con activación diferida puede registrar su servicio y esperar a que alguien lo solicite. Su estado satisfecho puede ser normal; no actives todo inmediatamente sólo para cambiar la etiqueta de la consola. [Especificación de Declarative Services](https://docs.osgi.org/specification/osgi.cmpn/8.1.0/service.component.html).

La inicialización debe ser breve. Una sincronización remota o un recorrido enorme del repositorio puede retrasar la disponibilidad del componente. Sus campos tampoco son almacenamiento durable: las instancias pueden reiniciarse o reemplazarse. La configuración detallada corresponde a una sesión posterior.

<a id="estados"></a>

## 6. Estados y diagnóstico

El estado del bundle y el del componente son evidencias separadas.

| Estado del bundle | Interpretación |
| --- | --- |
| `Installed` | Está instalado, pero todavía no está resuelto. |
| `Resolved` | Sus requisitos se resolvieron; no está activo. |
| `Active` | El bundle está activo. |

Si un bundle que debería arrancar permanece en `Installed`, inspecciona sus requisitos pendientes. El estado por sí solo no identifica la causa exacta. `Resolved` puede ser coherente con un bundle detenido. [Ciclo de vida OSGi](https://docs.osgi.org/specification/osgi.core/8.0.0/framework.lifecycle.html).

| Situación del componente | Qué investigar |
| --- | --- |
| Referencia insatisfecha | Servicio ausente o que no coincide con lo solicitado. |
| Configuración obligatoria ausente | Configuración requerida para satisfacer el componente. |
| Satisfecho, sin activar todavía | Posible activación diferida normal. |
| Fallo durante activación | Excepción y logs de inicialización. |
| Activo | Comportamiento, entradas y contenido. |

**Un bundle activo puede contener un componente insatisfecho.** Un componente activo también puede devolver datos incorrectos: su activación no valida la lógica de negocio.

En el SDK local puedes inspeccionar estas rutas, usando el host y puerto de tu instancia:

```text
/system/console/bundles
/system/console/components
```

En AEM as a Cloud Service utiliza Developer Console para inspeccionar el estado del entorno. La Web Console del SDK está destinada al desarrollo local; los cambios de código y configuración cloud siguen el proceso de despliegue. [Web Console — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developer-tools/web-console).

<a id="resource"></a>

## 7. Resource API

Un `Resource` representa un elemento direccionable del árbol de recursos de Sling. En AEM suele representar contenido almacenado en JCR, pero la abstracción no exige trabajar directamente con un `Node`.

Esta Guide Card es **ilustrativa**: los nombres y la ruta no prueban que exista en tu proyecto.

```text
/content/wknd/.../jcr:content/root/guidecard
    sling:resourceType = "wknd/components/guidecard"
    title = "Explora Yucatán"
    featured = true
    items/
```

Hay tres datos que debes distinguir:

- **Path:** dónde está esta instancia de contenido.
- **Resource type:** qué tipo de procesamiento o representación se asocia al recurso.
- **Properties:** los valores concretos de esa instancia.

Dos tarjetas pueden compartir `sling:resourceType` y tener títulos y rutas diferentes. Ese tipo de recurso tampoco es lo mismo que el tipo de nodo JCR.

| Método | Uso |
| --- | --- |
| `getPath()` | Obtener la ruta. |
| `getName()` | Obtener el nombre. |
| `getResourceType()` | Obtener el tipo de recurso. |
| `getValueMap()` | Leer propiedades. |
| `getChild("items")` | Obtener un recurso por ruta relativa. |
| `getChildren()` | Recorrer hijos directos. |
| `adaptTo(...)` | Solicitar una representación compatible. |

`getChild()` puede devolver `null` si el hijo no existe. Recorrer hijos directos tampoco equivale a recorrer todo el subárbol. [API de Resource](https://sling.apache.org/apidocs/sling12/org/apache/sling/api/resource/Resource.html).

<a id="valuemap"></a>

## 8. ValueMap y adaptación

Suponiendo que ya tienes un recurso válido, puedes leer sus propiedades así:

```java
ValueMap properties = resource.getValueMap();

String title = properties.get("title", "Untitled guide");
boolean featured = properties.get("featured", false);
```

Son fragmentos de lectura para estudiar el contrato, no una clase completa. El segundo argumento establece un valor predeterminado y permite determinar el tipo esperado.

También puedes pedir explícitamente un tipo:

```java
String title = properties.get("title", String.class);
```

Aquí el resultado puede ser `null` si falta la propiedad o no puede convertirse al tipo solicitado.

- El valor predeterminado no se guarda automáticamente en el repositorio.
- Una cadena vacía sigue siendo un valor; no se sustituye automáticamente por `"Untitled guide"`.
- **Propiedad ausente**, **valor vacío** y **valor no convertible** son situaciones diferentes.

Esta distinción evita usar un fallback para ocultar un contrato de contenido incorrecto. [API de ValueMap](https://sling.apache.org/apidocs/sling12/org/apache/sling/api/resource/ValueMap.html).

`adaptTo(...)` solicita una adaptación soportada. No es un cast universal ni garantiza un resultado: debes contemplar que devuelva `null`. Por ejemplo, pedir una representación de página requiere un recurso y una adaptación apropiados; una tarjeta dentro de una página no se convierte automáticamente en la página que la contiene. [Ejemplos de adaptación de Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/foundation/development/understand-java-api-best-practices).

<a id="resolver"></a>

## 9. Elección de API y ResourceResolver

La preferencia del curso es elegir la API que exprese directamente la necesidad:

| Necesidad | Punto de partida |
| --- | --- |
| Trabajar con conceptos de AEM, como páginas | AEM: `Page`, `PageManager`. |
| Leer propiedades y estructura de recursos | Sling: `Resource`, `ValueMap`. |
| Operaciones específicas del repositorio | JCR. |
| Declarar componentes, servicios y ciclo de vida | OSGi. |

El orden **AEM → Sling → JCR → OSGi** es una guía de selección. OSGi atiende cuestiones del contenedor; no es una alternativa para leer el título de una tarjeta. Usar JCR es válido cuando el requisito es específico del repositorio. [Buenas prácticas de APIs Java en AEM](https://experienceleague.adobe.com/en/docs/experience-manager-learn/foundation/development/understand-java-api-best-practices).

El `ResourceResolver` permite acceder a recursos bajo un contexto de identidad y permisos. Una ruta correcta no basta: importa quién intenta leerla.

- El resolver recibido desde la petición pertenece al ciclo de vida de esa petición; no lo cierres desde tu código.
- Si tu código crea un resolver, debe cerrarlo, preferentemente con `try-with-resources`.
- El trabajo en segundo plano debe utilizar un usuario de servicio con permisos limitados.
- No uses acceso administrativo para evitar resolver problemas de permisos.

Estas reglas de propiedad y acceso forman parte de las [notas de la sesión, slide 8](../slides/lesson-16/speech.md).

Un resolver generalmente no es seguro para uso concurrente. Evita guardarlo como campo compartido de un servicio para reutilizarlo entre peticiones. Los recursos y objetos asociados tampoco deben tratarse como independientes de su resolver. [API de ResourceResolver](https://sling.apache.org/apidocs/sling12/org/apache/sling/api/resource/ResourceResolver.html).

<a id="caso"></a>

## 10. Caso integrado y mapa de evidencias

Imagina que una Guide Card no muestra el título esperado. El recorrido útil es:

1. **Contenido:** identifica el recurso exacto, su tipo y la propiedad que contiene el título.
2. **Código:** localiza la clase consumidora en `core` y confirma qué nombre de propiedad lee.
3. **Bundle:** comprueba qué artefacto contiene esa clase y qué versión está desplegada.
4. **Resolución:** verifica que sus requisitos estén satisfechos.
5. **Componente, si aplica:** comprueba descriptor, referencias y estado.
6. **Ejecución:** revisa permisos, valores recibidos, valores predeterminados y logs.

Cada hallazgo cambia la siguiente acción:

| Evidencia | Siguiente investigación |
| --- | --- |
| Import sin resolver | Proveedor y compatibilidad del paquete. |
| Bundle activo, referencia insatisfecha | Servicio requerido por el componente. |
| Componente activo, título predeterminado | Recurso leído, propiedad y conversión. |
| Contenido visible con otra identidad | Permisos y contexto del resolver. |

La explicación que buscas poder dar es:

> Esta clase lee estas propiedades de este recurso. Está empaquetada en este bundle. Su función es esta y, cuando depende de DS, requiere estos servicios. Estas evidencias demuestran qué partes están disponibles y dónde empieza el fallo.

### Plantilla para una clase real

Completa este mapa con datos observados. Si es una clase normal, escribe «no aplica» en los campos de DS.

| Campo | Evidencia que debes registrar |
| --- | --- |
| Recurso | Ruta real y `sling:resourceType`. |
| Entrada | Propiedades e hijos que el código lee realmente. |
| Clase | Ruta del archivo Java y método consumidor. |
| Bundle | Nombre simbólico y versión desplegada. |
| Resolución | Estado y cualquier requisito pendiente. |
| Papel | Clase normal, componente DS y/o proveedor de servicio. |
| Dependencias DS | Contratos requeridos y estado de las referencias. |
| Resultado | Dato esperado, dato observado y explicación. |

**Criterio de preparación:** poder justificar cada vínculo con un artefacto. «El build pasó» sólo demuestra una parte del recorrido.

<a id="repaso"></a>

## 11. Repaso con respuestas

Responde en voz alta o por escrito antes de abrir cada respuesta. Si fallas, vuelve al apartado correspondiente y repite la pregunta antes de la sesión. Estas preguntas son para preparación personal; el cierre del deck sigue reservado a preguntas de la audiencia.

<details>
<summary>1. ¿Por qué puede compilar Java y fallar en AEM?</summary>
<p>Porque las dependencias del build y los requisitos del runtime se verifican en etapas distintas. Busca primero qué frontera falló: empaquetado, resolución, DS o comportamiento. Repasa el recorrido completo.</p>
</details>

<details>
<summary>2. ¿Un bundle activo garantiza todos sus servicios?</summary>
<p>No. Puede contener un componente con una referencia obligatoria insatisfecha. Comprueba el componente y el registro del servicio correspondiente, además del estado del bundle.</p>
</details>

<details>
<summary>3. ¿Exportar una interfaz registra su implementación como servicio?</summary>
<p>No. Exportar un paquete hace accesibles sus tipos; registrar un servicio publica una capacidad en ejecución. Son contratos diferentes.</p>
</details>

<details>
<summary>4. ¿@Reference crea un objeto mediante new?</summary>
<p>No. Declara una dependencia que DS debe satisfacer con un servicio compatible. La construcción manual no realiza automáticamente el enlace ni la gestión del contenedor.</p>
</details>

<details>
<summary>5. ¿Todo componente satisfecho debe estar ya activo?</summary>
<p>No. Un componente con activación diferida puede esperar hasta que se solicite su servicio. Comprueba su declaración antes de interpretar ese estado como error.</p>
</details>

<details>
<summary>6. ¿Resource y JCR Node son equivalentes?</summary>
<p>No. Resource es una abstracción de Sling; Node pertenece a JCR. Para propiedades e hijos de una tarjeta, empieza por Resource y ValueMap.</p>
</details>

<details>
<summary>7. ¿Qué ocurre si falta title al leerlo con un valor predeterminado?</summary>
<p>La lectura devuelve ese valor, sin persistirlo. Si title existe como cadena vacía, esa cadena no se reemplaza automáticamente por el valor predeterminado.</p>
</details>

<details>
<summary>8. ¿Quién cierra un ResourceResolver?</summary>
<p>El propietario de su ciclo de vida. Tu código cierra los que crea; no cierra el resolver proporcionado por la petición.</p>
</details>

### Tres casos para aplicar el diagnóstico

<details>
<summary>Caso A · Maven termina correctamente y el bundle permanece en Installed. ¿Qué inspeccionas?</summary>
<p>Los requisitos sin resolver del bundle, sus imports, versiones y proveedores disponibles. Ese estado orienta la investigación, pero no identifica por sí solo el requisito que falta. Repetir el mismo build no aporta esa evidencia.</p>
</details>

<details>
<summary>Caso B · El bundle está Active y GuideCatalog tiene una referencia GuideRepository insatisfecha. ¿Dónde investigas?</summary>
<p>En el servicio requerido: si está registrado, bajo qué contrato y si coincide con la referencia. Si su proveedor también depende de DS, revisa su estado y requisitos. El bundle consumidor activo no resuelve esa dependencia.</p>
</details>

<details>
<summary>Caso C · El código lee title, pero la tarjeta guarda jcr:title. ¿Qué explica el fallback?</summary>
<p>Los nombres no coinciden. ValueMap no traduce automáticamente title a jcr:title. Confirma el contrato entre diálogo, propiedad persistida y lectura Java antes de corregir el lado responsable. No cambies contenido existente sin evaluar su compatibilidad.</p>
</details>

Si una respuesta no te resulta clara, pregunta al agente con el caso y la evidencia que tienes; puedes pedir una explicación paso a paso o una pregunta nueva para practicar.

<a id="fuentes"></a>

## 12. Glosario y fuentes

| Término | Definición de referencia |
| --- | --- |
| `core` | Módulo Maven que contiene el Java del proyecto. |
| Runtime | Entorno donde el código se ejecuta. |
| Bundle | Módulo OSGi desplegable con clases y metadatos. |
| Wiring | Conexiones resueltas entre requisitos y proveedores del runtime. |
| DS | Declarative Services: gestión declarativa de componentes y dependencias. |
| Componente DS | Objeto gestionado por DS, distinto del componente visual de AEM. |
| Servicio OSGi | Capacidad registrada bajo contratos Java para consumidores. |
| Resource | Elemento direccionable del árbol de recursos de Sling. |
| ValueMap | Acceso a propiedades con lectura tipada. |
| ResourceResolver | Acceso a recursos bajo un contexto de identidad y permisos. |
| JCR | Java Content Repository: API del repositorio de contenido. |

**Lectura principal recomendada:** [Java API Best Practices in AEM — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/foundation/development/understand-java-api-best-practices). Concéntrate en elegir entre AEM, Sling, JCR y OSGi y en los ejemplos de lectura de contenido.

Fuentes del resumen, consultadas el 5 de septiembre de 2026:

- [Contenido y diapositivas de la sesión 16](../lessons/0016-java-osgi-resource-api-foundations.html).
- [Outline de la sesión 16](../slides/lesson-16/outline.md) y [notas del presentador](../slides/lesson-16/speech.md).
- [Declarative Services — OSGi](https://docs.osgi.org/specification/osgi.cmpn/8.1.0/service.component.html): componentes, referencias y activación diferida.
- [Life Cycle Layer — OSGi](https://docs.osgi.org/specification/osgi.core/8.0.0/framework.lifecycle.html): estados de bundles.
- [Web Console — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developer-tools/web-console): inspección local y acceso a Developer Console.
- [Resource — Apache Sling](https://sling.apache.org/apidocs/sling12/org/apache/sling/api/resource/Resource.html): propiedades y navegación.
- [ValueMap — Apache Sling](https://sling.apache.org/apidocs/sling12/org/apache/sling/api/resource/ValueMap.html): tipos y valores predeterminados.
- [ResourceResolver — Apache Sling](https://sling.apache.org/apidocs/sling12/org/apache/sling/api/resource/ResourceResolver.html): acceso, ciclo de vida y concurrencia.

Las referencias de OSGi y Sling explican los contratos citados; no fijan la versión de esas bibliotecas instalada en tu SDK. Para programar, contrasta las APIs con las dependencias del proyecto.

**Alcance de esta preparación:** domina bundle/componente/servicio, interpretación de estados y lectura de una Guide Card. Sling Models y Model Exporter se desarrollan en la [sesión 17](../lessons/0017-sling-models-delegation-exporter.html); configuración detallada, servlets y JUnit pertenecen a sesiones posteriores.
