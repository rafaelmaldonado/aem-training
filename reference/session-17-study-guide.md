# Sesión 17 · Sling Models, delegación y JSON en AEM

**Guía profunda de preparación · Martes 8 de septiembre de 2026 · Español**

[Abrir la versión HTML](session-17-study-guide.html) · [Ver las diapositivas](../lessons/0017-sling-models-delegation-exporter.html#slide-deck) · [Notas del presentador](../slides/lesson-17/speech.md)

La sesión 17 enseña a transformar el contexto de AEM en un contrato pequeño y explícito para la vista. Sobre los fundamentos de Java, OSGi y Resource API de la [sesión 16](session-16-study-guide.html), ahora debes decidir de dónde obtiene sus datos un Sling Model, cómo prepara esos datos y cómo los consumen HTL y, cuando corresponde, JSON.

> **Un Sling Model convierte contexto en valores y estado listos para la vista.** El modelo prepara los datos; HTL construye el markup; los servicios aportan capacidades reutilizables y un exporter puede publicar una representación del contrato.

## Cómo estudiar esta guía

- **Primera lectura, 20–25 minutos:** sigue la Guide Card desde el recurso hasta sus valores de salida. Detente en adaptable, inyección y fallbacks.
- **Recuperación, 5–10 minutos:** contesta las preguntas y los casos sin abrir primero las respuestas.
- **Antes de la sesión:** vuelve a los casos que fallaste y justifica cada decisión sin consultar el texto.
- **Después de la sesión:** identifica un modelo real de tu proyecto y completa el mapa de evidencias. Registra lo observado; si no tienes el SDK abierto, utiliza el caso ilustrativo sin inventar resultados.

**Resultado esperado:** explicar el adaptable y cada entrada de un modelo, separar la preparación de datos del HTL, reconocer una delegación correcta y comprobar si existe un contrato exportable. Memorizar anotaciones no demuestra esas capacidades.

## Índice

1. [Del recurso al contrato de vista](#contrato)
2. [Resource o request: elegir el adaptable](#adaptable)
3. [Cómo se descubre y crea un modelo](#creacion)
4. [Inyección: fuente y opcionalidad](#inyeccion)
5. [Fallbacks, valores derivados y estado vacío](#fallbacks)
6. [La frontera entre Java y HTL](#htl)
7. [Delegación de Core Components](#delegacion)
8. [Cuándo utilizar un servicio OSGi](#servicios)
9. [Model Exporter y .model.json](#exporter)
10. [Diagnóstico y mapa de evidencias](#diagnostico)
11. [Repaso con respuestas](#repaso)
12. [Glosario y fuentes](#fuentes)

<a id="contrato"></a>

## 1. Del recurso al contrato de vista

En la sesión 16 seguiste una clase desde `core` hasta su disponibilidad en AEM. Ahora el recorrido se concentra en el objeto que la vista utiliza:

```text
Resource o request compatible
        ↓
Models Adapter Factory e inyectores
        ↓
Sling Model: entradas → preparación → getters y estado
        ├── HTL → HTML
        └── Exporter habilitado → JSON
```

El **adaptable** es el objeto de partida: por ejemplo, un recurso con propiedades o una petición con contexto adicional. La Models Adapter Factory coordina la creación del modelo y la resolución de sus entradas.

El resultado útil no es una clase llena de anotaciones. Es un contrato que otro código puede consumir sin conocer cómo está guardado el contenido. En una Guide Card podría incluir `displayTitle`, `link` y `empty`.

| Elemento | Responsabilidad |
| --- | --- |
| Resource | Exponer el contenido y su estructura. |
| Sling Model | Preparar valores y estado para un consumidor. |
| HTL | Elegir elementos, atributos y condiciones del markup. |
| Servicio OSGi | Proporcionar una capacidad reutilizable cuando se necesita. |
| Exporter | Serializar la representación que el modelo expone. |

**Un Sling Model no es un servicio OSGi por defecto.** `@Model` declara un modelo adaptable; no equivale a `@Component`. Un modelo puede consumir un servicio sin convertirse en uno. Esta distinción continúa el vocabulario de la sesión 16. Base: [notas de la sesión, slides 2 y 9](../slides/lesson-17/speech.md).

<a id="adaptable"></a>

## 2. Resource o request: elegir el adaptable

La pregunta decisiva es **qué contexto necesita realmente el modelo**, no desde qué pantalla lo vas a usar.

| Si necesitas… | Punto de partida |
| --- | --- |
| Propiedades, hijos y tipo de recurso | `Resource`. |
| Atributos de petición, bindings u objetos de la petición | Request compatible con el SDK. |
| Delegar un modelo existente | Un adaptable compatible también con el delegado. |

Preferir `Resource` cuando sólo necesitas contenido permite reutilizar el modelo dentro y fuera de una petición. Usarlo desde HTL no obliga a declarar request como adaptable.

Una request sí permite leer contenido de su recurso, además del contexto de la petición. El sentido inverso no está garantizado: tener un `Resource` no proporciona atributos de request ni variables de scripting.

**Caso concreto:** `@ScriptVariable` necesita una request con los bindings correspondientes. Cambiar el adaptable a request no inventa un binding ausente. Si la entrada requerida no está disponible, la creación puede fallar.

No declares ambos adaptables por precaución: cada uno debe poder satisfacer el contrato que prometes. El tipo exacto de request y los imports deben coincidir con las APIs del proyecto; la documentación actual de Sling también muestra variantes Jakarta. [Contrato de adaptables de Apache Sling](https://sling.apache.org/documentation/bundles/models.html#model-and-adaptable-types).

<a id="creacion"></a>

## 3. Cómo se descubre y crea un modelo

Que una clase compile no demuestra que esté disponible como Sling Model. Debes distinguir registro, contexto, selección e inicialización.

| Comprobación | Evidencia |
| --- | --- |
| La clase llegó al runtime | Bundle desplegado con la versión esperada. |
| El runtime descubre el modelo | `@Model` y metadatos de registro generados en el bundle. |
| El objeto de entrada es compatible | Adaptable real frente a los declarados. |
| Se selecciona la implementación esperada | Tipo solicitado y asociación con el resource type, cuando aplica. |
| Las entradas están disponibles | Fuentes de inyección y dependencias requeridas. |
| La inicialización termina | Logs o excepción concreta de creación. |

Los metadatos pueden identificar paquetes mediante `Sling-Model-Packages` o clases mediante `Sling-Model-Classes`. El tooling del proyecto puede generarlos: inspecciona el artefacto antes de añadir configuración duplicada.

Los atributos de `@Model` expresan cosas distintas:

- **`adaptables`:** objetos desde los que se puede crear el modelo.
- **`adapters`:** tipos bajo los que puede solicitarse, por ejemplo una interfaz pública.
- **`resourceType`:** asociación usada para selección por recurso y exportación.

**Matiz del esquema de las slides:** `resourceType` no es una validación universal que rechace toda adaptación directa a una clase concreta. Interviene en la selección entre implementaciones, en búsquedas por recurso y en el exporter; no sustituye validar entradas. [Registro y asociación por resource type — Sling](https://sling.apache.org/documentation/bundles/models.html#associating-a-model-class-with-a-resource-type).

`adaptTo(...)` puede devolver `null`. Eso indica que no se obtuvo el modelo, pero no explica por sí solo la causa. `ModelFactory#createModel(...)` permite obtener una excepción más explícita para diagnosticarla. No conviertas todo fallo en un valor predeterminado antes de entender qué requisito falló. Base: [notas de la sesión, slide 4](../slides/lesson-17/speech.md).

<a id="inyeccion"></a>

## 4. Inyección: fuente y opcionalidad

Cada entrada debería permitir responder dos preguntas: **¿de dónde viene?** y **¿puede faltar legítimamente?**

| Anotación | Fuente o intención |
| --- | --- |
| `@ValueMapValue` | Propiedad del recurso. |
| `@ChildResource` | Recurso hijo y, según el tipo solicitado, su adaptación. |
| `@OSGiService` | Servicio registrado bajo un contrato compatible. |
| `@Self` | Adaptable actual o adaptación de éste al tipo solicitado. |
| `@ScriptVariable` | Variable de los Sling bindings de una request. |

Estas anotaciones hacen visible la fuente y evitan la ambigüedad de una inyección genérica de campos con `@Inject`. No confundas esta recomendación con prohibir cualquier uso de `@Inject`, incluida la inyección por constructor.

Por defecto, las inyecciones son requeridas salvo que el modelo o el campo indique otra estrategia. Si la entrada es imprescindible para un objeto válido, su ausencia debe seguir siendo un fallo visible.

Cuando la ausencia es parte del contrato, `Optional<T>` la comunica también en el tipo. Este fragmento ilustra las entradas de una tarjeta con compatibilidad de contenido; omite imports y el resto de la clase:

```java
@Model(adaptables = Resource.class)
public class GuideCardModel {
    @ValueMapValue
    private Optional<String> title;

    @ValueMapValue(name = "heading")
    private Optional<String> legacyTitle;
}
```

Ambas propiedades pueden faltar porque la tarjeta tiene un fallback definido. Eso no justifica hacer opcional un servicio imprescindible o cualquier otro campo del modelo.

Tampoco equivale **opcional** a **válido**: una cadena presente puede estar vacía o contener sólo espacios. La preparación de valores debe contemplarlo. Base: [notas de la sesión, slides 5 y 6](../slides/lesson-17/speech.md).

**Conexión con DS:** `@OSGiService` expresa la dependencia en el Sling Model; `@Reference` corresponde a componentes DS. Si falta un servicio obligatorio, revisa su proveedor y su estado OSGi antes de modificar las inyecciones para ocultar el fallo.

<a id="fallbacks"></a>

## 5. Fallbacks, valores derivados y estado vacío

En la Guide Card de la sesión, el contrato de prioridad es:

```text
title actual con contenido significativo
        ↓ si no existe o queda vacío al normalizar
heading heredado con contenido significativo
        ↓ si tampoco sirve
"Untitled guide"
```

`heading` es el nombre legado del ejemplo, no una propiedad que debas inventar en cualquier proyecto. Sólo mantén esa compatibilidad si existe contenido que la requiere.

El modelo prepara `getDisplayTitle()` y HTL recibe el resultado. La prioridad debe ser explícita y comprobable:

| `title` | `heading` | `displayTitle` esperado |
| --- | --- | --- |
| `"Guía actual"` | `"Título anterior"` | `Guía actual` |
| Ausente | `"Título anterior"` | `Título anterior` |
| `"   "` | `"  Ruta histórica  "` | `Ruta histórica` |
| Ausente | Ausente | `Untitled guide` |
| `"  Ruta nueva  "` | Ausente | `Ruta nueva` |

Esta tabla define un comportamiento ilustrativo: recortar espacios exteriores, considerar vacío el resultado sin texto y aplicar la prioridad una sola vez. No implica reescribir el contenido persistido.

### Un fallback no decide automáticamente si la tarjeta está vacía

Si `displayTitle` siempre tiene un valor predeterminado, no puedes deducir el estado vacío comprobando únicamente si ese getter devuelve texto.

Define qué contenido hace renderizable al componente. Por ejemplo, si una tarjeta sólo es útil con un destino válido, la falta de ese destino podría hacerla vacía aunque tenga un título de respaldo. Ésta es una decisión de producto que debe quedar explícita; no es una regla universal de Sling.

`isEmpty()` comunica esa decisión a la vista. El tratamiento del placeholder para autores sigue el contrato de authoring del componente, separado del markup destinado al visitante.

### Getters predecibles

La vista puede consultar un getter más de una vez. No escondas en él consultas nuevas, escrituras o llamadas remotas repetidas. Si una preparación merece calcularse al inicializar el modelo, puede realizarse después de las inyecciones, por ejemplo con `@PostConstruct`, y exponer después el resultado. `@PostConstruct` en un modelo no es el callback DS `@Activate`.

Los valores sencillos no necesitan una capa adicional sólo para devolverlos. Base: [fallbacks y contrato HTL, slides 6 y 7](../slides/lesson-17/speech.md).

<a id="htl"></a>

## 6. La frontera entre Java y HTL

El objetivo es que alguien pueda leer el template sin reconstruir reglas del repositorio.

| Decisión | Responsable |
| --- | --- |
| Propiedad actual frente a legado | Modelo. |
| Normalización y valor calculado | Modelo. |
| Condición de negocio que define `empty` | Modelo. |
| Elementos semánticos y jerarquía de encabezados | HTL. |
| Emisión condicional de markup | HTL usando el estado del modelo. |
| Escapado según el contexto de salida | HTL. |

Este fragmento ilustra el consumo del contrato. La clase y el elemento deben ajustarse al proyecto y a la jerarquía real de la página; no implementa el placeholder de authoring:

```html
<sly data-sly-use.card="com.example.core.models.GuideCardModel"></sly>
<article data-sly-test="${!card.empty}">
    <h2>${card.displayTitle}</h2>
</article>
```

HTL accede a `getDisplayTitle()` como `displayTitle` y al estado `isEmpty()` como `empty`. El template no necesita saber si el título procede de `title`, `heading` o un fallback.

Java tampoco debería construir una cadena de HTML para que HTL la inserte. Preparar el valor no elimina la necesidad de escapado contextual ni justifica desactivarlo. [Separación de responsabilidades — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/guidelines#separation-of-concerns).

<a id="delegacion"></a>

## 7. Delegación de Core Components

Cuando una personalización cambia sólo parte de un Core Component, la sesión propone conservar el comportamiento público existente y añadir únicamente lo que pertenece al proyecto.

El recorrido tiene dos niveles diferentes:

```text
Instancia de contenido
  sling:resourceType → componente proxy del proyecto
                              ↓ sling:resourceSuperType
                         Core Component

Modelo del proyecto
  comportamiento propio + métodos reenviados al modelo delegado
```

El proxy vive bajo el espacio de componentes del proyecto y su `sling:resourceSuperType` apunta a la versión del Core Component utilizada. La versión concreta se toma del proyecto, no de un ejemplo copiado.

El modelo usa la interfaz pública, por ejemplo `Title`. El fragmento central de delegación es:

```java
@Self
@Via(type = ResourceSuperType.class)
private Title delegate;

public String getText() {
    return delegate.getText();
}
```

Es un fragmento dentro de un modelo registrado y compatible con el adaptable del delegado; no es una implementación completa de `Title`. Debes conservar y reenviar el resto del contrato que corresponda a la versión utilizada.

`@Via(type = ResourceSuperType.class)` dirige la adaptación hacia el comportamiento del supertipo. Esto evita solicitar simplemente otra vez el contrato del mismo componente personalizado.

**La delegación no es automática por añadir el campo.** Tener un `delegate` no hace que todos tus getters invoquen sus métodos. Tampoco heredar el resource supertype equivale a herencia Java.

Si añades `getEyebrowText()`, esa salida también debe formar parte del contrato que consume tu HTL. Reutilizar el markup heredado no garantiza que muestre un getter nuevo.

Copiar clases privadas de Core Components crea una implementación propia que tendrás que mantener. Delegar conserva la ruta de reutilización, pero no elimina la necesidad de comprobar compatibilidad al actualizar dependencias. [Personalización de Core Components — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/customizing).

<a id="servicios"></a>

## 8. Cuándo utilizar un servicio OSGi

Un Sling Model coordina una vista. Un servicio puede concentrar trabajo reutilizable por varios modelos u otros consumidores.

| Trabajo | Ubicación razonable |
| --- | --- |
| Elegir título actual, legado o fallback | Modelo de la tarjeta. |
| Preparar una etiqueta específica de esa vista | Modelo. |
| Consulta compartida por varios componentes | Servicio, si existe esa reutilización. |
| Integración con un sistema externo | Servicio con un contrato claro. |
| Método que sólo reenvía una propiedad | Normalmente no necesita servicio. |

El modelo declara una dependencia real con `@OSGiService` y adapta el resultado a su vista. El servicio no debería necesitar conocer el HTML de la tarjeta para cumplir su función.

Antes de crear una capa nueva, pregunta qué responsabilidad reusable separa. Evita tanto el modelo que concentra consultas e integraciones como el servicio creado sólo para devolver un campo. Ciclo de vida, configuración y servlets se desarrollan en la [sesión 18](../lessons/0018-osgi-services-configuration-servlets.html).

<a id="exporter"></a>

## 9. Model Exporter y .model.json

Model Exporter permite reutilizar una representación preparada por el modelo y serializarla, normalmente con Jackson. No significa que cualquier clase con `@Model` tenga un endpoint JSON.

```text
Petición a un recurso con selector model y extensión json
        ↓
Resolución del recurso y su tipo
        ↓
Servlet de exportación aplicable
        ↓
Creación del Sling Model elegible
        ↓
Jackson → JSON
```

Este fragmento ilustra las declaraciones, no un componente desplegado:

```java
@Model(
    adaptables = Resource.class,
    resourceType = "example/components/guidecard"
)
@Exporter(name = "jackson", extensions = "json")
```

Se necesitan el registro del modelo, la asociación al recurso y el exporter disponible. El selector habitual es `model`; la extensión del ejemplo es `json`. El contenido de la respuesta depende de la serialización configurada. [Model Exporter — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/foundation/development/understand-sling-model-exporter).

**La ruta importa.** La URL debe identificar el recurso cuyo modelo quieres inspeccionar. Una página y una tarjeta dentro de su árbol pueden tener resource types y modelos diferentes. No asumas que exportar la página equivale a exportar directamente tu tarjeta.

Si el contrato expone `displayTitle` y `empty`, una representación posible sería:

```json
{
  "displayTitle": "Ruta histórica",
  "empty": false
}
```

Es un resultado ilustrativo, no la promesa de que cualquier modelo produzca exactamente esas claves. Jackson y sus anotaciones determinan qué propiedades se serializan y con qué nombres. Un getter nuevo puede ampliar la superficie JSON; inspecciona el resultado y evita exponer objetos internos o datos que el consumidor no debe recibir. [Opciones y anotaciones de exportación — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/foundation/development/develop-sling-model-exporter).

HTML y JSON representan información relacionada, pero no tienen que ser idénticos: HTML incluye estructura y presentación; JSON expone datos. Compara la coherencia de los valores y la política de campos ausentes.

Si un modelo declara Resource y request, el servlet de exportación de Sling prefiere Resource. Por eso un modelo que funciona desde HTL con contexto de request puede fallar al exportarse si sus entradas no funcionan desde Resource. [Selección del adaptable en Exporter Framework](https://sling.apache.org/documentation/bundles/models.html#exporter-framework).

Antes de implementar un servlet propio o duplicar datos en otro modelo, comprueba si el contrato exportado existente ya satisface la necesidad. Exportar JSON en esta sesión no cambia el alcance del curso hacia una arquitectura headless.

<a id="diagnostico"></a>

## 10. Diagnóstico y mapa de evidencias

Diagnostica la frontera que falla antes de cambiar anotaciones:

| Evidencia | Siguiente investigación |
| --- | --- |
| El bundle esperado no está disponible | Despliegue y resolución, como en la sesión 16. |
| La clase compila pero no se descubre como modelo | Registro generado y versión desplegada. |
| `adaptTo()` devuelve `null` | Adaptable, entradas requeridas e inicialización; buscar una causa explícita. |
| Falta una variable de scripting | Request y bindings efectivamente disponibles. |
| No se inyecta un servicio obligatorio | Contrato registrado y estado del proveedor OSGi. |
| Aparece siempre el fallback | Recurso leído, nombre de propiedad y normalización. |
| La extensión pierde comportamiento del Core Component | Contrato del delegado y métodos reenviados. |
| HTL funciona y JSON falla | Elegibilidad del exporter, ruta, adaptable y serialización. |

### Mapa para un modelo real

| Campo | Qué registrar |
| --- | --- |
| Recurso | Ruta, resource type y supertipo relevante. |
| Modelo | Clase, bundle y versión desplegada. |
| Adaptable | Tipo real de entrada y por qué es necesario. |
| Entradas | Anotación, fuente, nombre y obligatoriedad de cada una. |
| Preparación | Prioridad actual → legado → fallback y tratamiento de blancos. |
| Estado | Regla de `isEmpty()` y comportamiento de authoring. |
| HTL | Getters consumidos y markup que controla. |
| Delegación | Interfaz pública, adaptable y métodos propios frente a reenviados. |
| Servicios | Capacidad reutilizada y proveedor, o «no aplica». |
| JSON | Exporter, recurso solicitado y respuesta observada, o «no habilitado». |

**Criterio de preparación:** explicar qué cambia al quitar `title`, conservar sólo `heading`, eliminar ambos o perder una dependencia obligatoria. Los tres primeros casos siguen el fallback definido; el último debe seguir mostrando el contrato roto si el servicio es esencial.

<a id="repaso"></a>

## 11. Repaso con respuestas

Responde antes de desplegar cada solución. Si fallas, vuelve a la sección indicada por el concepto y repite la pregunta antes de la sesión. Este repaso es personal; la última slide sigue dedicada sólo a preguntas de la audiencia.

<details>
<summary>1. ¿Qué produce un Sling Model para la vista?</summary>
<p>Un contrato de valores tipados y estado preparados desde un contexto compatible. HTL consume ese contrato sin reconstruir las reglas del repositorio.</p>
</details>

<details>
<summary>2. ¿Cuándo elegirías Resource en lugar de request?</summary>
<p>Cuando el modelo necesita contenido, propiedades e hijos y sus dependencias son compatibles con ese contexto. Usarlo desde HTL no obliga a depender de una request.</p>
</details>

<details>
<summary>3. ¿@Model convierte la clase en servicio OSGi?</summary>
<p>No. Declara un modelo adaptable. Un Sling Model puede consumir servicios mediante @OSGiService, pero no se registra como servicio por tener @Model.</p>
</details>

<details>
<summary>4. ¿Qué sabes si adaptTo devuelve null?</summary>
<p>Que no obtuviste el modelo, no cuál fue la causa. Inspecciona registro, adaptable, entradas e inicialización; ModelFactory puede aportar una excepción más explícita.</p>
</details>

<details>
<summary>5. ¿Por qué no hacer opcionales todas las inyecciones?</summary>
<p>Porque ocultaría dependencias imprescindibles ausentes. La opcionalidad debe representar una ausencia legítima, como una propiedad con fallback definido.</p>
</details>

<details>
<summary>6. ¿Optional de String significa texto no vacío?</summary>
<p>No. Puede contener una cadena vacía o espacios. La normalización y la regla de contenido significativo son decisiones del modelo.</p>
</details>

<details>
<summary>7. ¿Dónde decides entre title, heading y Untitled guide?</summary>
<p>En el modelo. HTL recibe displayTitle y conserva el control del markup y su escapado contextual.</p>
</details>

<details>
<summary>8. ¿Inyectar un delegate reenvía todos los métodos automáticamente?</summary>
<p>No. La implementación debe conservar y reenviar el contrato correspondiente. La inyección proporciona el objeto delegado; no implementa todos tus getters.</p>
</details>

<details>
<summary>9. ¿Cuándo merece existir un servicio detrás del modelo?</summary>
<p>Cuando encapsula trabajo reutilizable, una integración o una orquestación con responsabilidad propia. Un getter que sólo devuelve una propiedad no necesita esa capa por defecto.</p>
</details>

<details>
<summary>10. ¿Todo Sling Model responde a .model.json?</summary>
<p>No. Debe existir una integración de exportación aplicable al recurso y un modelo que pueda crearse y serializarse. Inspecciona la respuesta real.</p>
</details>

### Cuatro casos de diagnóstico

<details>
<summary>Caso A · Un modelo sólo adapta Resource y requiere @ScriptVariable. ¿Qué contrato revisarías?</summary>
<p>La fuente requiere bindings de request y el adaptable prometido no los proporciona. Decide si el requisito necesita realmente request o si debe expresarse con contenido. Hacer opcional el campo no crea el contexto ausente.</p>
</details>

<details>
<summary>Caso B · title contiene espacios y heading contiene «Ruta histórica». ¿Qué debe mostrar la tarjeta del ejemplo?</summary>
<p>Ruta histórica. El contrato normaliza y descarta el título actual sin texto antes de consultar el legado. Si muestra espacios, falta aplicar la regla de contenido significativo; si muestra el fallback, revisa la lectura de heading.</p>
</details>

<details>
<summary>Caso C · El componente personalizado obtiene su delegate, pero un getter devuelve null en vez del valor del Core Component. ¿Qué inspeccionas?</summary>
<p>La implementación de ese getter y si realmente reenvía la llamada al delegado. Tener el campo inyectado no garantiza conservar el comportamiento del contrato heredado.</p>
</details>

<details>
<summary>Caso D · El modelo declara Resource y request, funciona en HTL y falla al exportarse. ¿Qué contexto compararías?</summary>
<p>El adaptable usado en cada ruta y las entradas requeridas. El servlet de exportación de Sling prefiere Resource cuando ambos están declarados; una dependencia de request podría quedar sin satisfacer. Comprueba también que la URL identifica el recurso correcto.</p>
</details>

Si necesitas más práctica, pregunta al agente con el modelo, el contexto de entrada y la evidencia disponible. Puedes pedir una explicación de una inyección o un caso nuevo sin ver la solución de antemano.

<a id="fuentes"></a>

## 12. Glosario y fuentes

| Término | Definición de referencia |
| --- | --- |
| Adaptable | Objeto de partida desde el que se solicita una adaptación. |
| Adapter | Tipo resultante solicitado en la adaptación. |
| Sling Model | Objeto Java creado desde contexto compatible mediante Sling Models. |
| Injector | Mecanismo que resuelve una entrada desde una fuente concreta. |
| Binding | Variable disponible en el contexto de scripting. |
| Inyección requerida | Entrada cuya falta impide una creación válida según el contrato. |
| Optional | Tipo que representa presencia o ausencia; no valida el contenido. |
| Contrato de vista | Valores y estado que un consumidor puede utilizar directamente. |
| Fallback | Alternativa definida para una entrada ausente o no significativa. |
| Proxy | Componente del proyecto que reutiliza otro mediante su supertipo. |
| Delegación | Reenvío explícito de comportamiento a otro objeto. |
| Model Exporter | Integración que exporta un modelo a otra representación. |

Este glosario amplía el de la [sesión 16](session-16-study-guide.html#fuentes): bundle, componente DS, servicio OSGi, Resource, ValueMap y ResourceResolver mantienen esas definiciones.

**Lectura principal recomendada:** [Apache Sling Models](https://sling.apache.org/documentation/bundles/models.html). Lee primero adaptables, inyecciones y creación; después asociación por resource type y Exporter Framework. Los ejemplos de la documentación no fijan las versiones de tu SDK: usa las dependencias e imports del proyecto.

Fuentes utilizadas para la preparación, consultadas el 5 de septiembre de 2026:

- [Contenido y diapositivas de la sesión 17](../lessons/0017-sling-models-delegation-exporter.html).
- [Outline de la sesión 17](../slides/lesson-17/outline.md) y [notas del presentador](../slides/lesson-17/speech.md).
- [Apache Sling Models](https://sling.apache.org/documentation/bundles/models.html): contraste de contratos y matices de registro, contexto y exportación.
- [Customizing Core Components — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/customizing): proxy, extensión y reutilización.
- [Core Components Guidelines — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/guidelines): separación entre lógica y markup.
- [Understand Sling Model Exporter — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/foundation/development/understand-sling-model-exporter): propósito de la exportación.
- [Develop Sling Model Exporter — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/foundation/development/develop-sling-model-exporter): configuración de la representación y Jackson.

**Alcance:** esta guía prepara para adaptables, inyección, contrato HTL, delegación y JSON. La [sesión 18](../lessons/0018-osgi-services-configuration-servlets.html) desarrolla servicios, configuración y servlets; JUnit se aborda después. No necesitas adelantar esas implementaciones para explicar correctamente el recorrido de esta sesión.
