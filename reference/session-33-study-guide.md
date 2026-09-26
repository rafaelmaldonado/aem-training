# Sesión 33 · Diagnosticar la caché de Dispatcher

**Miércoles 30 de septiembre de 2026 · Semana 7 · Núcleo de 30 minutos, ampliable a 60**

[Versión HTML](session-33-study-guide.html) · [Slides en inglés](../lessons/0033-dispatcher-cache.html#slide-deck) · [Demo local](#demo-local)

## Objetivo observable

Ante una página correcta en Publish pero antigua a través de Dispatcher, demostrar con **la misma petición** un miss, un hit y una respuesta actualizada después de publicar un cambio controlado. El participante entrega Host, URL, versión visible, respuesta y líneas de log o archivos de caché que sustentan cada paso.

La sesión 32 ubicó la ruta de la petición. Aquí se aísla la caché de Dispatcher local. La sesión 34 separará navegador y CDN. Los comandos locales no prueban el comportamiento del CDN administrado. [Caché en AEM Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching) · [Configurar Dispatcher — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration).

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–4 | 1–2 | Comparar una URL en Publish y Dispatcher. |
| 4–11 | 3–5 | Decidir si la respuesta entra en caché y cómo probar hit/miss. |
| 11–18 | 6–9 | Explicar `.stat`, invalidación, TTL y parámetros de URL. |
| 18–27 | 10–11 | Ejecutar o analizar la secuencia A, A, B, B. |
| 27–30 | 12 | Defender la causa con evidencia y cerrar. |

Para 60 minutos, añade 20 de ejecución local y 10 de discusión de resultados divergentes. Prepara Author, Publish, Docker y Dispatcher Tools antes de clase. Si el grupo no tiene entorno local, usa la traza didáctica suministrada abajo y pide la siguiente prueba, sin presentarla como una ejecución real.

## 1. La misma petición en dos límites

Comprueba primero la versión en Publish, como en la sesión 31. Después usa **el mismo método GET, Host y path** por Dispatcher. No cambies query string ni añadas un parámetro de “cache busting” entre peticiones: `/ignoreUrlParams` puede hacer que el parámetro se ignore o que la respuesta deje de ser cacheable. Para una comparación fiable, captura hora, status y un marcador visible dentro del HTML, además del log de Dispatcher y el request log de Publish. Dos respuestas HTTP 200 iguales no prueban un hit; la ausencia de una nueva petición a Publish, correlacionada con una línea de caché en Dispatcher, sí lo sostiene. [Reglas y parámetros — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration#specifying-the-documents-to-cache) · [Logging — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/logging).

## 2. Qué puede entrar y qué puede quedar obsoleto

| Ajuste | Pregunta que responde | Evidencia |
| --- | --- | --- |
| `/cache/rules` | ¿El path del documento puede almacenarse? | Regla efectiva y archivo bajo `/docroot`. |
| `/cache/invalidate` | ¿Qué archivos guardados se marcan obsoletos tras actualizar contenido? | Regla, petición de invalidación y tiempos `.stat`/archivo. |
| `/statfileslevel` | ¿Hasta qué nivel de la ruta se crean y tocan `.stat`? | Nivel configurado y timestamps del árbol local. |
| `/enableTTL` | ¿Expira el archivo por headers de tiempo? | Configuración, `Cache-Control`/`Expires`, archivo `.ttl` y nueva petición a Publish. |
| `/ignoreUrlParams` | ¿Los parámetros permiten reutilizar la misma respuesta? | Reglas de nombres de parámetros y respuesta para valores distintos. |

`/filter` permite o rechaza la petición; **no decide por sí mismo** si se guarda la respuesta. Dispatcher documenta otras condiciones además de `/cache/rules`, entre ellas método GET/HEAD, extensión, autenticación, query string y headers de respuesta. En una página de laboratorio usa GET y una URL `.html` pública. Por defecto, las peticiones con `Authorization`, cookie `authorization` o `login-token` no se cachean cuando `/allowAuthorized` permanece en `0`. No cambies ese ajuste para hacer pasar el ejercicio. [Condiciones de caché — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration#specifying-the-documents-to-cache) · [Autenticación — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration#caching-when-authentication-is-used).

La invalidación normal elimina directamente el archivo actualizado y marca otros documentos elegibles como obsoletos mediante `.stat`; éstos pueden seguir en disco hasta la siguiente solicitud. Dispatcher compara el tiempo del archivo cacheado con el `.stat` pertinente y vuelve a consultar Publish si el archivo es anterior. `/statfileslevel` limita el alcance en el árbol; un nivel demasiado general invalida más páginas de las necesarias. El nivel no se elige por intuición: comprueba el path de contenido y el docroot de la farm. [Invalidación y stat files — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration#invalidating-files-by-folder-level) · [Invalidación en Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching#dispatcher-cache-invalidation).

Con `/enableTTL "1"`, Dispatcher usa los headers de expiración que recibe del backend para decidir cuándo volver a solicitar un archivo. En versiones actuales, una invalidación estándar también puede actualizarlo **antes** de que venza el TTL. El TTL de Dispatcher no establece por sí solo la política del navegador o CDN; sus headers se tratan en la sesión 34. No asumas que `Cache-Control: max-age` es una prueba de hit. [TTL — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration#configuring-time-based-cache-invalidation-enablettl) · [Caché Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching).

`/ignoreUrlParams` tiene una semántica fácil de invertir: `allow` significa **ignorar** ese parámetro al decidir la caché; `deny` significa **no ignorarlo**, por lo que la petición con ese parámetro no se cachea en Dispatcher. Si todos los parámetros se ignoran, valores distintos pueden recibir el mismo archivo. Sólo ignora parámetros que no cambien el contenido, por ejemplo uno de medición; un parámetro de búsqueda o variante que cambie HTML requiere una política distinta. El CDN puede usar otra clave de caché, incluida la query completa. [Parámetros — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration#ignoring-url-parameters) · [Clave CDN — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching).

## 3. Caso guiado: A, A, B, B

**Traza didáctica simulada, no ejecución registrada en este repositorio.** Una página pública de prueba `/content/site/en/cache-lab.html` contiene el texto `Version A`. La farm permite almacenarla; la ruta de invalidación y el flush están configurados para ella.

| Paso | Publish directo | Dispatcher | Prueba que debes buscar |
| --- | --- | --- | --- |
| 1. Primera GET a Dispatcher | A | A | Dispatcher solicita Publish y crea el archivo de caché: miss. |
| 2. Misma GET | A | A | Dispatcher sirve el archivo; Publish no registra una nueva GET: hit. |
| 3. Cambiar A por B y publicar | B | A antes de la siguiente GET | Publish recibe B; llega invalidación y cambia `.stat` o se elimina el archivo del path. |
| 4. Misma GET tras publicar | B | B | Dispatcher vuelve a Publish: refresh/miss. |
| 5. Misma GET de nuevo | B | B | El archivo actualizado se sirve sin una nueva GET a Publish: hit. |

Si el paso 4 conserva A, no borres toda la caché. Revisa primero que Publish tenga B, que el Host elija la farm esperada, que el flush llegue al Dispatcher correcto, que el path de invalidación corresponda al archivo cacheado y que el archivo sea elegible por `/invalidate`. Si la página incluye un fragmento o asset actualizado, publicar sólo la dependencia no demuestra que se invalidó el HTML que la consume. [Invalidación Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching#dispatcher-cache-invalidation) · [Configurar Dispatcher — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration).

## Demo local

**Preparación:** Docker, Author `localhost:4502`, Publish `localhost:4503`, proyecto instalado en ambos y Dispatcher Tools del SDK. Usa el Host real de `dispatcher/src/conf.d/available_vhosts`, la farm que le corresponde y una página de prueba pública `.html`. El comando se ejecuta desde la carpeta extraída de Dispatcher Tools en macOS/Linux; en Windows usa la ruta documentada en la [guía local](windows-publish-dispatcher-sdk.html). [Dispatcher Tools — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/dispatcher-tools).

```sh
DISP_LOG_LEVEL=Debug ./bin/docker_run_hot_reload.sh /ruta/al/proyecto/dispatcher/src host.docker.internal:4503 8080
```

Reemplaza el Host y path ficticios. Una URL que aún no se solicitó a este Dispatcher hace más clara la primera observación. Mantén exactamente la misma URL para las repeticiones. `curl -i` permite ver headers y marcador del cuerpo; inspecciona también el log y el docroot de la farm.

```sh
curl -i 'http://localhost:4503/content/site/en/cache-lab.html'
curl -i -H 'Host: www.example.test' 'http://localhost:8080/content/site/en/cache-lab.html'
curl -i -H 'Host: www.example.test' 'http://localhost:8080/content/site/en/cache-lab.html'
```

1. Registra el marcador A, hora, status, URL, Host y las líneas de Dispatcher/Publish de cada GET. Si la primera ya es hit, usa otra página de prueba o identifica la entrada local existente; no atribuyas un miss a la primera petición por orden solamente.
2. En Author cambia el marcador a B, publica **la misma página** y comprueba B directamente en Publish. Registra hora, path y evidencia de publicación.
3. Busca la petición de invalidación/flush y la modificación de `.stat` o eliminación del archivo pertinente. Repite dos GET idénticas por Dispatcher. Documenta si la primera vuelve a Publish y la segunda se sirve de caché.
4. Si no se actualiza, conserva la evidencia y diagnostica la farm, `/cache/rules`, `/invalidate`, `/statfileslevel`, mapeo URL/path y conexión de flush. Cambia una sola condición en la copia local si se necesita probar una hipótesis; no limpies globalmente la caché para ocultar la causa.

| Evidencia mínima | Registro |
| --- | --- |
| Entrada | Método GET, Host, path, hora y ausencia de cambios en query string. |
| Contenido | Marcador A o B en Publish y Dispatcher. |
| Caché | Regla, archivo y/o línea de hit, miss o refresh; presencia de GET en Publish. |
| Invalidación | Path publicado, flush y timestamp `.stat` o archivo eliminado. |
| Conclusión | Paso exacto que dejó de coincidir y regla o capa responsable. |

**Resultados esperados, no ejecución registrada.** La secuencia depende de la configuración real de la farm y del flush local; una observación distinta es material para el diagnóstico. Dispatcher Tools locales no reproducen el CDN de Cloud. [Dispatcher Tools — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/dispatcher-tools) · [Caché Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching).

## Decisión al cierre

| Primera evidencia diferente | Continuación |
| --- | --- |
| Publish aún muestra A | Sesión 31: estado de publicación, path y dependencias. |
| Publish muestra B; Dispatcher no guardó A en el paso 2 | Elegibilidad: `/cache/rules`, método, extensión, query, auth y headers. |
| Publish muestra B; Dispatcher sigue sirviendo A tras publicar | Flush, Host/farm, path, `/invalidate`, `.stat`, TTL y logs. |
| Dispatcher sirve B; la URL pública externa muestra A | Sesión 34: navegador y CDN, con evidencia de esas capas. |

## Repaso con respuestas

1. **¿Qué distingue `/cache/rules` de `/invalidate`?** La primera decide qué entra en caché; la segunda qué archivos cacheados quedan obsoletos al actualizar contenido.
2. **¿Un segundo HTTP 200 demuestra un hit?** No. Necesitas la decisión de Dispatcher y comprobar que Publish no recibió otra petición equivalente.
3. **¿Qué hace `.stat`?** Marca con su timestamp una región de caché como obsoleta; Dispatcher compara ese tiempo con el archivo guardado.
4. **¿TTL impide una invalidación anticipada?** No en las versiones actuales documentadas: la invalidación estándar puede refrescar antes del vencimiento.
5. **¿Qué significa `allow` en `/ignoreUrlParams`?** Que ese parámetro se ignora para decidir la caché. Si cambia el HTML, ignorarlo puede devolver la variante equivocada.
6. **¿Borrar toda la caché prueba la causa?** No. Puede quitar el síntoma sin explicar la regla, el flush o el path incorrectos.

## Fuentes oficiales

- [Configuración de caché, invalidación, stat files, TTL y parámetros — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration)
- [Caché e invalidación en AEM as a Cloud Service — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/caching)
- [Preparar Dispatcher Tools locales — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/dispatcher-tools)
- [Validar y depurar configuración — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/validation-debug)
