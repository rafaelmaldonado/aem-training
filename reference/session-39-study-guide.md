# Sesión 39 · Diagnosticar AEM Cloud con la herramienta adecuada

**Jueves 8 de octubre de 2026 · Semana 8 · 30 minutos**

[Versión HTML](session-39-study-guide.html) · [Slides en inglés](../lessons/0039-cloud-diagnostic-tools.html#slide-deck)

## Objetivo observable

Ante una respuesta 500 en Publish que no ocurre en Author, escoger la **siguiente herramienta según una hipótesis concreta**, citar qué evidencia aporta y formular una conclusión que no exceda esa evidencia. La sesión usa una ficha didáctica inventada; no requiere acceso a Cloud Manager, Developer Console ni RDE, ni pide un despliegue o ejercicio posterior.

La sesión 38 explicó cómo llega un valor a un servicio. Aquí se examina el **estado efectivo del runtime** y del contenido cuando una petición falla. No se vuelve a enseñar la selección de archivos `.cfg.json`; si aparece una configuración como posible causa, se comprueba después de observar el componente afectado.

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–5 | 1–2 | Presentar el caso y fijar ambiente, tier, ruta, hora y códigos. |
| 5–9 | 3 | Relacionar cuatro preguntas con cuatro herramientas. |
| 9–17 | 4–5 | Correlacionar un log y leer bundle, componente y referencia. |
| 17–21 | 6 | Comprobar la presencia del contenido en Publish. |
| 21–27 | 7–8 | Explicar el flujo RDE y sus comandos CLI. |
| 27–29 | 9 | Formular el diagnóstico limitado. |
| 29–30 | 10 | Preguntas y cierre. |

## 1. Elegir la herramienta por la pregunta

| Pregunta | Herramienta | Evidencia que buscas | Lo que no demuestra sola |
| --- | --- | --- | --- |
| ¿Qué ocurrió alrededor de la petición fallida? | Logs de Cloud del servicio y ventana temporal afectados | Petición, status, error y contexto correlacionable | La causa raíz sólo por compartir hora. |
| ¿Está activo el bundle y satisfecho el componente? | AEM Developer Console | Estado de bundles, componentes, referencias y configuraciones | Que una corrección ya fue desplegada o que todos los pods se comportan igual. |
| ¿Existe el recurso en el tier afectado? | Repository Browser | Path, nodos y propiedades visibles en Author, Publish o Preview | Que la página renderice bien o que toda identidad tenga acceso. |
| ¿Una corrección candidata reproduce y cambia el resultado? | RDE | Antes/después con código y configuración comparables | Pasar los gates de Cloud Manager o equivalencia con producción. |

En Cloud, Developer Console ofrece herramientas de **sólo lectura** para estado OSGi. No es el Web Console editable del SDK local. Repository Browser también es de sólo lectura y respeta el acceso del usuario; la ausencia de un nodo en su vista puede ser una cuestión de permisos. Los logs se pueden descargar desde Cloud Manager o consultar por CLI, según el acceso disponible. [Developer Console — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/aem-developer-console) · [Repository Browser — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developer-tools/repository-browser) · [Gestionar logs — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/manage-logs).

## 2. Caso guiado: Author responde 200 y Publish responde 500

**Todos los resultados, nombres y horarios de esta sección son inventados.** Una petición a `/content/wknd/en/guides.html` devuelve 200 en Author y 500 en Publish. Esa diferencia delimita el tier que investigar, pero **no prueba** que el contenido, la configuración o el código sean idénticos entre tiers.

La ficha de logs suministra estas dos líneas simplificadas de Publish:

```text
14:05:17 GET /content/wknd/en/guides.html 500
14:05:17 ERROR GuideListModel: CatalogService unavailable
```

Se consulta el log del ambiente y servicio correctos y se acota por hora y ruta. Las líneas acercan el diagnóstico al servicio utilizado por la página. En una investigación real hay que correlacionar además el identificador de petición o el contexto del log; una hora coincidente no basta para demostrar causalidad. El texto «unavailable» tampoco indica por sí mismo si faltó un bundle, una configuración o una dependencia. [Acceso a logs — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/manage-logs).

La ficha simulada de Developer Console para **Publish** muestra:

| Elemento | Estado ilustrativo | Lectura |
| --- | --- | --- |
| Bundle `wknd.core` | `ACTIVE` | El bundle inició; no garantiza que todos sus componentes estén activos. |
| Componente `CatalogService` | `UNSATISFIED` | No está disponible como servicio en ese estado. |
| Referencia obligatoria `CatalogClient` | `MISSING` | Hay que investigar el proveedor de esa referencia y su configuración. |

La consola permite comprobar estados de bundles, componentes, servicios y configuraciones. Una referencia insatisfecha delimita la siguiente búsqueda, pero **no identifica aún por qué falta**. Revisa si el proveedor está instalado y activo, si registra el servicio esperado y si su configuración efectiva permite la activación. Compara con Author sólo después de fijar el estado de Publish. [AEM Developer Console — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/aem-developer-console).

Por último, la ficha de Repository Browser muestra `/content/wknd/en/guides/jcr:content` en Author y Publish. Esto descarta, **para esta ficha y con esa visibilidad**, la hipótesis simple de que falta por completo el nodo base en Publish. No descarta referencias ausentes, permisos distintos, propiedades incorrectas ni fallos de render. En un caso real selecciona el ambiente y tier adecuados y toma en cuenta los permisos con los que se abrió el navegador. [Repository Browser — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developer-tools/repository-browser).

## 3. Qué aporta un RDE

El RDE permite sincronizar código, configuración y contenido desde herramientas locales para iterar con rapidez. **Este apartado es una referencia teórica: no hay un RDE disponible para esta clase.** Un equipo con acceso primero intentaría reproducir la respuesta 500 con artefactos y datos comparables al ambiente afectado; después probaría **una** corrección candidata y comprobaría tanto la respuesta HTTP como el estado del componente. Si no se reproduce el 500, un 200 posterior en RDE sería evidencia débil para explicar el incidente original.

La sincronización de RDE no pasa por una pipeline de Cloud Manager. Tras validar una hipótesis allí, el cambio debe seguir el flujo normal hacia Development y sus gates antes de considerarse para entornos posteriores. Un RDE es para desarrollo, análisis de errores y pruebas funcionales acotadas; no equivale a stage ni producción. Su reset elimina el código y contenido actuales, así que coordina su uso cuando sea compartido. No se hará reset ni despliegue en esta sesión. [RDE — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/rapid-development-environments).

### Comandos de la slide 08

Como referencia, con AIO CLI, el plugin RDE, permisos y un ambiente disponible, la secuencia sería:

```sh
aio login
aio aem:rde:setup
aio aem:rde:status
aio aem:rde:install <artifact.zip>
aio aem:rde:history
```

`<artifact.zip>` representa un paquete construido para el proyecto, no un archivo incluido en este repositorio. `setup` elige el RDE; `status` comprueba disponibilidad y despliegues; `install` sincroniza el artefacto; `history` muestra el historial. Sin opción de servicio, la instalación apunta a Author y Publish. Confirma que la selección de RDE es correcta antes de instalar. Estos comandos **no se ejecutaron** para preparar la clase. [Comandos RDE — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/rapid-development-environments#rde-command-line-tools-commands).

## 4. Conclusión defendible

> «En la ficha inventada, Publish devuelve 500 para la ruta indicada; el log de esa petición apunta a `CatalogService`; Developer Console muestra el componente insatisfecho por la referencia `CatalogClient`; el nodo base existe en Publish. La siguiente comprobación es averiguar por qué no está disponible `CatalogClient`. Una corrección candidata se probaría en RDE y después por la pipeline normal».

Todavía **no** se puede afirmar que faltó desplegar un bundle concreto ni que la incidencia esté corregida. Una posible explicación es un proveedor ausente; otra, que el proveedor exista pero no se active por configuración o dependencia. La comprobación del proveedor distingue esas hipótesis.

## Repaso con respuestas

1. **¿Por qué abrir primero logs de Publish?** Porque el 500 observado pertenece a Publish; una traza de Author respondería otra pregunta.
2. **¿Un bundle `ACTIVE` prueba que `CatalogService` está activo?** No. El estado del componente y sus referencias se comprueba aparte.
3. **¿Qué significa ver `jcr:content` en Publish?** El nodo base está visible con esa identidad; no demuestra render, acceso universal ni publicación de todas las referencias.
4. **¿Qué compruebas tras leer `CatalogClient → MISSING`?** El proveedor del servicio, su bundle, su registro y la configuración o dependencias que condicionan su activación.
5. **¿Por qué no basta un 200 en RDE?** Primero hay que reproducir el 500 en condiciones comparables; además RDE no ejecuta los gates de la pipeline.

## Fuentes oficiales

- [AEM as a Cloud Service Developer Console — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/aem-developer-console)
- [Repository Browser — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developer-tools/repository-browser)
- [Access and manage logs — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/manage-logs)
- [Rapid Development Environments — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/rapid-development-environments)
