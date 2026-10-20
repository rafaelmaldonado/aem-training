# Sesión 48 · Accesibilidad y SEO en una página AEM

**Miércoles 21 de octubre de 2026 · Semana 10 · 30 minutos**

[Versión HTML](session-48-study-guide.html) · [Slides en inglés](../lessons/0048-accessibility-seo-page-audit.html#slide-deck) · [Práctica voluntaria de la semana 10](wknd-project-backlog.html#practice-10)

## Objetivo observable

Revisar una página Sites de práctica como visitante: recorrerla con teclado, comprobar foco, nombres y estructura, y observarla a 320 CSS px sin perder contenido ni funciones. Corregir en Author un título de sección, el texto de un enlace y el texto alternativo de una imagen informativa. Después inspeccionar el HTML entregado por Publish para verificar título de documento, canonical y directivas de indexación; comprobar que la URL del sitemap coincide con la URL pública elegida. Registrar un hallazgo y su evidencia después de la corrección.

La sesión 47 comprobó con Cypress que un título publicado era visible. Esta sesión examina **cómo** se usa y describe esa página. Una puntuación de Lighthouse orienta la revisión, pero no sustituye el recorrido manual. Los ejemplos de UI y de dominio público de las slides son ilustrativos; los resultados se convierten en evidencia sólo al ejecutarlos en el SDK o en un ambiente autorizado.

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–5 | 1–3 | Definiciones y página de práctica. |
| 5–12 | 4–5 | Teclado, reflow y correcciones en Author. |
| 12–22 | 6–7 | Señales SEO y evidencia de Publish. |
| 22–28 | 8–9 | Herramientas de auditoría y repaso. |
| 28–30 | 10 | Preguntas. |

## Términos del caso

**Accesibilidad** significa que las personas pueden percibir, navegar y usar la página. **WCAG** (*Web Content Accessibility Guidelines*) es el conjunto de criterios del W3C para contenido web accesible. Esta sesión comprueba algunos comportamientos observables; no es una auditoría completa de conformidad. **SEO** (*Search Engine Optimization*) reúne prácticas que ayudan a los buscadores a descubrir y entender páginas públicas, sin garantizar una posición en resultados. [W3C: WCAG](https://www.w3.org/WAI/standards-guidelines/wcag/) · [Google: requisitos técnicos](https://developers.google.com/search/docs/essentials/technical).

En la revisión, **foco** es el control activo para el teclado y **reflow** es la adaptación del contenido a un viewport estrecho. **Nombre accesible** es el texto que la tecnología de apoyo anuncia para un control; **alt** comunica el propósito de una imagen informativa. Para SEO, **canonical** expresa la URL pública preferida, las **directivas robots** controlan rastreo o indexación y un **sitemap** enumera URLs que ayudan al descubrimiento. Las slides introducen cada término junto a su comprobación.

## Caso de práctica

En una rama o carpeta desechable de WKND, crea `guide-48-lab` con el título visible **River walk**. Usa un Core Title como encabezado principal, un Core Image informativo de una ruta junto al río y un Core Text con un enlace a una página de mapa de práctica. El enlace inicial dice `Click here`; la imagen tiene un texto alternativo genérico; y el Title usa un nivel que no corresponde a la jerarquía observada. Estos defectos son **datos del ejercicio**, no una afirmación sobre WKND por defecto. Mantén sólo componentes permitidos por el template de práctica.

El contrato de la página al terminar es:

| Área | Evidencia esperada |
| --- | --- |
| Teclado | El enlace se alcanza y activa con teclado; el foco se ve y el orden tiene sentido. |
| Estructura | El encabezado principal es `h1`; los siguientes niveles describen secciones reales. |
| Nombres | El enlace dice `Open the river trail map`; la imagen informativa describe la escena. Si fuera decorativa, se marcaría como tal. |
| Reflow | A 320 CSS px se lee el contenido vertical sin desplazamiento horizontal de página ni pérdida de controles. |
| SEO | La respuesta de Publish tiene un `<title>` específico, una canonical de la URL pública correcta, y una directiva robots coherente con la intención de indexar. |
| Descubrimiento | El sitemap publicado, si está configurado, lista esa misma URL canónica y ninguna URL de Author o de laboratorio. |

## Accesibilidad: comprobar antes de corregir

1. Abre la página en **Publish local** como visitante, o en vista previa sin modo de edición si sólo tienes Author. Indica en el registro qué entorno usaste. No confundas el editor de Author con la página entregada a visitantes.
2. Desde el inicio de la página, usa `Tab` y `Shift+Tab`. Anota el orden de enlaces y controles. Activa el enlace con `Enter`; confirma el destino. Comprueba que el indicador de foco permanece visible y que ningún encabezado fijo lo tapa. Si el foco desaparece, inspecciona CSS del componente o del template antes de atribuirlo al contenido. [W3C: Focus Order](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html) · [W3C: Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible).
3. Inspecciona el árbol de encabezados y los nombres accesibles con las herramientas del navegador. El Core Title permite elegir nivel de encabezado; selecciona `h1` para el título principal sólo si el template no lo emite ya. Cambia `Click here` por **Open the river trail map**. El destino debe seguir siendo la página del mapa. [Adobe: Title Component](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/wcm-components/title) · [W3C: Link Purpose](https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context).
4. En el Core Image, describe la información que aporta la imagen, por ejemplo **Hikers following the river trail**. Si la imagen sólo repite información y es decorativa, usa la opción de imagen decorativa y comprueba el `alt` emitido. No inventes una descripción a partir del nombre del archivo. [Adobe: Image Component](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/wcm-components/image) · [W3C: Non-text Content](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html).
5. Reduce el viewport a **320 CSS px** o usa un viewport inicial de 1280 CSS px con zoom al 400 %. Recorre toda la página y comprueba que el texto y los controles siguen disponibles sin scroll horizontal de página. El zoom al 200 % puede ser una comprobación adicional, pero no equivale por sí solo al caso de reflow de 320 CSS px. [W3C: Reflow](https://www.w3.org/WAI/WCAG21/Understanding/reflow).

La corrección de contenido sólo cubre los controles que el autor puede configurar. Si el foco, el orden del DOM o el reflow fallan por CSS, HTL o estructura del template, registra el componente y la evidencia para una corrección de código. No marques ese fallo como resuelto por cambiar un campo de Author.

## SEO: propiedades y salida entregada

En **Page Properties**, establece un título de documento específico, por ejemplo `River walk guide | Weekend Guides`, y una descripción fiel al contenido. El Core Title visible y el `<title>` del documento tienen propósitos distintos; revisa ambos en el HTML. La disponibilidad y el nombre de las propiedades dependen del tipo de página y su implementación. [Adobe: Page Properties](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/authoring/sites-console/page-properties).

Para una página que debe aparecer en buscadores, revisa estas señales como conjunto:

| Señal | Qué comprobar en Publish | Riesgo si difiere |
| --- | --- | --- |
| Respuesta | URL pública responde correctamente y muestra contenido indexable. | Un error o una página privada impide indexación. |
| Canonical | Hay una única URL absoluta preferida con dominio y protocolo públicos correctos. | Duplicados, `localhost` o un dominio equivocado confunden la URL preferida. |
| Robots | No hay `noindex` en meta ni en cabecera `X-Robots-Tag`; `robots.txt` permite rastreo cuando corresponde. | `noindex` excluye la página; bloquear el rastreo puede impedir ver la directiva. |
| Sitemap | La URL que se incluye coincide con la canonical y pertenece al sitio publicado. | El mapa anuncia una URL distinta de la elegida como preferida. |

La propiedad **Canonical Url** puede sobrescribir la URL canónica; si se deja vacía, AEM usa la URL de la página según su configuración. Verifica el `<link rel="canonical">` **real** antes de publicar un cambio: Externalizer, mappings, protocolo recibido y personalizaciones del template pueden alterar el resultado. No pegues una URL de `example.org` o `localhost` como canonical de producción. [Adobe: Page Properties](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/authoring/sites-console/page-properties) · [Adobe: SEO and URL Management](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/overview/seo-and-url-management) · [Adobe: canonical diagnosis](https://experienceleague.adobe.com/en/docs/experience-cloud-kcs/kbarticles/ka-34775).

La opción **Generate Sitemap** marca una raíz de sitemap para la página y sus descendientes cuando el sitio está configurado para ello. Abre el sitemap de **Publish** que corresponda a la raíz real; revisa las URLs emitidas. Un sitemap ayuda al descubrimiento, pero no garantiza indexación ni ranking. Una canonical expresa preferencia y Google puede elegir otra URL. Para excluir una página de resultados, `noindex` es la señal apropiada; `robots.txt` controla rastreo y no protege contenido sensible. [Adobe: SEO and URL Management](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/overview/seo-and-url-management) · [Google: canonicalization](https://developers.google.com/search/docs/crawling-indexing/canonicalization) · [Google: technical requirements](https://developers.google.com/search/docs/essentials/technical).

## Demo local · Author SDK y Publish

**Preparación previa del instructor:** SDK Author y Publish locales, proyecto WKND instalado, permiso para crear una página desechable, Core Title/Image/Text disponibles y una imagen de práctica. Anota la URL real de Publish y una página de mapa de práctica para que el enlace tenga destino. Si sólo está disponible Author, ejecuta la parte de autoría y accesibilidad en preview, y deja canonical, robots y sitemap como plan de verificación para Publish. No hay acceso confirmado a Cloud Manager.

1. Crea `guide-48-lab` con los defectos controlados descritos arriba. Registra URL, entorno, título, nivel del encabezado, texto del enlace y alt iniciales. Usa una imagen con contenido que se pueda describir de forma honesta.
2. Publica la página y sus dependencias. Abre la URL de Publish sin credenciales y toma una línea base: navegación de teclado, árbol de encabezados, nombre del enlace, alt y ancho a 320 CSS px.
3. En Author, corrige el nivel del Core Title, el texto del enlace y el alt o la marca decorativa del Core Image. Comprueba que el destino del enlace no cambió. Revisa el título y la descripción en Page Properties. Publica de nuevo.
4. Repite las comprobaciones manuales en Publish. Guarda una captura del foco visible y una nota del recorrido a 320 CSS px. Si hay un fallo del template, regístralo con selector o componente responsable y no lo declares corregido.
5. En el HTML y la respuesta HTTP de Publish, anota el `<title>`, la canonical, cualquier directiva robots y la URL pública. Revisa `robots.txt` y el sitemap publicado **si el sitio los tiene configurados**. Compara la URL del sitemap con la canonical. No infieras indexación real a partir del SDK local.
6. Ejecuta Lighthouse sobre la misma URL como ayuda para localizar auditorías de accesibilidad y SEO. Revisa el hallazgo concreto y repite el control manual correspondiente. Registra la versión de página y el entorno. Las puntuaciones entre entornos o ejecuciones no bastan para demostrar la corrección.

**Limpieza:** conserva el registro de hallazgos y elimina sólo la página, la página de mapa y los assets creados para esta práctica, después de confirmar que no son recursos compartidos.

## Lighthouse y Experience Audit

Lighthouse produce auditorías de accesibilidad y SEO para una URL. Usa sus hallazgos como pistas: su cobertura automática no agota WCAG, y la categoría SEO no certifica indexación. El recorrido de teclado, el foco, los nombres y el reflow necesitan observación manual. [Chrome: Lighthouse](https://developer.chrome.com/docs/lighthouse) · [Chrome: accessibility scoring](https://developer.chrome.com/docs/lighthouse/accessibility/scoring/).

Experience Audit de Cloud Manager usa Lighthouse en pipelines de producción y muestra resultados de páginas configuradas, con categorías y diferencias respecto a auditorías anteriores. En este curso sólo se interpreta un reporte o ejemplo documental, porque no hay acceso confirmado a Cloud Manager. Un Lighthouse local no prueba que la pipeline haya ejecutado Experience Audit. [Adobe: Experience Audit dashboard](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/reports/report-experience-audit).

## Diagnóstico rápido

| Síntoma | Primera comprobación |
| --- | --- |
| El enlace se ve pero no recibe foco | HTML emitido, elemento interactivo real y CSS de foco. |
| El foco queda tapado | Encabezado fijo, scroll y estilo de foco en viewport pequeño. |
| Hay dos `h1` o ninguno | Core Title, título emitido por el template y jerarquía real del DOM. |
| La imagen sigue con alt genérico | Opción de heredar alt del DAM, campo del componente y HTML publicado. |
| La canonical usa `localhost` | Dominio público, Externalizer, mappings, `X-Forwarded-Proto` y personalización del head. |
| La página no aparece en sitemap | Raíz configurada, estado de publicación, URL canónica y sitemap de Publish. |
| Lighthouse mejora pero el teclado falla | Auditoría automática limitada; reproduce el recorrido manual. |

## Repaso con respuestas

1. **¿Un Lighthouse alto prueba conformidad WCAG?** No. Revisa manualmente teclado, foco, estructura, nombres y reflow del caso.
2. **¿El texto `Click here` permite entender el destino?** Es ambiguo sin contexto. `Open the river trail map` describe la acción y el destino.
3. **¿Qué diferencia hay entre `h1` y `<title>`?** `h1` estructura el contenido visible; `<title>` identifica el documento en pestaña y resultados de búsqueda. Ambos se inspeccionan en la salida.
4. **¿Poner la URL en el sitemap garantiza indexación?** No. Comprueba acceso, directivas, canonical y contenido; el buscador decide si indexa.
5. **¿Qué demuestra la demo local?** El comportamiento y HTML de la instancia observada. No demuestra un resultado en CDN, Google ni Cloud Manager.

## Fuentes

- [Adobe · Page Properties](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/authoring/sites-console/page-properties)
- [Adobe · SEO and URL Management](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/overview/seo-and-url-management)
- [Adobe · Core Title](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/wcm-components/title) y [Core Image](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/wcm-components/image)
- [Adobe · Experience Audit](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/reports/report-experience-audit)
- [W3C · WCAG 2.2 Understanding](https://www.w3.org/WAI/WCAG22/Understanding/)
- [Google · Search technical requirements](https://developers.google.com/search/docs/essentials/technical) y [canonicalization](https://developers.google.com/search/docs/crawling-indexing/canonicalization)
- [Chrome · Lighthouse](https://developer.chrome.com/docs/lighthouse)
