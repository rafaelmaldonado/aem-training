# Sesión 27 · Diagnosticar una consulta costosa

**Martes 22 de septiembre de 2026 · Semana 6 · Núcleo de 30 minutos, ampliable a 60**

[Versión HTML](session-27-study-guide.html) · [Slides en inglés](../lessons/0027-query-diagnosis-indexes.html#slide-deck) · [Ejemplo local](#ejemplos-locales)

Una consulta puede devolver las dos páginas correctas y aun así realizar demasiado trabajo. El límite controla la ventana entregada; el repositorio puede haber examinado muchos candidatos para filtrar, comprobar permisos u ordenar. Para diagnosticar Guide List necesitamos conservar su contrato de contenido y observar cómo se satisface: qué acceso selecciona Oak, qué condiciones resuelve allí y qué operaciones quedan después.

En esta sesión pasamos de leer la consulta a leer su plan. Contrastamos una raíz demasiado amplia con la raíz prevista, usamos Explain y distinguimos estimaciones de observaciones. Después inspeccionamos la definición del índice seleccionado. El objetivo es decidir el siguiente cambio con evidencia: corregir la consulta cuando basta y justificar una modificación de índice cuando falta cobertura. El ejemplo se prepara en Author local; el proceso Cloud se explica con documentación.

- Pocos hits no demuestran pocas lecturas.
- Distingue traversal del repositorio y exploración excesiva de un índice.
- Busca soporte de tipo, ruta, propiedades y orden dentro del plan.
- Separa coste estimado, filas examinadas y tiempo transcurrido.
- Conserva las condiciones de comparación y comprueba las rutas devueltas.
- Revisa los índices existentes antes de proponer una definición nueva.

## Recorrido de la sesión

| Minutos | Slides | Contenido |
| --- | --- | --- |
| 0–5 | 1–3 | Dos resultados, trabajo desconocido y selección del plan. |
| 5–11 | 4–6 | Restricciones, corrección del contrato y Explain/Measure. |
| 11–23 | 7–8 | Demo local y comparación de evidencia. |
| 23–27 | 9–10 | Definición del índice y proceso Cloud. |
| 27–30 | 11–12 | Key takeaways y preguntas. |

Para ampliar a 60 minutos: repetir la inspección con las variantes durante 20 minutos y dedicar otros 10 a preguntas. El instructor suministra el conjunto de páginas; no se requieren prácticas previas ni entregables por sesión.

<a id="plan"></a>

## 1. Qué explica un plan

Oak compara costes estimados para elegir un acceso. El valor sirve para comparar alternativas del planificador; no representa milisegundos. Un índice produce candidatos, pero pueden quedar condiciones y comprobaciones de acceso pendientes. Sin un acceso adecuado, puede recorrerse el subárbol. Una entrada de log que enumera el coste de traversal no prueba que esa alternativa haya sido elegida. [Motor de consultas de Oak](https://jackrabbit.apache.org/oak/docs/query/query-engine.html).

En nuestra lectura anotamos cuatro preguntas junto al plan real:

| Pregunta | Qué buscar |
| --- | --- |
| ¿Qué acceso se eligió? | Nombre y ruta del índice, o indicación de traversal en el plan seleccionado. |
| ¿Dónde se acota el contenido? | Tipo `cq:Page` y frontera del subárbol. |
| ¿Dónde se aplica Hiking? | La igualdad de la propiedad relativa `jcr:content/cq:tags`. |
| ¿Quién entrega el orden? | Soporte del orden por `jcr:content/jcr:title` en la parte del índice. |

No basta encontrar la condición en el `where` del plan: distingue la consulta enviada al índice del filtrado restante. Un índice presente puede leer muchos candidatos; un orden no soportado puede obligar a acumular resultados y ordenarlos en memoria. [Lectura de planes — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/query-and-indexing-best-practices#reading-query-execution-plan).

**Selectividad:** una condición útil descarta candidatos que no pertenecen al resultado. En Guide List, la raíz y el tag expresan el requisito del producto. No eliminamos páginas válidas ni quitamos el orden para obtener un tiempo menor. Primero comprobamos que la consulta representa lo que se pidió.

<a id="herramientas"></a>

## 2. Explain, Measure y las opciones de la herramienta

| Operación SQL2 en Oak | Resultado | ¿Ejecuta la consulta de resultados? |
| --- | --- | --- |
| `EXPLAIN SELECT …` | Una columna `plan`. | No. |
| `EXPLAIN MEASURE SELECT …` | Plan y coste estimado. | No. |
| `MEASURE SELECT …` | Columnas `selector` y `scanCount`. | Sí. |

`MEASURE` informa filas examinadas, con entradas por selector y una entrada `query`. No sumes esas filas como contadores independientes ni las interpretes como milisegundos. Estas instrucciones son extensiones de Oak a SQL2. [Gramática SQL2: Explain y Measure](https://jackrabbit.apache.org/oak/docs/query/grammar-sql2.html#explain).

La consola **Query Performance → Explain Query** puede ejecutar trabajo adicional según sus opciones. Para inspeccionar sin leer resultados, elige **JCR-SQL2**, pega el `SELECT` y deja desmarcadas **Include Execution Time**, **Read first page of results** e **Include Node Count**. La opción de contar nodos lee el resultado completo; no es necesaria en esta demo. El comportamiento de explicar QueryBuilder es distinto: usamos SQL2 para esta inspección. [Herramienta Query Performance — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/query-and-indexing-best-practices#query-performance-tool).

<a id="ejemplos-locales"></a>

## 3. Ejemplo completo en Author local

### A. Preparar un punto de partida independiente

Necesitas un SDK Author con WKND o un sitio de Archetype, una plantilla de página habilitada y una cuenta local con permisos para crear páginas/tags y abrir las herramientas de diagnóstico. El instructor prepara este conjunto aunque nadie haya hecho la sesión anterior. No hace falta implementar Guide List ni disponer de Cloud Manager.

1. Inicia sesión en `http://localhost:4502`. Si usas otro puerto, adapta las direcciones de esta guía.
2. En **Tools → General → Tagging**, crea el namespace `training` (título Training), el tag contenedor `activity` (Activity) y sus hijos `hiking` (Hiking) y `cycling` (Cycling). Reutilízalos sólo si pertenecen al ejemplo. El ID de Hiking debe ser `training:activity/hiking`.
3. En **Sites**, crea el padre `training-search` bajo `/content/wknd/us/en`, con la plantilla habilitada de tu sitio. Crea las cuatro primeras páginas dentro de él y la quinta al lado del padre.
4. Asigna los tags con **Properties → Basic → Tags → Save & Close**. Mantén sin tags el padre y Visitor notes. Comprueba que Cycling no tenga también Hiking.
5. Si usas Archetype, sustituye `/content/wknd/us/en` por tu raíz real en todos los archivos. Si `training-search` contiene otros datos, usa un nombre nuevo y actualiza las consultas; no sustituyas contenido ajeno.

| Ruta respecto de la raíz del sitio | Título | Tag |
| --- | --- | --- |
| `training-search/forest-trail` | `01 Forest trail` | Hiking |
| `training-search/river-trail` | `02 River trail` | Hiking |
| `training-search/city-ride` | `03 City ride` | Cycling |
| `training-search/visitor-notes` | `04 Visitor notes` | Ninguno |
| `training-outside-trail` | `05 Outside trail` | Hiking |

Inspecciona `forest-trail/jcr:content` en [CRXDE Lite local](http://localhost:4502/crx/de/index.jsp): `jcr:title` y `cq:tags` deben coincidir. Guarda el contenido y comprueba que la consulta ya ve las dos páginas antes de comparar. Los índices asíncronos pueden tardar en reflejar cambios; no interpretes una actualización pendiente como prueba de que falta un índice. [Tagging — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/tags), [modos de indexación — Oak](https://jackrabbit.apache.org/oak/docs/query/indexing.html).

### B. Comprobar la selección y su ventana

Abre el [QueryBuilder Debugger local](http://localhost:4502/libs/cq/search/content/querydebug.html), pega el archivo completo y pulsa **Search**. Deja desactivada **Query is given as URL** si aparece. La ventana esperada es Forest y River, en ese orden.

[Descargar querybuilder.properties](examples/session-27/querybuilder.properties)

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

Esta consulta conserva el contrato de la 26. `p.guessTotal=true` reduce la necesidad de contar todo, pero no arregla una propiedad sin cobertura ni un orden costoso. No uses `p.limit=-1` para un listado de navegación. [QueryBuilder y guessTotal — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/full-stack/search/query-builder-api#using-p-guesstotal-to-return-the-results).

La selección equivalente en SQL2 es:

[Descargar guides.sql2](examples/session-27/guides.sql2)

```sql
SELECT * FROM [cq:Page] AS page
WHERE ISDESCENDANTNODE(page, '/content/wknd/us/en/training-search')
AND page.[jcr:content/cq:tags] = 'training:activity/hiking'
ORDER BY page.[jcr:content/jcr:title] ASC
```

Para ejecutar esa misma ventana en una consola SQL2, configura límite 2 y offset 0 cuando existan esos campos; en código JCR son `Query.setLimit(2)` y `Query.setOffset(0)`. Si el formulario no los expone, compara sólo selección y orden sobre el conjunto pequeño. El archivo no incorpora paginación. [API JCR Query](https://developer.adobe.com/experience-manager/reference-materials/cloud-service/javadoc/javax/jcr/query/Query.html).

### C. Explicar la raíz amplia y la raíz correcta

1. Abre [Query Performance local](http://localhost:4502/libs/granite/operations/content/diagnosistools/queryPerformance.html). Elige **Explain Query** y **JCR-SQL2**.
2. Para esa interfaz, pega el `SELECT` de `guides.sql2`, **sin prefijo EXPLAIN**, y deja desmarcadas las tres opciones de ejecución descritas arriba. Pulsa **Explain**.
3. Conserva el texto del plan y las cuatro observaciones de la sección 1. El nombre/versionado del índice depende de tu SDK: no esperamos un `cqPageLucene` con sufijo fijo.
4. Cambia sólo la raíz a `/content/wknd/us/en` y vuelve a explicar con las mismas opciones. Es una selección más amplia: Outside trail pasa a estar dentro del alcance. No la ejecutes ni midas para buscar un tiempo lento; explicar basta para compararla.
5. Restaura la raíz `training-search`. Compara acceso, restricciones y orden. Es válido que ambas consultas seleccionen el mismo índice. Eso no demuestra que tengan el mismo trabajo ni que el índice sea insuficiente.

**Alternativa en CRXDE Lite:** abre **Tools → Query**, selecciona **JCR-SQL2** y ejecuta uno de estos archivos completos. Aquí sí se incluye `EXPLAIN`: el resultado es el plan, no las páginas. No pegues ambas sentencias a la vez.

[Descargar explain-broad.sql2](examples/session-27/explain-broad.sql2)

```sql
EXPLAIN
SELECT * FROM [cq:Page] AS page
WHERE ISDESCENDANTNODE(page, '/content/wknd/us/en')
AND page.[jcr:content/cq:tags] = 'training:activity/hiking'
ORDER BY page.[jcr:content/jcr:title] ASC
```

[Descargar explain-bounded.sql2](examples/session-27/explain-bounded.sql2)

```sql
EXPLAIN
SELECT * FROM [cq:Page] AS page
WHERE ISDESCENDANTNODE(page, '/content/wknd/us/en/training-search')
AND page.[jcr:content/cq:tags] = 'training:activity/hiking'
ORDER BY page.[jcr:content/jcr:title] ASC
```

La corrección de raíz **cambia intencionalmente la selección** para ajustarse al requisito. No presentamos las dos expresiones como equivalentes ni atribuimos una mejora medida a este cambio. La consulta amplia es incorrecta para Guide List aunque el SDK pequeño la ejecute rápido.

### D. Observar trabajo en el conjunto pequeño

1. Confirma que la raíz de prueba contiene únicamente las páginas suministradas, con dos coincidencias Hiking. Conserva la misma cuenta, contenido y orden.
2. En la consola SQL2 de CRXDE Lite, ejecuta `measure-bounded.sql2`. `MEASURE` **sí ejecuta** y consume resultados: la seguridad del ejemplo depende del conjunto pequeño, no de un supuesto límite dentro del archivo.
3. Lee cada `selector` y su `scanCount`. Anota también las rutas obtenidas con la consulta normal; los contadores solos no demuestran que los resultados sean correctos.
4. Si dispones de la tabla de Query Performance, compara sus campos **Scanned** y **Read**, conservando sus nombres. No los mezcles automáticamente con `scanCount`: pertenecen a salidas distintas y pueden observar diferente cantidad de resultados.
5. Repite sólo la consulta acotada bajo las mismas condiciones. Una segunda ejecución puede aprovechar caché. No prometas porcentajes de mejora con cinco páginas.

[Descargar measure-bounded.sql2](examples/session-27/measure-bounded.sql2)

```sql
MEASURE
SELECT * FROM [cq:Page] AS page
WHERE ISDESCENDANTNODE(page, '/content/wknd/us/en/training-search')
AND page.[jcr:content/cq:tags] = 'training:activity/hiking'
ORDER BY page.[jcr:content/jcr:title] ASC
```

**Resultado esperado, no ejecución registrada:** Forest y River son las dos coincidencias de la consulta normal. Explain muestra el plan que elija tu SDK; Measure informa contadores reales de esa ejecución. No hay un índice ni un número de lecturas garantizados. El material fue revisado contra documentación; no se ejecutó en tu instancia durante su preparación.

Si no puedes abrir Query Performance pero sí CRXDE, usa los archivos SQL2. Si tampoco están disponibles las herramientas o permisos, el instructor demuestra su instancia preparada y el grupo interpreta el caso sintético siguiente. No se requiere cambiar permisos globales ni desplegar índices para terminar la sesión.

<a id="evidencia"></a>

## 4. Comparar evidencia, no sólo el cronómetro

**Caso sintético de enseñanza: estos datos son inventados para explicar el diagnóstico, no mediciones del SDK.**

| Observación | Caso A | Caso B |
| --- | --- | --- |
| Usa un índice | Sí | Sí |
| Candidatos examinados | 8400 | 2 |
| Resultados devueltos | 2 | 2 |
| Ordenamiento | Fuera del índice | Dentro del índice |

Ambos casos entregan dos resultados. A exige investigar qué trabajo queda fuera del acceso; B ilustra una ejecución con poco descarte. La tabla no establece un umbral universal, no prueba que las ACL sean iguales y no predice que cambiar la ruta produzca exactamente B.

Para una conversación técnica basta conservar: consulta exacta, instancia/build del SDK, identidad usada, contenido y momento, límite/offset, plan, rutas de resultados y métricas con su nombre original. Es una ayuda de diagnóstico voluntaria, no una entrega evaluada. Si cambias una condición, anótala para no comparar experimentos diferentes.

<a id="indice"></a>

## 5. Leer una definición de índice

Desde el plan real, localiza el nodo indicado bajo `/oak:index` en CRXDE local y **sólo inspecciónalo**. Busca `type`, `compatVersion`, configuración asíncrona y reglas que cubran `cq:Page`. En las propiedades, `name` puede ser una ruta relativa o una expresión configurada; los nombres de nodos auxiliares no tienen que llamarse `tags` y `title`.

Este **fragmento ilustrativo** representa el nodo `properties` dentro de `indexRules/cq:Page`. Es un material de lectura, **no una definición completa ni un paquete instalable**. No se debe importar ni usar para reemplazar un índice existente.

[Descargar properties-review.json](examples/session-27/properties-review.json)

```json
{
  "jcr:primaryType": "nt:unstructured",
  "tags": {
    "jcr:primaryType": "nt:unstructured",
    "name": "jcr:content/cq:tags",
    "propertyIndex": true
  },
  "title": {
    "jcr:primaryType": "nt:unstructured",
    "name": "jcr:content/jcr:title",
    "propertyIndex": true,
    "ordered": true,
    "type": "String"
  }
}
```

`propertyIndex` aporta soporte para condiciones sobre la propiedad; `ordered` habilita su uso para ordenar y aumenta el trabajo/espacio de indexación. El título es monovalor en el ejemplo: no actives `ordered` sobre el array `cq:tags`. `evaluatePathRestrictions` permite resolver la restricción de ruta dentro del índice Lucene. `includedPaths` define qué se indexa y `queryPaths` interviene en qué consultas lo pueden seleccionar; deben alinearse. [Definición de índices Lucene — Oak](https://jackrabbit.apache.org/oak/docs/query/lucene.html).

En una revisión Cloud comprobaríamos `type=lucene`, `compatVersion=2` y un modo `async` admitido, además de las reglas necesarias. Para páginas, primero revisamos la extensión de un índice existente apropiado; no recortamos sus rutas o reglas compartidas con otras funcionalidades. Si se justifica un índice completamente nuevo, también se revisan su alcance y la política de selección por index tag. Ese index tag **no es** el tag editorial `training:activity/hiking`. [Índices Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/indexing), [selección por tags — Oak](https://jackrabbit.apache.org/oak/docs/query/query-engine.html#query-option-index-tag).

<a id="cloud"></a>

## 6. Decidir el siguiente cambio

| Hallazgo | Siguiente paso |
| --- | --- |
| La raíz o filtros contradicen el requisito. | Corrige la consulta y vuelve a comprobar incluidos/excluidos. |
| Aparece traversal. | Revisa consulta, definición disponible y plan; identifica la cobertura que falta. |
| Hay índice, pero muchas lecturas. | Busca filtrado posterior, orden, conteo, offset y restricciones poco selectivas. |
| Los resultados nuevos aún no aparecen. | Comprueba guardado, ruta, identidad y actualización del índice. |
| Falta cobertura después de corregir la consulta. | Documenta el caso y revisa una extensión versionada del índice adecuado. |

En Cloud, una modificación se versiona en el proyecto y se despliega mediante el pipeline de Cloud Manager. Se comprueban las consultas afectadas y la compatibilidad con el despliegue; editar un índice de producción o marcar `reindex=true` a mano no forma parte de ese proceso. La definición local puede diferir de la Cloud. Aquí leemos el flujo documentado, sin asumir acceso ni ejecutar un despliegue. [Despliegue de índices — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/indexing#deploying-custom-index-definitions).

<a id="repaso"></a>

## 7. Repaso con respuestas

1. **¿Dos hits prueban que se leyeron dos candidatos?** No; pueden haberse filtrado u ordenado muchos más.
2. **¿El nombre de un índice basta para aprobar una consulta?** No; hay que revisar restricciones, orden y trabajo observado.
3. **¿El coste del plan son milisegundos?** No, es una estimación para seleccionar el acceso.
4. **¿EXPLAIN MEASURE ejecuta la consulta de resultados?** No; devuelve plan y coste estimado. `MEASURE` por sí solo sí ejecuta.
5. **¿Por qué Outside trail deja de pertenecer al resultado?** La raíz correcta es `training-search`; la corrección restaura el contrato.
6. **¿Qué pasa si ambos planes usan el mismo índice?** Puede ser correcto; compara cobertura y alcance, sin inventar una mejora.
7. **¿Debemos activar ordered sobre cq:tags?** No, es multivalor; aquí el orden solicitado corresponde al título.
8. **¿Instalamos properties-review.json?** No; es un fragmento para leer, no un índice desplegable.
9. **¿Cómo se cambia un índice Cloud?** Mediante definición revisada/versionada y pipeline, con comprobaciones posteriores.

<a id="fuentes"></a>

## Fuentes y continuidad

Fuentes oficiales de Adobe y Apache enlazadas junto al contenido. Consulta documental: 20 de septiembre de 2026. [Calendario nuevo](eleven-week-redesign-proposal.html): la 26 define tags y consultas; la 27 diagnostica su coste; la 28 estudia identidades y ACLs y la 29 el acceso mediante resolvers. El SDK pequeño permite aprender a inspeccionar; no sustituye una evaluación de carga representativa.
