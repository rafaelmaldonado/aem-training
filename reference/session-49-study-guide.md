# Sesión 49 · Medir y corregir un cuello de botella en AEM

**Jueves 22 de octubre de 2026 · Semana 10 · 30 minutos**

[Versión HTML](session-49-study-guide.html) · [Slides en inglés](../lessons/0049-performance-bottleneck.html#slide-deck) · [Práctica voluntaria de la semana 10](wknd-project-backlog.html#practice-10)

## Objetivo observable

En una página Sites de práctica, establecer una línea base repetible, atribuir el retraso a una capa con evidencia, acordar un presupuesto concreto y aplicar **un solo cambio**. Repetir la medición bajo las mismas condiciones y decidir si el cambio mejoró la experiencia sin alterar el contenido. La clase usa como caso una imagen principal demasiado pesada; no presupone que todas las páginas lentas tengan ese problema.

La sesión 48 comprobó uso y señales de una página publicada. Aquí se mide cuánto tarda en presentar su contenido principal. Las cifras de ejemplo de esta guía y de las slides son **datos didácticos simulados**, no mediciones de WKND, del SDK ni de un entorno Cloud. Sólo las cifras recogidas en la URL real del participante cuentan como resultado de la demo.

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–4 | 1–2 | Resultado esperado, métricas y presupuesto. |
| 4–9 | 3–4 | Separar capas y fijar un protocolo comparable. |
| 9–14 | 5–6 | Leer el caso y atribuir el cuello de botella. |
| 14–22 | 7–8 | Cambiar la imagen y comparar resultados. |
| 22–28 | 9 | Comprobar calidad y decidir siguiente paso. |
| 28–30 | 10 | Preguntas. |

## Términos y contrato de medición

**Línea base** es el conjunto de mediciones antes del cambio, con URL, versión, dispositivo, red, caché y método registrados. **Cuello de botella** es la etapa cuya mejora podría reducir el tiempo que importa al usuario. **Presupuesto** es el límite acordado antes de intervenir. **TTFB** (*Time to First Byte*) mide hasta el primer byte de la respuesta HTML e incluye red y espera del servidor; no es, por sí solo, «tiempo de AEM». **LCP** (*Largest Contentful Paint*) marca cuándo se representa el elemento de contenido más grande en el viewport; identifica el elemento real en la traza. [Chrome: Network timing](https://developer.chrome.com/docs/devtools/network/reference/) · [web.dev: optimizar LCP](https://web.dev/articles/optimize-lcp).

Usa una URL de **Publish local** que sirva una página `guide-49-lab` basada en la página de práctica de la 48. Coloca un Core Image visible al inicio con una foto informativa del río. Para preparar el ejercicio, conserva dos assets visualmente equivalentes: una variante pesada y una variante optimizada con dimensiones suficientes para el tamaño mostrado. No se reemplaza una fotografía real de producción sin revisar nitidez, recorte, derechos y texto alternativo. La variante pesada es un **defecto controlado** de esta práctica, no una propiedad por defecto del Core Image.

El contrato del caso es:

| Elemento | Criterio acordado para esta práctica |
| --- | --- |
| Escenario | Misma URL de Publish, viewport móvil de 390 × 844 CSS px, mismo perfil de red/CPU de DevTools, recarga de primera visita con caché del navegador limpia y sin otros cambios de página. |
| Muestras | Una ejecución de calentamiento y **cinco** mediciones antes y después; comparar medianas, conservar los cinco valores y anotar la variación. |
| Presupuesto didáctico | Mediana de LCP ≤ 3,0 s y transferencia de la imagen LCP ≤ 300 kB en el escenario elegido; calidad visual y alt correctos. Son límites del laboratorio, no un estándar universal de AEM. |
| Restricción | Cambiar sólo el asset del Core Image; conservar URL de página, copy, posición, dimensiones de presentación y configuración de caché. |

Los resultados pueden variar incluso con el mismo protocolo. Una diferencia pequeña dentro de la dispersión observada no justifica atribuir una mejora. Lighthouse puede orientar, pero usa la traza de Performance y Network para identificar el elemento LCP y el recurso que realmente descargó el navegador. No uses únicamente la puntuación agregada de Lighthouse. [Chrome: Lighthouse](https://developer.chrome.com/docs/devtools/lighthouse/) · [web.dev: LCP por etapas](https://web.dev/articles/optimize-lcp).

## Localizar la primera etapa lenta

Sigue la ruta de una solicitud antes de tocar código o contenido:

```text
navegador → CDN (si existe) → Dispatcher → Publish → componente/consulta
          ↘ HTML → CSS/JS (clientlibs) → imagen LCP → render del navegador
```

El SDK local normalmente permite observar navegador y Publish, pero puede no incluir CDN ni Dispatcher. En ese caso marca esas capas como **no observadas**; no inventes un hit o miss. Si tu entorno sí tiene Dispatcher, registra si el recurso es cacheable y el resultado de caché con los logs o encabezados de diagnóstico configurados. Un TTFB alto en el navegador no demuestra una consulta lenta: primero separa conexión/red, caché y tiempo de respuesta de Publish. Para investigar Publish, correlaciona la solicitud con `request.log`; si aparece una consulta costosa, inspecciona su plan y alcance antes de cambiar índices. [Adobe: caching in AEM Cloud Service](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching) · [Adobe: Dispatcher debug](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration#debug) · [Adobe: análisis de consultas lentas](https://experienceleague.adobe.com/en/docs/experience-manager-65/content/implementing/developing/bestpractices/troubleshooting-slow-queries).

| Observación | Primera comprobación | Capa posible |
| --- | --- | --- |
| HTML tarda en entregar el primer byte; Publish también registra demora | `request.log`, componente y, si existe, consulta/plan | Backend o consulta. |
| Publish responde rápido, pero un miss del Dispatcher tarda y el hit no | Elegibilidad, invalidación, headers y logs de caché | Caché; sólo si Dispatcher está presente. |
| HTML llega pronto; el recurso LCP inicia tarde | Descubrimiento, prioridad, `loading`, CSS/JS que bloquea | Navegador o clientlibs. |
| Recurso LCP inicia pronto pero descarga muchos bytes | URL, dimensiones reales, formato y tamaño transferido | Imagen. |
| Recurso LCP termina pronto pero se pinta tarde | Traza de tareas principales, estilos y scripts | Render del navegador/clientlibs. |

Esta tabla propone **hipótesis**, no diagnósticos automáticos. Adobe documenta que Core Image entrega imágenes responsivas y que las anchuras se configuran en el design dialog; el SDK local usa Adaptive Image Servlet cuando no dispone del servicio de imágenes optimizadas de AEM Cloud. Verifica la URL y los bytes recibidos en Network antes de afirmar qué formato o variante se sirvió. [Adobe: Core Image](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/wcm-components/image) · [Adobe: Adaptive Image Servlet](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/adaptive-image-servlet) · [Adobe: Web-Optimized Image Delivery](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/web-optimized-image-delivery).

## Caso didáctico: una hipótesis comprobable

La siguiente tabla es **simulada**. Muestra cómo leer un resultado, no promete lo que ocurrirá en tu SDK:

| Antes de cambiar | Valor ilustrativo | Lectura |
| --- | --- | --- |
| Mediana TTFB del HTML | 0,18 s | No aparece como la etapa dominante del caso. |
| Imagen identificada como elemento LCP | 1,6 MB transferidos | Recurso candidato a optimizar. |
| Descarga de esa imagen | 1,9 s | Una parte grande del recorrido de LCP. |
| Mediana LCP de cinco corridas | 3,6 s | Supera el presupuesto didáctico de 3,0 s. |

**Hipótesis:** sustituir esa imagen por una variante visualmente equivalente y más ligera reducirá bytes y duración de descarga, y puede reducir el LCP. La reducción de bytes **no garantiza** una reducción de LCP: el tiempo ahorrado puede trasladarse a espera de render u otra etapa. La medición posterior debe comprobar ambos resultados. [web.dev: optimizar LCP](https://web.dev/articles/optimize-lcp).

## Demo local · Author SDK y Publish

**Preparación previa del instructor, fuera de los 30 minutos:** SDK Author y Publish, una página desechable, acceso a Core Image y dos imágenes de práctica con licencia y alt apropiados. Publica la versión inicial y confirma que Publish sirve la foto pesada; anota la URL real. Elige un perfil de DevTools disponible en tu Chrome y mantenlo fijo. Si sólo hay Author, documenta que la medición es de preview y que falta validar Publish. No se asume acceso a CDN, Dispatcher ni Cloud Manager.

1. Abre la URL de Publish como visitante en Chrome. En DevTools, fija viewport **390 × 844 CSS px**, perfil de red y ralentización de CPU, y primera visita con caché del navegador limpia. Registra versión de Chrome, URL, estado HTTP y condiciones. No cambies el perfil entre corridas. Cierra pestañas o procesos que alteren mucho la máquina.
2. Haz una corrida de calentamiento y cinco mediciones de navegación con Performance/Lighthouse bajo el mismo protocolo. Conserva los valores individuales de LCP y la mediana. En Network, anota TTFB del documento, URL/tamaño transferido/duración de la imagen LCP, clientlibs relevantes y si los recursos salieron de red o caché. Identifica el elemento LCP en la traza: no presupongas que es la imagen.
3. Decide la capa responsable a partir de las observaciones. Si la imagen no es LCP o su descarga no domina, **no apliques este cambio como solución de rendimiento**: registra la capa sospechada y la siguiente comprobación de la tabla anterior. Para el caso preparado, verifica que la imagen pesada sí es el recurso LCP y que su descarga tiene peso material.
4. En Author, cambia sólo el asset del Core Image a la variante optimizada. Conserva el encuadre informativo y el alt; confirma que las dimensiones sirven para el viewport elegido. Publica el nuevo asset y la página según las dependencias observadas. Revisa en Publish la URL final del recurso, tipo, dimensiones, bytes transferidos y calidad visual. No supongas WebP en el SDK local: puede responder el Adaptive Image Servlet.
5. Repite la corrida de calentamiento y cinco mediciones con las mismas condiciones. Compara medianas y rangos, elemento LCP, bytes, duración de descarga y TTFB. Si el LCP cambió de elemento, anótalo. Comprueba también que la página sigue accesible y sin imagen borrosa o recortada de forma engañosa.
6. Decide frente al presupuesto. Si se cumplen LCP, bytes y calidad, conserva el cambio y registra evidencia. Si sólo bajan los bytes, inspecciona la etapa siguiente en la traza. Si la diferencia es comparable al ruido, repite con más corridas o en un entorno controlado; no declares victoria a partir de una sola ejecución.

| Registro mínimo | Antes | Después |
| --- | --- | --- |
| URL, versión publicada y condiciones | Anotar | Las mismas, salvo el asset. |
| LCP de las cinco corridas y mediana | Anotar | Anotar. |
| Elemento LCP y URL de imagen | Anotar | Anotar. |
| Bytes y duración del recurso | Anotar | Anotar. |
| TTFB del documento y estado de caché observable | Anotar | Anotar. |
| Calidad, alt y contenido | Anotar | Confirmar. |

**Limpieza:** conserva capturas, trazas y tabla. Elimina sólo la página y los assets creados para el laboratorio cuando ya no los necesites, después de comprobar que nadie más los usa.

## Ejemplo de decisión después del cambio

Un resultado **simulado** podría ser: imagen de 1,6 MB → 260 kB; mediana LCP de 3,6 s → 2,7 s; TTFB de 0,18 s → 0,19 s; elemento LCP igual; alt y calidad correctos. Bajo el protocolo acordado, cumple los dos límites del laboratorio y apoya la hipótesis de que la transferencia era material. Es una inferencia sobre ese escenario medido, no una promesa para usuarios reales. Si sólo baja el tamaño del archivo pero LCP permanece en 3,6 s, la mejora de transferencia es real, pero el cuello de botella de LCP sigue sin resolver.

La imagen optimizada de AEM Cloud requiere un entorno AEM as a Cloud Service; no se valida activándola en `localhost`. En una implementación real, comparar también datos de campo y rutas con CDN/Dispatcher si están disponibles. Cambios de caché, clientlibs, consultas o índices son experimentos separados, cada uno con su propio baseline y revisión de corrección. [Adobe: Web-Optimized Image Delivery](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/web-optimized-image-delivery) · [Adobe: caching](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching).

## Diagnóstico rápido

| Síntoma | Primera comprobación |
| --- | --- |
| Los valores de LCP cambian mucho entre corridas | Red/CPU de DevTools, caché, pestañas, versión de página y dispersión de las cinco muestras. |
| La imagen optimizada pesa lo mismo | Recurso realmente solicitado, asset publicado, caché, variante responsive y tamaño transferido. |
| La imagen ya no es LCP | Elemento LCP nuevo y su etapa dominante; no compares sólo la URL de la imagen. |
| Baja el peso, no el LCP | Espera de descubrimiento o render, clientlibs y tareas principales. |
| TTFB alto sólo a través de Dispatcher | Hit/miss, elegibilidad, red y origen; no atribuirlo directamente a una consulta. |
| Foto borrosa tras el cambio | Resolución servida frente a tamaño mostrado y densidad de pantalla; revisa el asset. |

## Repaso con respuestas

1. **¿Por qué cinco corridas?** Para ver variación y comparar una mediana bajo condiciones repetibles; una sola cifra puede engañar.
2. **¿TTFB alto demuestra una consulta lenta?** No. Incluye red y capas intermedias; correlaciona Publish y la consulta antes de intervenir.
3. **¿Menos bytes garantizan mejor LCP?** No. Comprueba el elemento LCP y las etapas de carga y render después del cambio.
4. **¿El SDK demuestra el resultado de Web-Optimized Image Delivery?** No. En local puede usar Adaptive Image Servlet; el servicio optimizado se verifica en AEM Cloud.
5. **¿Cuándo aceptas la corrección?** Cuando mediciones comparables cumplen el presupuesto acordado y la imagen conserva calidad y significado.

## Fuentes

- [Adobe · Core Image](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/wcm-components/image), [Adaptive Image Servlet](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/adaptive-image-servlet) y [Web-Optimized Image Delivery](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/web-optimized-image-delivery)
- [Adobe · Caching in AEM as a Cloud Service](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching) y [Dispatcher Configuration](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration)
- [Adobe · Client Libraries and Core Components](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/including-clientlibs) y [Troubleshooting Slow Queries](https://experienceleague.adobe.com/en/docs/experience-manager-65/content/implementing/developing/bestpractices/troubleshooting-slow-queries)
- [Chrome · Network features reference](https://developer.chrome.com/docs/devtools/network/reference/) y [Lighthouse](https://developer.chrome.com/docs/devtools/lighthouse/)
- [web.dev · Optimize Largest Contentful Paint](https://web.dev/articles/optimize-lcp)
