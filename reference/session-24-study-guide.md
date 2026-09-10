# Sesión 24 · Content Fragments y Experience Fragments

**Resumen de preparación · Jueves 17 de septiembre de 2026 · Español**

[Versión HTML](session-24-study-guide.html) · [Diapositivas](../lessons/0024-content-experience-fragments.html#slide-deck) · [Ejemplos paso a paso](#ejemplos-locales)

La sesión 24 trata una decisión habitual en Sites: qué unidad conviene reutilizar y quién controla su presentación. Una ficha con datos y un aviso visual pueden aparecer en muchas páginas, pero eso no significa que deban almacenarse igual.

> **Define la unidad de reutilización; identifica su fuente y comprueba quién la consume.** Un cambio pequeño en contenido compartido puede verse en varias páginas.

## Índice

1. [Elegir CF o XF](#eleccion)
2. [Modelo, fragmento y componente](#cf)
3. [Variaciones de contenido](#variaciones)
4. [Experiencias compuestas](#xf)
5. [Ubicación y propiedad](#repositorio)
6. [Referencias y copias](#referencias)
7. [Publicación y dependencias](#publicacion)
8. [Repaso con respuestas](#repaso)
9. [Ejemplo CF: dos campos](#ejemplos-locales)
10. [Ejemplo XF: título y texto](#ejemplo-xf)
11. [Glosario y fuentes](#fuentes)

<a id="eleccion"></a>

## 1. Elegir qué reutilizar

Un **Content Fragment (CF)** conserva contenido estructurado independiente de una página. Un **Experience Fragment (XF)** conserva una composición de componentes, contenido y layout. Ambos se pueden consumir en Sites tradicional.

| Pregunta | Content Fragment | Experience Fragment |
| --- | --- | --- |
| ¿Qué reutilizo? | Valores de campos. | Un bloque de experiencia compuesto. |
| ¿Qué define su estructura? | Content Fragment Model. | Editable template y componentes permitidos. |
| ¿Quién decide la presentación? | El componente consumidor y sus estilos. | La composición del XF, sus componentes y los estilos del sitio. |
| Ejemplo de esta sesión | Una ficha: heading y summary. | Un aviso: Title y Text. |

Elige según el requisito. Si una misma ficha debe tener distintas presentaciones, unos campos explícitos permiten separar los datos de su renderizado. Si el equipo necesita mantener un aviso compuesto como unidad, un XF conserva esa composición. El tamaño del texto o la cantidad de páginas no bastan para decidir.

Un XF tampoco es una captura de pantalla: sus componentes se renderizan dentro de un contexto con estilos y anchura disponibles. [Conceptos de fragmentos en Sites — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/authoring/fragments/content-fragments).

<a id="cf"></a>

## 2. Modelo, fragmento y componente son tres piezas

El modelo establece los campos; el fragmento contiene valores; el componente de la página los presenta. En nuestro ejemplo, `heading` y `summary` son nombres de propiedades del modelo. `Trail information` y `Bring water.` son valores de un fragmento concreto.

La etiqueta que ve el autor y el nombre técnico del campo tienen funciones distintas. Cambiar la etiqueta no equivale a renombrar la propiedad que un consumidor selecciona. Del mismo modo, llamar `heading` a un campo no lo convierte automáticamente en un elemento HTML de encabezado.

Piensa en tres cambios distintos: añadir un campo al modelo, editar el valor de una ficha o cambiar los estilos del componente. Cada uno afecta a una pieza diferente. Antes de cambiar un modelo compartido, identifica los fragmentos y consumidores que dependen de él. [Modelos de Content Fragment — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/assets/content-fragments/content-fragments-models).

<a id="variaciones"></a>

## 3. Una variación es una alternativa de contenido

El contenido principal es el punto de partida de un CF. Una variación permite mantener otra versión de sus valores, por ejemplo un resumen más breve. El consumidor debe seleccionar cuál mostrar.

La alternativa `short` podría conservar `Bring water.` mientras el contenido principal dice `Bring water and wear comfortable shoes.`. No deduzcas que una variación se traduce sola, que representa un idioma o que todo cambio del principal se refleja automáticamente en ella. Revisa las acciones de edición/sincronización del editor y el contenido realmente seleccionado.

**Error común:** editar el principal y mirar una página configurada para otra variación. No es necesariamente un fallo de guardado; puede ser una selección distinta. [Variaciones — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/assets/content-fragments/content-fragments-variations).

<a id="xf"></a>

## 4. Un XF conserva una composición

En el aviso del ejemplo, Title y Text siguen siendo dos componentes. La variación del XF los agrupa para que la página los utilice como un bloque. Su editable template y sus policies definen la estructura y las opciones de autoría.

La página contiene un componente Experience Fragment que selecciona una **variación**. Esa referencia no convierte los dos componentes internos en copias editables independientes dentro de la página consumidora. Para cambiar el aviso compartido, abre la fuente XF y edítala allí.

Las variaciones XF son composiciones alternativas. Una variación creada como Live Copy incorpora reglas MSM; una variación normal no adquiere esas reglas por tener otro nombre. El ejemplo usa únicamente la variación inicial. [Componente Experience Fragment — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/wcm-components/experience-fragment).

<a id="repositorio"></a>

## 5. Ubicar el contenido ayuda a reconocer su responsabilidad

| Pieza | Ubicación habitual | Qué inspeccionar |
| --- | --- | --- |
| Content Fragment | `/content/dam` | Asset, modelo asociado y valores/variaciones. |
| Content Fragment Model | `/conf` | Definición de campos y estado del modelo. |
| Experience Fragment | `/content/experience-fragments` | Variación y componentes authored. |
| Editable template y policies | `/conf` | Estructura y restricciones de componentes. |
| Página Sites | `/content` bajo el sitio | Componentes consumidores y sus selecciones. |

La misma raíz `/conf` aloja distintos tipos de definiciones; no significa que un modelo CF sea una plantilla XF. Usa las consolas y propiedades para relacionar cada pieza. No hace falta editar nodos manualmente para completar estos ejemplos.

<a id="referencias"></a>

## 6. Compartir una referencia tiene consecuencias

Imagina dos páginas, A y B, que seleccionan la misma variación `Training notice`. Si cambias el texto en esa fuente, ambas pueden mostrarlo al volver a renderizarse. Si copiaste el aviso como contenido separado, cada copia tendrá sus propios cambios y ciclo de publicación.

En los diagramas, **la flecha de referencia sale del consumidor y apunta a su fuente**. No representa una operación que copie contenido hacia la página. Esta lectura permite responder qué objeto necesita inspeccionarse cuando el resultado cambia.

Antes de mover, borrar o rediseñar contenido compartido, revisa sus referencias. «Lo veo en una página» no demuestra que sólo exista un consumidor. Publicación y caché también intervienen en cuándo un cambio se hace visible fuera de Author.

<a id="publicacion"></a>

## 7. Author y Publish son comprobaciones distintas

Un preview correcto confirma el resultado en Author bajo ese usuario y estado. Para el sitio publicado, considera el conjunto: página consumidora, fragmento y variación seleccionados, assets referenciados y definiciones requeridas en el destino.

El modelo de un CF debe estar disponible al publicar sus fragmentos dependientes. Un XF necesita su contenido y la estructura/implementaciones que usa; el flujo de publicación de contenido no sustituye el despliegue del código del proyecto. Revisa las dependencias que presenta el asistente y confirma el resultado final en la instancia de destino.

No publiques una carpeta raíz para «enviar todo»: selecciona los elementos concretos del ejemplo. Si el contenido ya llegó pero se ve una versión anterior, revisa la ruta consumida y la caché de entrega antes de editar otra vez la fuente.

Los ejemplos siguientes funcionan con Author. Si además tienes Publish configurado, puedes comprobar allí esos mismos elementos mediante el flujo de publicación de tu baseline. Si no lo tienes, conserva esa diferencia al describir lo observado. [Publicación de Content Fragments](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/assets/content-fragments/content-fragments-managing) y [Experience Fragments](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/authoring/fragments/experience-fragments).

<a id="repaso"></a>

## Repaso con respuestas

<details><summary>1. ¿Un campo llamado heading define la tipografía de la página?</summary><p>No. Define contenido; el componente y sus estilos deciden cómo renderizarlo.</p></details>

<details><summary>2. ¿Crear un modelo crea también una ficha?</summary><p>No. El modelo define los campos. Después creas un fragmento que contiene valores.</p></details>

<details><summary>3. ¿Por qué una página puede seguir mostrando otro resumen?</summary><p>Puede seleccionar otro fragmento o variación. Comprueba esa selección, el guardado y la instancia antes de atribuirlo a caché.</p></details>

<details><summary>4. ¿La página referencia la carpeta del XF?</summary><p>El componente selecciona la variación que se quiere renderizar. Una carpeta organiza; no reemplaza esa selección.</p></details>

<details><summary>5. ¿Un XF garantiza el mismo resultado visual en cualquier sitio?</summary><p>No. Los componentes, estilos y contexto de layout del destino también influyen.</p></details>

<details><summary>6. ¿Una copia sigue siendo la misma fuente compartida?</summary><p>No. El contenido copiado se puede editar por separado. Una relación especial, como Live Copy, requiere su propia configuración.</p></details>

<details><summary>7. ¿Qué revisas si un selector está vacío?</summary><p>El selector concreto: modelos habilitados y permitidos en Assets; plantillas permitidas en XF; o componentes permitidos por la policy del contenedor.</p></details>

<details><summary>8. ¿Un preview de Author demuestra publicación completa?</summary><p>No. Hay que verificar el contenido y las dependencias en el destino y después el resultado entregado.</p></details>
<a id="ejemplos-locales"></a>

## Ejemplos simples en Author

Estos ejemplos usan los componentes que ya trae tu proyecto. No requieren clases Java, HTL ni comandos Maven adicionales. Trabaja en Author SDK (`http://localhost:4502`) con tu baseline WKND Sites o Archetype instalado y una página de prueba editable.

<a id="preparacion"></a>

### Antes de empezar: comprobar los selectores

En el editor de tu página, abre **Insert New Component**. Deben aparecer **Content Fragment** y **Experience Fragment**, los componentes del proyecto que reutilizan Core Components. El componente **Content Fragment List** es otro componente; no lo uses para este ejemplo.

Si no aparecen:

1. En el menú de información de la página, abre **Edit Template**, o entra a **Tools → General → Templates** y selecciona la plantilla de esa página.
2. En modo **Structure**, selecciona el contenedor editable donde vas a insertar el contenido y abre **Policy**.
3. En **Allowed Components**, permite los componentes Content Fragment y Experience Fragment del proyecto. Conserva las otras selecciones y guarda. Una policy compartida afecta a otras páginas: usa la de tu plantilla de prueba.
4. Vuelve al editor de la página y recarga. Si los componentes tampoco existen en el selector de la policy, falta su instalación o sus proxies en el baseline; la policy no instala componentes. Usa el baseline WKND/Archetype completo antes de seguir.

Para el segundo ejemplo también necesitas una plantilla **Experience Fragment de tipo web** instalada, que permita los componentes Title y Text. Una plantilla normal de página Sites no sustituye a una plantilla XF.

### Ejemplo 1 · Una ficha con dos campos

**Qué verás:** el texto de un Content Fragment dentro de una página Sites. Los nombres y valores siguientes son sólo contenido de ejemplo.

#### A. Habilitar la configuración y crear el modelo

1. Abre **Tools → General → Configuration Browser → Create**. Pon título `Training fragments`, nombre `training-fragments` y activa **Content Fragment Models**. Guarda. Si ya existe esta configuración del ejemplo, úsala; no crees otra.
2. En **Tools → General → Content Fragment Models**, entra a esa configuración y pulsa **Create**. Título: `Training fact sheet`. Crea el modelo y ábrelo para editar.
3. Añade estos dos campos, comprobando especialmente **Property Name**:

| Tipo | Field Label | Property Name | Configuración |
| --- | --- | --- | --- |
| Single line text | Heading | `heading` | Required activado |
| Multi line text | Summary | `summary` | Default Type: Plain Text |

4. Guarda el modelo. En su consola, selecciónalo y pulsa **Enable** si todavía no está habilitado.
5. En **Assets → Files**, crea una carpeta propia llamada `training-fragments`. Selecciónala y abre **Properties → Cloud Services**. En **Cloud Configuration**, selecciona `/conf/training-fragments` y guarda.
6. En **Properties → Policies** de esa carpeta, permite `Training fact sheet` mediante **Allowed Content Fragment Models by Path**, usando el picker. Si la política viene heredada, desactiva esa herencia únicamente en esta carpeta de ejemplo antes de seleccionar el modelo. Guarda.

La configuración vincula la carpeta con sus definiciones; la política controla los modelos permitidos. [Configuration Browser](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/assets/content-fragments/content-fragments-configuration-browser) y [modelos y políticas](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/assets/content-fragments/content-fragments-models).

#### B. Crear la ficha y verla en la página

1. Dentro de la carpeta Assets anterior, pulsa **Create → Content Fragment**, selecciona `Training fact sheet` y continúa. Usa título `Trail information` y nombre `trail-information`.
2. Abre el fragmento. En su contenido principal escribe **Heading:** `Trail information` y **Summary:** `Bring water and wear comfortable shoes.`. Guarda con **Save** o **Save & Close**, según tu editor.
3. Abre tu página de prueba en Sites. Inserta **Content Fragment** y abre **Configure**.
4. En **Content Fragment**, selecciona con el picker el fragmento que acabas de crear. Usa **Display Mode → Multiple Elements** y selecciona `heading` y `summary`. En **Variation**, conserva el contenido principal: según la versión, puede aparecer como **Master** o **Main**. Confirma el diálogo.
5. En **Preview**, comprueba que aparecen los dos valores. El componente puede mostrarlos como campos, sin convertir `heading` en un encabezado visual: el nombre del campo no decide el HTML ni la tipografía.
6. Vuelve al editor del fragmento, cambia Summary a `Bring water.` y guarda. Regresa a la página y recarga su preview: el componente debe leer el nuevo valor de la misma fuente.

Si quieres ver el efecto en dos lugares, referencia ese mismo fragmento desde una segunda página de prueba; no copies su texto dentro de un componente Text. [Crear y editar fragmentos](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/assets/content-fragments/content-fragments-managing) y [usarlos en páginas](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/authoring/fragments/content-fragments).

<a id="ejemplo-xf"></a>

### Ejemplo 2 · Un aviso con título y texto

**Qué verás:** dos componentes compuestos en un Experience Fragment y reutilizados desde una página.

1. En la navegación principal, abre **Experience Fragments**. Dentro de la carpeta del proyecto, crea una subcarpeta `training-fragments` para este ejemplo.
2. Selecciona la carpeta y abre **Properties → Allowed Templates**. Conserva la selección heredada si ya permite la plantilla XF web de tu proyecto. Si el selector de creación está vacío, añade la ruta real de esa plantilla instalada y habilitada, obtenida en **Tools → General → Templates**, a Allowed Templates de esta carpeta. Este campo acepta patrones; una ruta exacta de tu plantilla evita permitir todas las plantillas. Guarda.
3. Dentro de la carpeta, pulsa **Create → Experience Fragment**. Elige la plantilla XF web disponible, título `Training notice` y nombre `training-notice`. Crea y abre el fragmento.
4. En su variación inicial, agrega **Title** con texto `Before you go` y **Text** con `Bring water.`. Confirma ambos diálogos. Si tu plantilla ya incluye esos componentes, edítalos en lugar de añadir duplicados. Si no están permitidos, revisa la policy del contenedor de **esa plantilla XF**, siguiendo el procedimiento anterior para Title y Text.
5. Abre tu página de prueba Sites e inserta **Experience Fragment**. En **Configure → Experience Fragment variation**, elige con el picker la variación que acabas de editar, normalmente `master`. Selecciona la variación, no la carpeta ni sólo el contenedor raíz del fragmento. Confirma.
6. Abre **Preview**. Debes ver el título y el texto compuestos. Vuelve a esa variación XF, cambia el Text a `Bring water and a hat.` y confirma. Recarga la página consumidora para observar el cambio.

No es necesario crear una segunda variación, configurar MSM ni publicar para observar esta referencia en Author. [Crear Experience Fragments](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/authoring/fragments/experience-fragments) y [configurar su componente](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/wcm-components/experience-fragment).

### Si algo no aparece

| Síntoma | Comprobación concreta |
| --- | --- |
| Falta Create en Content Fragment Models. | Configuration Browser: Content Fragment Models habilitado y permisos de edición. |
| El modelo no aparece al crear el fragmento. | Estado Enable, Cloud Configuration y Policies de la carpeta Assets. |
| El componente no aparece en la página. | Instalación del componente y Allowed Components del contenedor de esa plantilla. |
| No hay plantilla para crear el XF. | Plantilla XF web instalada/habilitada y Allowed Templates de la carpeta XF. |
| El componente XF queda vacío. | Selección de una variación existente con contenido; permisos y template/policy del XF. |
| Cambiaste contenido, pero la página sigue igual. | Guardado, fuente y variación seleccionadas, instancia que estás mirando y caché. |

**Alcance de la comprobación:** las instrucciones se contrastaron con documentación oficial; no se ejecutaron en tu SDK. Los dos ejemplos son de autoría/configuración y no incluyen código nuevo que compilar. Si sólo tienes Author, observar el resultado allí no confirma su publicación.

<a id="fuentes"></a>

## Glosario y fuentes

| Término | Significado en esta sesión |
| --- | --- |
| CF | Content Fragment: contenido estructurado reutilizable. |
| XF | Experience Fragment: composición reutilizable de componentes. |
| Model | Definición de campos de un CF. |
| Element | Campo de contenido seleccionable por el consumidor. |
| Variation | Alternativa de contenido/composición dentro del mecanismo correspondiente. |
| Policy | Restricciones de autoría aplicables al contenedor o carpeta. |
| Reference | Selección de una fuente existente por un consumidor. |

Las fuentes oficiales están enlazadas junto a cada explicación y procedimiento. Consulta realizada el 10 de septiembre de 2026. Los pasos usan las consolas Tools, Assets y el editor de páginas del SDK; algunas etiquetas cambian entre versiones. No requieren acceso a Cloud Manager.
