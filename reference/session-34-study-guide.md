# Sesión 34 · Separar navegador, CDN y Dispatcher

**Jueves 1 de octubre de 2026 · Semana 7 · Núcleo de 30 minutos, ampliable a 60**

[Versión HTML](session-34-study-guide.html) · [Slides en inglés](../lessons/0034-browser-cdn-dispatcher-cache.html#slide-deck) · [Caso guiado](#caso-guiado)

## Objetivo observable

Ante una traza suministrada donde Publish y Dispatcher sirven la versión nueva pero la respuesta pública es antigua, identificar **la primera capa que diverge**. Entregar Host, URL, marcador A/B, hora, headers y evidencia, distinguiendo observaciones locales de datos simulados. La sesión 33 cubrió Dispatcher. **Esta clase no requiere acceso a una CDN, logs Cloud ni una URL pública real.**

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–5 | 1–2 | Situar las tres decisiones de caché. |
| 5–13 | 3–5 | Leer headers y comprobar si el navegador hizo una petición. |
| 13–21 | 6–9 | Interpretar log de CDN, privacidad, query y clientlibs. |
| 21–28 | 10–11 | Resolver la traza B, B, A con evidencia. |
| 28–30 | 12 | Defender la capa responsable y cerrar. |

Para 60 minutos, añade 15 minutos de comparación en DevTools sobre el sitio local y 15 de discusión de variantes. La respuesta y el log de CDN son **evidencia didáctica suministrada**; la comprobación local sólo cubre navegador, Publish y Dispatcher Tools.

## 1. Un recorrido, tres decisiones

La respuesta puede salir de **navegador → CDN → Apache/Dispatcher → Publish**. Un hit temprano impide que la petición llegue a las capas siguientes. Mantén método GET, Host, path y query string constantes dentro de cada comparación local. Registra un marcador visible del cuerpo, por ejemplo `Version A` o `Version B`; un `200` por sí solo no indica frescura ni origen. Para la URL pública, **lee la respuesta suministrada** y sus coordenadas; no intentes consultar una CDN real. [Caché en AEM Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching).

| Capa | Prueba útil | Límite de la prueba |
| --- | --- | --- |
| Navegador | DevTools Network: memoria/disco frente a petición de red; respuesta y URL. | Un reload puede cambiar headers y comportamiento de caché. |
| CDN | Respuesta y log simulados del GET público: `rid`, `host`, `url`, `cache`, `res_age`, `pop`, status. | Permiten resolver el caso, no demuestran el estado de una CDN real. |
| Dispatcher | Log de decisión y ausencia/presencia de nueva GET en Publish. | Dispatcher Tools local no reproduce la CDN administrada. |
| Publish | Respuesta directa con marcador B. | Publish B no garantiza que las capas anteriores hayan vencido. |

Los logs de CDN de AEM registran `cache` como `HIT`, `MISS` o `PASS`, además de `res_age` y `pop`. En la traza suministrada, correlaciona **la petición concreta** por hora, Host, URL y `rid`; un HIT de otra URL o POP no explica esa respuesta. [Logging en AEM Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/logging).

## 2. Leer la política HTTP

`Cache-Control: max-age=300` permite que el navegador considere fresca la respuesta durante 300 segundos; también puede influir en cachés compartidas. `Surrogate-Control: max-age=3600` permite fijar una vigencia distinta para la **CDN administrada por Adobe**. Una CDN propia puede usar otras reglas. En AEM Cloud, la caché de Dispatcher sigue sus reglas de almacenamiento e invalidación; `/enableTTL` puede hacer que use headers de expiración. No conviertas un valor de `max-age` en prueba de que hubo un hit: comprueba la petición y los logs. Estos números son un **ejemplo didáctico**, no una recomendación universal. [Caché en AEM Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching) · [Configuración Dispatcher — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration).

Si la respuesta tiene `Age: 900`, ya superó los 300 segundos del navegador pero sigue dentro de los 3600 de CDN del ejemplo: una nueva GET puede obtener un `HIT` en CDN aunque la copia local haya vencido.

```http
Cache-Control: max-age=300
Surrogate-Control: max-age=3600
```

Captura también `Age`, `Set-Cookie`, status, fecha y marcador del cuerpo. `Age` ayuda a interpretar cuánto tiempo pasó una respuesta en cachés intermedias, pero no identifica por sí solo la capa ni sustituye el log. Evita `curl -I` como única prueba: en un miss, Adobe documenta que la CDN puede transformar `HEAD` en `GET` hacia origen. Usa una GET real cuando la duda sea el contenido visible. [HEAD en la CDN — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching#head-request-behavior).

## 3. Privacidad, parámetros y clientlibs

La CDN administrada no almacena respuestas con `Cache-Control: private`, `no-cache` o `no-store`, ni respuestas que incluyen `Set-Cookie`. **Comprueba Dispatcher por separado**: una respuesta privada para CDN todavía podría guardarse allí según su configuración. Las páginas con datos de un usuario requieren revisar las dos capas y la política del navegador. No añadas un header amplio para todas las páginas sin excluir rutas privadas. [Contenido privado — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching#html-text).

La clave de CDN considera la URL completa, incluida la query, aunque las transformaciones configuradas pueden eliminar parámetros de campañas comunes. Dispatcher usa `/ignoreUrlParams` con semántica propia. Por eso `?v=aleatorio` no es una prueba fiable de qué caché falló: puede crear otra entrada en CDN, ignorarse o impedir caché en Dispatcher. Diagnostica primero con la URL original y revisa las reglas efectivas. [Parámetros en CDN — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching#marketing-campaign-parameters) · [Parámetros en Dispatcher — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration#ignoring-url-parameters).

AEM Cloud activa el versionado estricto de clientlibs: cuando cambia CSS o JS, la URL lleva otro hash `lc-`. Si el navegador muestra estilos viejos, compara **primero el HTML**: ¿sigue apuntando al hash anterior? Si sí, busca HTML antiguo en navegador/CDN/Dispatcher. Si el HTML ya apunta al hash nuevo, comprueba la petición y respuesta de ese asset. No purgues clientlibs por intuición. [Versionado de clientlibs — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching#client-side-libraries-and-version-consistency).

## Caso guiado

**Traza didáctica simulada; no es una ejecución del repositorio ni un log Cloud real.** La misma página pública `/content/site/en/cache-lab.html` cambió de A a B y ya se publicó. La CDN administrada usa una política de una hora para este ejemplo.

| Hora | Límite | Evidencia suministrada |
| --- | --- | --- |
| 10:00 | Publish directo | `200`, cuerpo `Version B`. |
| 10:01 | Dispatcher local, Host del sitio | `200`, `Version B`; log local indica archivo actualizado. |
| 10:02 | Respuesta pública suministrada | `200`, `Version A`, `Cache-Control: max-age=300`, `Surrogate-Control: max-age=3600`. |
| 10:02 | Log CDN simulado de esa GET | `host=www.example.test`, `url=/content/site/en/cache-lab.html`, `cache=HIT`, `res_age=900`, `pop=MAD`. |
| 10:03 | Registro de navegador suministrado | `Version A`; Network indica respuesta de red, no memoria/disco. |

**Conclusión sustentada para este caso simulado:** Publish y Dispatcher sirven B; la respuesta pública suministrada es A y el log correspondiente indica `HIT`. La CDN es la primera capa divergente **en la traza**, no un hallazgo en un ambiente real. El navegador también muestra A, pero recibió esa versión por red. Propón revisar la vigencia y, si la actualización debe ser inmediata, el mecanismo de purga para esa URL; no ejecutes ninguna purga en esta práctica. [Purgar caché CDN — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/cdn-cache-purge).

**Variante A:** navegador A, respuesta pública suministrada B y Network marca memoria/disco → primera divergencia: navegador. **Variante B:** log CDN simulado `MISS`, respuesta pública A, Dispatcher B → faltaría comprobar Host, ruta y origen realmente usado; el `MISS` impide atribuir A a un hit de CDN. **Variante C:** Dispatcher A y Publish B → retoma el diagnóstico de la sesión 33.

## Comprobación guiada sin CDN

1. Si tienes Publish y Dispatcher Tools locales, solicita la página de prueba por ambos límites como en la sesión 33. Registra Host, URL, marcador A/B y decisión de caché de Dispatcher. No atribuyas esa observación a la CDN.
2. En el navegador local, abre DevTools → Network y comprueba memoria/disco frente a petición de red. Anota si usaste reload o desactivaste caché. Para comparar navegador y `curl`, ambos deben usar el **mismo Host y path**; si no coinciden, registra las pruebas por separado.
3. Lee la respuesta pública y el log CDN **suministrados en la tabla**, sin ejecutar `curl` contra un dominio público ni buscar logs Cloud. Correlaciona hora, Host, URL, `cache`, `res_age` y `pop` y determina la primera capa divergente de esa traza.
4. Resuelve las variantes A–C con la siguiente prueba que pedirías en un ambiente real. Declara qué parte se observó localmente y qué parte provino del caso simulado.

| Evidencia mínima | Registro |
| --- | --- |
| Observación local | GET, Host, URL, marcador A/B y decisión de Dispatcher o Network del navegador, si hay entorno. |
| Datos suministrados | Respuesta pública, headers y log CDN simulados; `cache`, `res_age`, `pop` y `rid` cuando aparezca. |
| Decisión | Primera capa divergente **del caso** y prueba que descarta las anteriores. |

## Repaso con respuestas

1. **¿`Surrogate-Control` y `Cache-Control` tienen que durar lo mismo?** No. En la CDN administrada por Adobe pueden fijar vigencias distintas para CDN y navegador.
2. **¿Un HTTP 200 con `Age` demuestra un hit de CDN?** No por sí solo. En el caso, correlaciona la respuesta con el campo `cache` del log suministrado.
3. **¿`private` protege también Dispatcher?** No necesariamente. Revisa su política de caché y autenticación por separado.
4. **¿Sirve añadir `?v=123` para ubicar la capa?** No de forma fiable. CDN y Dispatcher pueden tratar la query de modo distinto.
5. **¿Qué indica HTML antiguo que referencia un hash `lc-` anterior?** Primero se debe actualizar el HTML; el navegador puede estar descargando correctamente la clientlib que ese HTML pidió.

## Fuentes oficiales

- [Caché en AEM as a Cloud Service — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching)
- [Logging y campos de CDN — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/logging)
- [Configuración de Dispatcher — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration)
- [Purgar caché CDN — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/cdn-cache-purge)
