# Sesión 26 · Tags y consultas de contenido acotadas

**Lunes 21 de septiembre de 2026 · Semana 6 · Núcleo de 30 minutos, ampliable a 60**

[Versión HTML](session-26-study-guide.html) · [Slides en inglés](../lessons/0026-tags-bounded-content-queries.html#slide-deck) · [Ejemplo local](#ejemplos-locales)

Una Guide List empieza con una decisión de contenido: qué páginas pertenecen al listado y cuáles quedan fuera. La taxonomía permite clasificarlas; la consulta convierte esa decisión en restricciones sobre una ruta, un tipo de nodo y propiedades concretas. Un título visible como `Hiking` ayuda al autor, mientras que un ID como `training:activity/hiking` identifica el tag almacenado.

La sesión conecta esa clasificación con QueryBuilder y una lectura equivalente en JCR-SQL2. Usamos un conjunto pequeño de páginas creado desde cero, un orden explícito y ventanas de resultados limitadas. El objetivo es poder anticipar la salida y explicar las exclusiones. La selección de índices y Explain Query se trabajan en la sesión 27; hoy sólo reconocemos que devolver pocos resultados no demuestra bajo coste.

- Define la raíz del listado antes de consultar.
- Distingue el nodo `cq:Page` de sus propiedades en `jcr:content`.
- Usa el ID almacenado del tag, no su etiqueta visible.
- Separa selección, orden y paginación.
- Comprueba casos incluidos, excluidos y una página de resultados vacía.
- Interpreta los resultados en la instancia y con la identidad que los consultó.

## Recorrido de la sesión

| Minutos | Slides | Contenido |
| --- | --- | --- |
| 0–5 | 1–3 | Contrato de Guide List y clasificación. |
| 5–12 | 4–6 | Predicados y lectura equivalente en SQL2. |
| 12–17 | 7–9 | Orden, ventanas, full-text y respuesta. |
| 17–27 | 10 | Demo con páginas suministradas y consultas copiables. |
| 27–30 | 11–12 | Key takeaways y preguntas. |

**Ampliación a 60 minutos:** dedica 20 minutos adicionales a repetir las variantes con el mismo contenido y 10 a preguntas. Los ejemplos son demostraciones del instructor que cualquiera puede reproducir; no añaden tareas ni entregables por sesión. Para observarlos no hace falta haber completado prácticas anteriores.

<a id="taxonomia"></a>

## 1. Taxonomía: ID, título y asignación

El namespace agrupa una taxonomía. Nuestro ejemplo crea `training`, el contenedor `activity` y dos tags hoja: `hiking` y `cycling`. La definición de Hiking está en `/content/cq:tags/training/activity/hiking`; su ID es `training:activity/hiking`. El título `Hiking` puede mostrarse o localizarse sin convertirse en el identificador de la consulta.

Al asignarlo a una página, inspeccionamos `cq:tags` en su nodo `jcr:content`. Es una propiedad multivalor: una página puede pertenecer a varias categorías. La jerarquía del árbol de tags y la del árbol de páginas cumplen funciones distintas; clasificar una página no la mueve a otra carpeta ni le concede permisos. [Framework de tagging — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/full-stack/tagging-framework).

**Decisión del ejemplo:** buscamos el valor exacto `training:activity/hiking`. Si mañana el requisito incluye toda la rama Activity, tags movidos o equivalencias históricas, habrá que revisar las reglas de tagging y la consulta. Una igualdad sobre una propiedad no expande automáticamente esas relaciones.

<a id="contrato"></a>

## 2. Contrato del listado

| Decisión | Valor del ejemplo |
| --- | --- |
| Raíz | `/content/wknd/us/en/training-search` |
| Tipo de resultado | `cq:Page` |
| Clasificación | `jcr:content/cq:tags` contiene el ID exacto de Hiking. |
| Orden | `jcr:content/jcr:title`, ascendente. |
| Tamaño | Hasta dos resultados por petición. |
| Instancia | Author local, con el usuario autenticado de la demo. |
| Exclusiones | Cycling, página sin tag y página Hiking fuera de la raíz. |

Los títulos del conjunto de ejemplo son únicos para que el orden sea inequívoco. En un listado real que permita títulos repetidos, define un segundo criterio estable y comprueba su soporte y coste. Mantén el contenido sin cambios al comparar ventanas: offset no ofrece una instantánea entre peticiones y las inserciones o cambios de orden pueden desplazar resultados.

<a id="querybuilder"></a>

## 3. QueryBuilder: predicados que se combinan

QueryBuilder recibe restricciones declarativas. Sus evaluadores pueden expresarlas en XPath y, según el predicado, filtrar resultados. Oak procesa la consulta. JCR-SQL2 es otra forma de expresar una selección equivalente; no es el texto que QueryBuilder necesariamente genera. [QueryBuilder API — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/full-stack/search/query-builder-api).

Esta consulta completa está en [querybuilder.properties](examples/session-26/querybuilder.properties):

```properties
path=/content/wknd/us/en/training-search
type=cq:Page
property=jcr:content/cq:tags
property.value=training:activity/hiking
orderby=@jcr:content/jcr:title
orderby.sort=asc
p.limit=2
p.offset=0
p.guessTotal=true
```

`path` acota los descendientes; con los valores por defecto no incluye la propia raíz. `type` determina que el resultado es la página, por eso la propiedad usa la ruta relativa `jcr:content/cq:tags`. Las restricciones se combinan con AND por defecto. Si se cambia el tipo a `cq:PageContent`, cambia también el nodo devuelto y la ruta relativa de las propiedades: no cambies uno sin revisar el otro.

En este caso `property` compara el valor guardado. QueryBuilder también ofrece `tagid` para búsquedas por ID de tag. Se puede sustituir el par `property`/`property.value` por `tagid=training:activity/hiking` y `tagid.property=jcr:content/cq:tags`; no lo añadas encima como si fuera otra condición necesaria. Esta alternativa no define la equivalencia SQL2 de nuestro ejemplo: cuando haya jerarquías o tags movidos, comprueba el comportamiento concreto del predicado instalado. [Predicados de QueryBuilder — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/full-stack/search/query-builder-predicates).

<a id="sql2"></a>

## 4. JCR-SQL2: leer la misma selección

Consulta completa en [guides.sql2](examples/session-26/guides.sql2):

```sql
SELECT * FROM [cq:Page] AS page
WHERE ISDESCENDANTNODE(page, '/content/wknd/us/en/training-search')
AND page.[jcr:content/cq:tags] = 'training:activity/hiking'
ORDER BY page.[jcr:content/jcr:title] ASC
```

`FROM` selecciona el tipo; `ISDESCENDANTNODE` conserva la frontera del subárbol; la comparación encuentra el valor en `cq:tags`; `ORDER BY` aplica el mismo orden. Oak admite propiedades relativas como `jcr:content/cq:tags`. No son tablas de una base relacional ni consultas a una API externa. [Gramática SQL2 de Oak](https://jackrabbit.apache.org/oak/docs/query/grammar-sql2.html).

El archivo muestra selección y orden. Para comparar la **misma ventana**, configura también límite 2 y offset 0 en la herramienta. En la API JCR esos controles son `Query.setLimit(2)` y `Query.setOffset(0)`, antes de ejecutar. No pegues un `LIMIT 2` de SQL relacional al final esperando que sea JCR-SQL2 estándar. [API JCR Query](https://developer.adobe.com/experience-manager/reference-materials/cloud-service/javadoc/javax/jcr/query/Query.html).

Sólo usamos SQL2 para leer y contrastar la selección; no construimos dos implementaciones de Guide List.

<a id="ventanas"></a>

## 5. Orden, límites y conteo

`p.limit=2` devuelve como máximo dos hits y `p.offset=2` omite los dos primeros. `p.guessTotal=true` evita exigir un conteo completo cuando basta conocer el tramo solicitado. En la respuesta JSON, `hits` contiene la ventana, `offset` identifica su inicio, `more` indica si quedan resultados y `total` puede ser un límite inferior cuando el conteo se detiene antes de recorrer todos. Si `more` es verdadero, la interfaz no debe presentar `total` como un total exacto. [Conteo con guessTotal — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/full-stack/search/query-builder-api#using-p-guesstotal-to-return-the-results).

Una respuesta con dos hits puede haber leído u ordenado muchos candidatos. Tampoco un offset muy grande deja de costar sólo porque la ventana sea pequeña. Evita `p.limit=-1` en un listado de navegación. La sesión 27 examina el plan y el trabajo real: hoy conservamos raíz, tipo y tamaño explícitos. [Consultas e índices — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/query-and-indexing-best-practices).

<a id="texto"></a>

## 6. Full-text y propiedad exacta responden preguntas distintas

Un tag clasifica; full-text busca términos en contenido indexado. Sobre la consulta base, añade:

```properties
fulltext=Forest
fulltext.relPath=jcr:content
```

Mantén el resto de predicados y vuelve a `p.offset=0`. En el conjunto suministrado sólo `01 Forest trail` debe coincidir, una vez que su título sea buscable por el índice. No confundas este comportamiento con buscar una subcadena literal: intervienen los campos indexados, el análisis de términos y la frescura del índice. [Full-text — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/full-stack/search/query-builder-predicates#fulltext), [motor de consultas de Oak](https://jackrabbit.apache.org/oak/docs/query/query-engine.html).

Si en el futuro se expone un buscador, la aplicación debe fijar las raíces y tipos permitidos, validar términos y límites y conservar la identidad adecuada. No debe aceptar un mapa arbitrario de predicados enviado por el navegador. Para valores dinámicos en SQL2 usa variables enlazadas cuando corresponda, no concatenación de texto externo. Aquí ejecutamos consultas fijas en las herramientas del SDK.

<a id="ejemplos-locales"></a>

## 7. Ejemplo completo en Author local

### Punto de partida suministrado

Necesitas un Author SDK local con WKND o un sitio creado con Archetype, una plantilla de página habilitada y una cuenta local con permisos para crear páginas y tags. No necesitas Guide List implementada, servicios Java, Cloud Manager ni prácticas previas. Las rutas de WKND siguientes son **rutas del ejemplo a crear**; no se presupone que existan.

Si usas Archetype, identifica tu raíz de idioma en Sites y reemplaza `/content/wknd/us/en` por esa raíz en ambos archivos de consulta y en la tabla. El instructor prepara este mismo conjunto antes de clase y lo demuestra aunque nadie haya hecho práctica. Si una página o un namespace ya existen con otros datos, usa un nombre de prueba distinto y ajusta las consultas; no reemplaces contenido ajeno.

### A. Crear la taxonomía

1. Inicia sesión en tu Author, normalmente `http://localhost:4502`.
2. Abre **Tools → General → Tagging**. Crea un namespace con título `Training` y nombre `training`, o reutilízalo si pertenece a este ejemplo.
3. Dentro de Training crea un tag contenedor con título `Activity`, nombre `activity`.
4. Dentro de Activity crea `Hiking` con nombre `hiking` y `Cycling` con nombre `cycling`.
5. Comprueba sus IDs: `training:activity/hiking` y `training:activity/cycling`. El título no sustituye al campo Name.

La creación necesita permisos sobre la taxonomía. Si faltan, el instructor suministra estos tags en el baseline local; no se resuelve concediendo permisos globales a visitantes. [Administrar tags — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/tags).

### B. Crear páginas y asignar tags

1. En **Sites**, entra a la raíz de idioma del sitio. Crea una página padre con título `Training search` y nombre `training-search`, usando la plantilla de página habilitada de tu baseline.
2. Dentro de ella crea las primeras cuatro páginas de la tabla. La quinta se crea **al lado de Training search**, fuera de esa raíz.
3. En cada página abre **Properties → Basic → Tags** y elige el tag indicado con el picker. Guarda con **Save & Close**. Deja sin tag `Visitor notes` y la página padre; elimina únicamente tags heredados de una copia de prueba si los hubiera. Es preferible crear estas páginas nuevas.
4. Comprueba nombres, títulos y selección de tags antes de consultar. Los prefijos 01–05 son parte del título, no del nombre de nodo.

| Ruta respecto de `/content/wknd/us/en` | Título exacto | Tag | Consulta base |
| --- | --- | --- | --- |
| `training-search/forest-trail` | `01 Forest trail` | Hiking | Incluida. |
| `training-search/river-trail` | `02 River trail` | Hiking | Incluida. |
| `training-search/city-ride` | `03 City ride` | Cycling | Excluida por tag. |
| `training-search/visitor-notes` | `04 Visitor notes` | Ninguno | Excluida por tag ausente. |
| `training-outside-trail` | `05 Outside trail` | Hiking | Excluida por ruta. |

En CRXDE Lite local (`http://localhost:4502/crx/de/index.jsp`), inspecciona sin editar el nodo `.../forest-trail/jcr:content`: `jcr:title` debe ser `01 Forest trail` y `cq:tags` debe contener `training:activity/hiking`. La asignación se hace desde el picker, no creando a mano una propiedad con un título o un ID inexistente.

### C. Ejecutar QueryBuilder

1. Abre `http://localhost:4502/libs/cq/search/content/querydebug.html` con la misma cuenta local.
2. Reemplaza el contenido del formulario por la consulta completa de la sección 3. Si aparece **Query is given as URL**, déjalo desactivado al pegar líneas `clave=valor`.
3. Pulsa **Search**. Deben aparecer `forest-trail` y `river-trail` en ese orden. Las rutas de los hits corresponden a páginas, no a sus nodos `jcr:content`.
4. Cambia únicamente `p.offset` a `2` y repite. Debe quedar vacío porque sólo hay dos coincidencias.
5. Vuelve a offset `0`. Para ver dos ventanas no vacías sin crear más contenido, cambia temporalmente `p.limit` a `1`: offset `0` devuelve Forest y offset `1` devuelve River. Restaura límite `2` al terminar.
6. Añade las dos líneas de full-text de la sección 6 y busca de nuevo. El resultado esperado es Forest. Quita esas líneas antes de contrastar con SQL2.

El Debugger muestra detalles útiles para aprender. Si quieres observar directamente el JSON, abre el endpoint local con los mismos parámetros codificados en la URL; el HTML de esta guía incluye un enlace preparado. Estas herramientas sirven para el SDK autenticado; no se pide exponerlas en el sitio público. [Debugger de QueryBuilder — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/full-stack/search/query-builder-api#testing-and-debugging).

### D. Leer la selección en SQL2

1. En CRXDE Lite, abre la herramienta de consultas (**Tools → Query**, según la versión) y elige **JCR-SQL2** como lenguaje.
2. Pega `guides.sql2`, ajustando la raíz si usas otro sitio.
3. Configura **Limit = 2** y **Offset = 0** cuando la consola ofrezca esos campos. Si tu versión no los expone, conserva el conjunto de cinco páginas y compara sólo selección y orden: la ventana no queda demostrada por ese formulario. Los controles portables están en la API JCR descrita arriba.
4. Ejecuta y compara las rutas: Forest, River. No compares con la variante QueryBuilder que todavía contiene `fulltext=Forest`.

**Resultado esperado del ejemplo, no evidencia de ejecución:** con la misma identidad, contenido guardado e índices actualizados, las dos expresiones seleccionan las mismas dos páginas. Las instrucciones y sintaxis se contrastaron con fuentes oficiales; no se ejecutaron en tu SDK durante la preparación del material.

<a id="diagnostico"></a>

## 8. Si la salida no coincide

| Síntoma | Comprobación concreta |
| --- | --- |
| Cero resultados desde la primera búsqueda. | Ruta real del sitio, tipo `cq:Page`, ID exacto y propiedad en `jcr:content`. |
| Sólo falla después de paginar. | Offset actual; vuelve a 0 al cambiar filtros. |
| La página Cycling aparece. | `cq:tags` es multivalor: comprueba si también tiene Hiking. |
| Aparece Outside trail. | Verifica que la raíz termina en `training-search`, no en la raíz del sitio. |
| Full-text no devuelve Forest. | Título guardado, alcance `jcr:content` y actualización/cobertura del índice. |
| Resultados distintos entre herramientas. | Misma instancia, usuario, filtros, orden, offset y contenido; retira el full-text adicional. |
| Consulta lenta con sólo dos hits. | Conserva la consulta y sus condiciones; analiza el plan en la 27 antes de proponer un índice. |
| Funciona como administrador. | Eso no demuestra lectura con la identidad del visitante; se estudia en las sesiones 28–29. |

No cambies a `/` ni retires todos los límites para “encontrar algo”. Comprueba una condición cada vez dentro del conjunto de prueba. Un resultado en Author tampoco confirma presencia en Publish, publicación de dependencias ni acceso anónimo.

<a id="repaso"></a>

## 9. Repaso con respuestas

1. **¿Por qué no buscar `Hiking` como valor de `cq:tags`?** Es el título; el ejemplo almacena `training:activity/hiking`.
2. **¿Por qué el path de la propiedad incluye `jcr:content`?** El hit es una `cq:Page` y los valores están en su nodo hijo.
3. **¿Por qué se excluye Outside trail si tiene Hiking?** No es descendiente de la raíz seleccionada.
4. **¿Qué devuelve offset 2 con límite 2?** Ningún hit en el conjunto suministrado: sólo existen dos coincidencias.
5. **¿QueryBuilder genera esta SQL2?** No; mostramos dos expresiones de la misma selección y QueryBuilder normalmente produce XPath.
6. **¿Dos hits significan dos nodos leídos?** No; la ejecución puede leer u ordenar más candidatos.
7. **¿Full-text equivale a filtrar un tag?** No; una clasificación explícita y términos indexados son condiciones distintas.
8. **¿Se puede mostrar `total` siempre como cifra exacta?** No con conteo parcial; revisa `more` y la configuración de `guessTotal`.

<a id="fuentes"></a>

## Fuentes y continuidad

Fuentes oficiales de Adobe y Apache enlazadas junto a cada explicación. Consulta documental: 18 de septiembre de 2026. La sesión sigue el [calendario nuevo](eleven-week-redesign-proposal.html): la 27 diagnostica consultas costosas; la 28 trata identidades y ACLs; la 29 el acceso mediante resolvers. Este material no modifica por sí solo el resto del temario publicado.
