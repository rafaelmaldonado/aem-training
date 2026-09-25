# Sesión 32 · Seguir una petición por Apache y Dispatcher

**Martes 29 de septiembre de 2026 · Semana 7 · Núcleo de 30 minutos, ampliable a 60**

[Versión HTML](session-32-study-guide.html) · [Slides en inglés](../lessons/0032-apache-dispatcher-request.html#slide-deck) · [Demo local](#demo-local)

## Objetivo observable

Ante una URL pública que devuelve 403, 404 o una redirección inesperada mientras el contenido correcto ya existe en Publish, identificar **la primera capa que cambió la petición o respondió**. El participante entrega Host, URL, código, `Location` si existe, path resuelto y la línea de log que sostiene su conclusión.

La sesión 31 terminó al comprobar Publish. Aquí seguimos **una sola petición HTTP** por CDN, Apache, Dispatcher y Publish. La caché y su invalidación se estudian en la sesión 33. La práctica local usa Dispatcher Tools y el Publish del SDK; no afirma reproducir el CDN administrado de Cloud. [Flujo de entrega — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/overview) · [Dispatcher Tools — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/dispatcher-tools).

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–4 | 1–2 | Fijar Host, URL y respuesta observada; dibujar la ruta. |
| 4–11 | 3–4 | Encontrar vhost y farm aplicables. |
| 11–18 | 5–7 | Distinguir rewrite, redirect, filtro y headers. |
| 18–27 | 8–10 | Comparar 403/404 con logs y ejecutar la prueba local. |
| 27–30 | 11–12 | Nombrar la primera divergencia y cerrar. |

Para 60 minutos, añade 20 de ejecución local y 10 de discusión de las tres respuestas del caso. El instructor prepara de antemano Publish local, el proyecto y Dispatcher Tools; cada participante puede analizar el registro sin acceso a Cloud Manager.

## 1. Ruta y evidencia de una petición

```text
Navegador → CDN → Apache (vhost y rewrites) → Dispatcher (farm y filtro) → Publish
```

Registra la URL exacta, método, Host, hora, status y headers relevantes antes de seguir redirecciones. No uses `curl -L` en la primera observación: ocultaría la respuesta 3xx inicial. El CDN puede transformar o responder una petición antes de que llegue a Apache; si no hay entrada en el access log de Apache, esa ausencia sólo sirve como indicio tras correlacionar hora, Host y entorno. [Tráfico en CDN — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/cdn-configuring-traffic) · [Logs Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/logging).

En Apache, `ServerName` y `ServerAlias` participan en la elección del virtual host. Revisa el archivo habilitado y los includes de rewrites para el Host concreto. Después, Dispatcher selecciona una farm con sus `/virtualhosts`; esa farm aporta `/filter`, `/renders` y otras reglas. Un Host diferente puede llevar a otro vhost o farm aunque el path sea idéntico. [Configuración de Dispatcher — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration) · [Validación de configuración Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/validation-debug).

## 2. Rewrite, redirect, filtros y headers

| Mecanismo | Señal observable | Comprobación |
| --- | --- | --- |
| Rewrite interno de Apache | La URL del navegador permanece; Apache cambia el path que procesa internamente. | Compara URI original, regla aplicada y path que llega a Dispatcher/Publish. |
| Redirect externo | Respuesta 3xx con `Location`; el navegador hace otra petición. | Inspecciona status y `Location` sin seguir automáticamente la redirección. |
| Filtro de Dispatcher | Una regla `/filter` permite o rechaza una petición antes del renderer. Un rechazo devuelve normalmente 404. | Busca la decisión y la regla en el log de Dispatcher; verifica si Publish recibió la petición. |
| Header de petición | `Host` afecta selección; `/clientheaders` controla qué headers del cliente llegan al renderer. | Compara los headers de entrada con la configuración y la evidencia en destino. |

`RewriteRule` con flag `[R]` genera una redirección externa; una sustitución interna no equivale a un 3xx. Para un redirect simple, Apache también ofrece `Redirect` y `RedirectMatch`. En Cloud un redirect puede ocurrir además en el CDN, por lo que primero hay que ubicar la capa que emitió la respuesta. [mod_rewrite — Apache](https://httpd.apache.org/docs/2.4/mod/mod_rewrite.html) · [Flags — Apache](https://httpd.apache.org/docs/2.4/rewrite/flags.html) · [Tráfico en CDN — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/cdn-configuring-traffic).

La configuración de `/filter` puede usar método, URL, query, path, selectors, extensión y suffix. Mantén la política de denegar por defecto y permitir sólo lo necesario. Adobe documenta que una petición rechazada por ese filtro se devuelve al servidor web con 404. Un **403 observado no demuestra** una denegación del filtro de Dispatcher; revisa Apache, CDN, Publish y otras reglas con logs. Un **404 tampoco demuestra** que falte contenido en Publish. [Filtro y códigos — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration#configuring-access-to-content-filter).

`/clientheaders` define los headers de la petición que Dispatcher pasa al renderer. Los headers de respuesta, como `Location` o `Cache-Control`, requieren una inspección distinta; Apache y el CDN también pueden transformarlos. No deduzcas el comportamiento de caché sólo a partir de esta clase. [Headers en Dispatcher — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration#specifying-the-http-headers-to-pass-through-clientheaders) · [Tráfico en CDN — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/cdn-configuring-traffic).

## 3. Caso guiado: tres respuestas

**Evidencia didáctica simulada, no una ejecución registrada en este repositorio.** El contenido de `/content/site/en/adventures.html` está comprobado en Publish. Se prueban tres peticiones con el mismo Host de ejemplo, `www.example.test`:

| Observación suministrada | Primera lectura | Prueba siguiente |
| --- | --- | --- |
| `/old` devuelve `302` y `Location: /new`; no aparece petición a Publish para `/old`. | Una capa anterior a Publish respondió con redirect. | Correlaciona log de Apache o CDN y regla; inspecciona `/new` por separado. |
| `/content/site/en/adventures.html` devuelve `404`; Dispatcher registra rechazo de `/filter`; Publish no recibe la petición. | El primer corte está en la farm/filtro seleccionado. | Identifica Host, farm y regla exacta. No abras el filtro globalmente. |
| `/adventures` devuelve `404`; Dispatcher reescribe y envía un path a Publish; Publish registra 404 para ese path. | El corte está en el path resuelto o en el recurso de destino. | Compara la regla de rewrite con el path publicado real. |

**Pregunta al grupo:** ¿puedes diagnosticar cualquiera de los tres sólo por status? **Respuesta:** no. El status junto con `Location`, la presencia en access logs y la línea de Dispatcher/Publish identifica el primer tramo que cambió la respuesta. Un 403 se investiga del mismo modo, sin asignarlo automáticamente a ACL ni a filtro. [Logging — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/logging) · [Validación y debugging — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/validation-debug).

## Demo local

**Preparación:** Docker, Publish del SDK en `localhost:4503`, proyecto instalado en Publish y Dispatcher Tools del SDK. Usa el Host que realmente figure en `dispatcher/src/conf.d/available_vhosts` y una página de prueba publicada. El comando se ejecuta desde la carpeta extraída de Dispatcher Tools. En macOS/Linux Adobe documenta `docker_run_hot_reload.sh` para recargar cambios de configuración; en Windows se usa `bin\docker_run`. [Preparar Dispatcher Tools — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/dispatcher-tools).

```sh
./bin/docker_run_hot_reload.sh /ruta/al/proyecto/dispatcher/src host.docker.internal:4503 8080
```

En otra terminal, sustituye Host y path por valores de tu proyecto. La primera petición preserva la respuesta original; la segunda contrasta directamente con Publish.

```sh
curl -i -H 'Host: www.example.test' 'http://localhost:8080/content/site/en/adventures.html'
curl -i 'http://localhost:4503/content/site/en/adventures.html'
```

1. Registra status, `Location` si aparece y el path solicitado en ambas respuestas. Si se produce 3xx, haz una petición **nueva** al destino después de documentar la primera.
2. Repite con el Host de tu proyecto y con un Host distinto. Observa qué vhost y farm se eligen; no supongas que el Host ficticio del ejemplo coincide con tu configuración.
3. Revisa el `stdout` de Dispatcher Tools y, si necesitas más detalle, arráncalo con `DISP_LOG_LEVEL=Debug REWRITE_LOG_LEVEL=Debug` antes del comando. Busca el request, farm, rewrite o rechazo; correlaciona con access y request logs de Publish.
4. Cambia **una sola regla en una copia local** de la configuración, deja que hot reload la valide y repite exactamente la misma petición. Guarda antes/después. No despliegues la regla de ejercicio.

| Evidencia mínima | Registro esperado |
| --- | --- |
| Entrada | Hora, método, Host y URL exactos. |
| Respuesta | Status y `Location` si existe; no seguirla en la primera captura. |
| Apache/Dispatcher | Vhost/farm y línea de rewrite o filtro, si aplica. |
| Publish | Si llegó la petición, path y status de destino. |
| Conclusión | Primera capa con una decisión distinta y evidencia citada. |

**Resultado esperado, no ejecución registrada.** El ejercicio separa una decisión de Apache/Dispatcher de una respuesta generada por Publish. Las herramientas locales no reproducen por completo la capa CDN de Cloud. [Dispatcher Tools y logs — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/dispatcher-tools) · [Logging — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/logging).

## Decisión al cierre

| Primera evidencia diferente | Continúa en |
| --- | --- |
| CDN responde y Apache no recibe la petición | Reglas y logs de CDN para ese Host y hora. |
| Apache recibe Host incorrecto o emite 3xx | Vhost, alias e include de redirects/rewrites. |
| Dispatcher selecciona otra farm o rechaza | `/virtualhosts`, `/filter` y log de Dispatcher. |
| Publish recibe path distinto o responde 403/404 | Rewrite efectivo, path del recurso y logs de Publish. |
| Publish sirve bien y hay respuesta vieja en URL pública | Sesión 33: caché Dispatcher e invalidación. |

## Repaso con respuestas

1. **¿Cómo distingues un rewrite interno de un redirect?** El redirect devuelve 3xx y `Location`; el rewrite cambia el path dentro del servidor y conserva la URL del navegador.
2. **¿Por qué registrar el Host?** Ayuda a elegir vhost y farm; el mismo path con otro Host puede tomar otra configuración.
3. **¿Qué devuelve normalmente un rechazo de `/filter`?** 404 según la documentación de Dispatcher; el log confirma la regla.
4. **¿Un 403 prueba un problema de ACL?** No. Hay que identificar qué capa respondió y con qué evidencia.
5. **¿Para qué sirve `/clientheaders`?** Para definir qué headers de petición del cliente pasan desde Dispatcher al renderer.
6. **¿Qué estudiar después de demostrar que Publish y el path son correctos, pero la respuesta pública es vieja?** Caché e invalidación en la sesión 33.

## Fuentes oficiales

- [Dispatcher en Cloud y herramientas locales — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/disp-overview)
- [Configurar Dispatcher, farm, filtros y headers — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration)
- [Validar y depurar Apache/Dispatcher — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/validation-debug)
- [Dispatcher Tools locales — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/dispatcher-tools)
- [Logs en AEM Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/logging)
- [mod_rewrite y flags — Apache](https://httpd.apache.org/docs/2.4/mod/mod_rewrite.html)
