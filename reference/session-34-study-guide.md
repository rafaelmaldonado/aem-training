# Sesión 34 · Separar navegador, CDN y Dispatcher

**Jueves 1 de octubre de 2026 · Semana 7 · Núcleo de 30 minutos, ampliable a 60**

[Versión HTML](session-34-study-guide.html) · [Slides en inglés](../lessons/0034-browser-cdn-dispatcher-cache.html#slide-deck) · [Caso guiado](#caso-guiado)

## Objetivo observable

Ante contenido antiguo en la URL pública después de comprobar la versión nueva en Publish y Dispatcher, identificar **la primera capa que diverge**. Entregar la misma URL y Host, marcador A/B, hora, headers y evidencia del navegador o del log de CDN. La sesión 33 cubrió la caché de Dispatcher; aquí se comparan sus resultados con el navegador y la CDN. No se presupone acceso a Cloud Manager ni una CDN real en clase.

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–5 | 1–2 | Situar las tres decisiones de caché. |
| 5–13 | 3–5 | Leer headers y comprobar si el navegador hizo una petición. |
| 13–21 | 6–9 | Interpretar log de CDN, privacidad, query y clientlibs. |
| 21–28 | 10–11 | Resolver la traza B, B, A con evidencia. |
| 28–30 | 12 | Defender la capa responsable y cerrar. |

Para 60 minutos, añade 15 minutos de comparación en DevTools y 15 de discusión de variantes del caso. El material de CDN es **simulado**; la comprobación local sólo cubre navegador, Publish y Dispatcher Tools.

## 1. Un recorrido, tres decisiones

La respuesta puede salir de **navegador → CDN → Apache/Dispatcher → Publish**. Un hit temprano impide que la petición llegue a las capas siguientes. Mantén método GET, Host, path y query string constantes. Registra un marcador visible del cuerpo, por ejemplo `Version A` o `Version B`; un `200` por sí solo no indica frescura ni origen. Al comparar Publish directo con Dispatcher, respeta el Host que selecciona vhost y farm. Al comparar la URL pública, conserva el dominio público real. [Caché en AEM Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching).

| Capa | Prueba útil | Límite de la prueba |
| --- | --- | --- |
| Navegador | DevTools Network: memoria/disco frente a petición de red; respuesta y URL. | Un reload puede cambiar headers y comportamiento de caché. |
| CDN | Log del GET público: `rid`, `host`, `url`, `cache`, `res_age`, `pop`, status. | Una respuesta pública aislada no prueba `HIT`. |
| Dispatcher | Log de decisión y ausencia/presencia de nueva GET en Publish. | Dispatcher Tools local no reproduce la CDN administrada. |
| Publish | Respuesta directa con marcador B. | Publish B no garantiza que las capas anteriores hayan vencido. |

Los logs de CDN de AEM registran `cache` como `HIT`, `MISS` o `PASS`, además de `res_age` y `pop`. Correlaciona **la petición concreta** por hora, Host, URL y `rid`; un HIT de otra URL o POP no explica esta respuesta. [Logging en AEM Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/logging).

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
| 10:02 | GET a URL pública con `curl` | `200`, `Version A`, `Cache-Control: max-age=300`, `Surrogate-Control: max-age=3600`. |
| 10:02 | Log CDN de esa GET | `host=www.example.test`, `url=/content/site/en/cache-lab.html`, `cache=HIT`, `res_age=900`, `pop=MAD`. |
| 10:03 | Navegador normal | `Version A`; Network indica respuesta de red, no memoria/disco. |

**Conclusión sustentada:** Publish y Dispatcher ya sirven B; una GET pública independiente sigue recibiendo A y el log correspondiente indica `HIT`. La CDN es la primera capa divergente en esta traza. El navegador también muestra A, pero recibió esa versión por red. La acción siguiente es revisar la política de vigencia y el mecanismo de purga para **esa URL**, sin borrar toda la caché para esconder la causa. El purgado de CDN existe, pero requiere configuración y autorización operativa; no es parte de la demo local. [Purgar caché CDN — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/cdn-cache-purge).

**Variante A:** navegador A, GET pública fresca B y Network marca memoria/disco → primera divergencia: navegador. **Variante B:** CDN `MISS`, URL pública A, Dispatcher B → vuelve a comprobar Host, ruta y origen realmente usado; el `MISS` impide atribuir el A a un hit de CDN. **Variante C:** Dispatcher A y Publish B → retoma el diagnóstico de la sesión 33.

## Comprobación guiada si hay entorno

1. En el navegador abre DevTools → Network, conserva la URL exacta y registra si hubo petición de red, status, marcador, `Cache-Control`, `Surrogate-Control` y `Age` si aparecen. Anota si usaste reload o desactivaste caché en DevTools.
2. Desde una terminal nueva, solicita la **URL pública con GET**, sin cookies ni query añadida: `curl -i 'https://www.example.test/content/site/en/cache-lab.html'`. Reemplaza dominio y path por los reales; no ejecutes literalmente el dominio de ejemplo.
3. Si tienes acceso autorizado a logs Cloud, busca esa petición por hora, Host, URL y `rid`. Lee `cache`, `res_age` y `pop`. Sin ese acceso, usa la traza simulada y declara la conclusión como análisis del caso, no observación real.
4. Compara con Publish y Dispatcher local siguiendo las sesiones 31–33. Registra la **primera respuesta distinta**, no sólo la última pantalla que parece antigua.

| Evidencia mínima | Registro |
| --- | --- |
| Petición | GET, Host, URL completa, hora, entorno y cookies presentes o ausentes. |
| Contenido | Marcador A/B en Publish, Dispatcher y URL pública. |
| Política | `Cache-Control`, `Surrogate-Control`, `Age` y `Set-Cookie` si aparece. |
| CDN/navegador | `cache`/`res_age`/`pop`/`rid` o indicación de memoria/disco/red en Network. |
| Decisión | Primera capa divergente y prueba que descarta las anteriores. |

## Repaso con respuestas

1. **¿`Surrogate-Control` y `Cache-Control` tienen que durar lo mismo?** No. En la CDN administrada por Adobe pueden fijar vigencias distintas para CDN y navegador.
2. **¿Un HTTP 200 con `Age` demuestra un hit de CDN?** No por sí solo. Correlaciona la GET con el campo `cache` del log CDN.
3. **¿`private` protege también Dispatcher?** No necesariamente. Revisa su política de caché y autenticación por separado.
4. **¿Sirve añadir `?v=123` para ubicar la capa?** No de forma fiable. CDN y Dispatcher pueden tratar la query de modo distinto.
5. **¿Qué indica HTML antiguo que referencia un hash `lc-` anterior?** Primero se debe actualizar el HTML; el navegador puede estar descargando correctamente la clientlib que ese HTML pidió.

## Fuentes oficiales

- [Caché en AEM as a Cloud Service — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching)
- [Logging y campos de CDN — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/logging)
- [Configuración de Dispatcher — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration)
- [Purgar caché CDN — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/cdn-cache-purge)
