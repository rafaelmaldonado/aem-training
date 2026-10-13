# Sesión 42 · Consumir un servicio externo desde AEM

**Martes 13 de octubre de 2026 · Semana 9 · 30 minutos**

[Versión HTML](session-42-study-guide.html) · [Slides en inglés](../lessons/0042-external-http-integration.html#slide-deck) · [Demo local y código](examples/session-42/README.md)

## Objetivo observable

En Author SDK local, ejecutar una llamada HTTP saliente desde un servicio OSGi a un stub en loopback. Diferenciar una respuesta `200`, una credencial incorrecta (`401`), un fallo temporal (`503`) y una respuesta que supera el timeout de lectura. Explicar el contrato HTTP, la espera durante el render, un presupuesto finito de reintentos y la incertidumbre de una escritura remota cuando se pierde su respuesta. Relacionar cada concepto con los límites de la sonda local.

La sesión 41 enseñó cómo una cola vuelve a entregar trabajo. Ahora se delimita **una llamada externa**: destino configurado, secreto separado del código, timeouts, resultado clasificado y diagnóstico. El Process Step de la demo realiza un intento por instancia; no incluye una cola ni un reintento automático.

## Ejemplos habituales de integración HTTP

Estos contratos son **ilustrativos**: las rutas concretas dependen del proveedor. Un servicio OSGi propio tiene sentido cuando hace falta adaptar un contrato específico; antes conviene revisar las integraciones que AEM ya ofrece.

| Necesidad | Llamada posible | Decisión principal | Opción de AEM que revisar |
| --- | --- | --- | --- |
| Disponibilidad o precio de producto | Consultar el sistema de comercio con `GET` | Frescura, caché y coste de esperar durante el render. | [Commerce Integration Framework](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/content-and-commerce/cif-storefront/storefront/getting-started). |
| Enviar un lead a CRM | Enviar el formulario con `POST` | Credencial del servidor, identidad de operación y duplicados. | [Submit to REST endpoint de AEM Forms](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/forms/integrate/set-submit-action/configure-environment-specific-rest-endpoints). |
| Solicitar una traducción | Enviar un trabajo y consultar su resultado | Trabajo de fondo, demora y estado del proveedor. | [Translation Integration Framework y sus conectores](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/translation/sites/configure-connector). |

La sonda de esta sesión es más pequeña: un workflow manual llama a un stub local con `GET /ok` y clasifica el status. No implementa ninguno de los tres proveedores anteriores.

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–4 | 1–2 | Ejemplos comunes y elección de integración. |
| 4–8 | 3–4 | Contrato HTTP, servicio OSGi y credenciales. |
| 8–12 | 5 | Latencia en el render y significado de los timeouts. |
| 12–18 | 6–7 | Resultados observados, presupuesto de reintentos e idempotencia remota. |
| 18–24 | 8; volver a 6 | Leer el cliente Java y ejecutar los cuatro casos locales. |
| 24–28 | 9–10 | Egress Cloud y puntos clave. |
| 28–30 | 11 | Preguntas. |

## Contrato HTTP y responsabilidades OSGi

Un contrato HTTP define método, destino, headers, cuerpo cuando corresponda y respuesta esperada. Si una página necesita datos JSON, recibir 200 sólo confirma ese resultado HTTP: todavía hay que validar formato, tamaño, estructura y campos. Nuestra demo es una sonda de estado; no interpreta datos de Guides.

El workflow recibe el servicio mediante @Reference. @Designate define su configuración y @Activate la valida. check() hace la llamada y devuelve un enum propio. OK, RETRY y STOP no son JobResult de Sling: devolver RETRY no encola nada. Registrar una clase como servicio OSGi tampoco crea un hilo ni vuelve asíncrona una llamada Java.

## Latencia y frescura del contenido

Si un Sling Model llama sincrónicamente al proveedor, el render y su hilo esperan. Ejemplo ilustrativo: 150 ms de trabajo local más 2 s de espera externa suman unos 2,15 s, antes de otros costes de entrega. No es una medición de AEM ni implica que toda consulta síncrona esté prohibida.

Si el dato tolera cierta antigüedad, un job puede obtenerlo y persistirlo para que el render lea el resultado. Esa decisión exige definir cuánto puede envejecer, qué mostrar si falla la actualización y qué hacer cuando todavía no existe un resultado. El workflow manual de la demo permite estudiar HTTP fuera del render.

## 1. Una llamada externa tiene un límite claro

Una petición de página no debe quedar a la espera de trabajo largo o inestable del proveedor. Para la demo, **un workflow manual** invoca un servicio OSGi; el servicio conoce la URL fija configurada y hace un solo GET. No expone un servlet ni acepta URLs desde contenido o parámetros de usuario. En una integración real con trabajo largo, un Sling Job reanudable puede iniciar el servicio, como se explicó en la sesión 41. [Guías de desarrollo AEM Cloud](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/development-guidelines#background-tasks-and-long-running-jobs).

El cliente usa `HttpURLConnection`, que Adobe reconoce como opción disponible en AEM; Adobe recomienda HttpComponents 4.x para conexiones HTTP en sus guías generales. La API elegida aquí mantiene la demo pequeña y usa los timeouts y el proxy estándar del JDK. Antes de trasladar la demo a una integración real, comprueba la política HTTP y la biblioteca ya usada por tu proyecto. [HTTP saliente en AEM Cloud](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/development-guidelines#outgoing-http-connections).

## 2. Dos timeouts, dos preguntas

- **Conexión (`1000 ms` en la demo):** limita el establecimiento de conexión. No debe suponerse que este ajuste también acota la resolución DNS ni todo el intercambio.
- **Lectura (`2000 ms`):** limita una lectura bloqueada mientras espera datos disponibles. No es un deadline total; varias lecturas pueden prolongar la operación. `/slow` demora 3 segundos antes de responder y produce el timeout de lectura de la demo. [Semántica de URLConnection, Oracle](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/net/URLConnection.html).

Adobe recomienda establecer ambos; sus valores orientativos de 1 y 5 segundos deben ajustarse al proveedor. El `2 s` de lectura de esta demo es sólo para hacer visible el timeout en clase. Un timeout no prueba por sí solo que el proveedor no procesó la solicitud; para operaciones con efecto hay que diseñar idempotencia antes de repetirlas. [Adobe, outgoing HTTP connections](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/development-guidelines#outgoing-http-connections).

## 3. Clasificar antes de reintentar

La tabla describe el contrato simplificado del ejemplo. En una integración real, revisa el significado del fallo y el contrato del proveedor; no todos los 5xx ni todos los errores de transporte mejoran al repetirse.

| Observación | Clasificación didáctica | Acción antes de un nuevo intento |
| --- | --- | --- |
| `200` | `OK` | Confirmar que el resultado requerido llegó; este ejemplo sólo revisa el código. |
| `401` o `403` | `STOP` | Revisar clave, permisos y configuración; repetir la misma credencial no lo arregla. |
| `429`, `5xx` | `RETRY` | Respetar `Retry-After` si aplica, fijar máximo de intentos y presupuesto de tiempo. |
| Timeout o fallo de transporte | `RETRY` | Verificar conectividad y estado remoto antes de repetir una operación con efecto. |
| Otro estado, incluido `3xx` | `STOP` | Investigar contrato o URL; el cliente no sigue redirecciones. |

`RETRY` es una **decisión de clasificación**, no una orden de repetición infinita. El Process Step registra `RETRY` y falla para que el instructor inspeccione el caso. En producción, un llamador puede limitar intentos y espaciar reentregas; si usa Sling Jobs, la cola decide su política. Para operaciones no idempotentes, la clave de negocio y el estado persistido siguen siendo necesarios. [AEM Cloud, background tasks](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/development-guidelines#background-tasks-and-long-running-jobs).

## Presupuesto de reintentos y efecto remoto

Ejemplo de diseño, no código implementado: un máximo de tres intentos totales, cada uno con un deadline real de 2 s, y esperas de 1 y 2 s producen 3 × 2 + 1 + 2 = 9 s nominales. Un deadline global de 10 s debe cancelar o impedir trabajo que ya no cabe. Los dos timeouts de HttpURLConnection no implementan esos deadlines.

Backoff significa espaciar cada intento; jitter añade variación para que muchos clientes no vuelvan al mismo tiempo. Si Retry-After pide una espera que supera el presupuesto, difiere el trabajo o termina; no adelantes el intento. Elige un único dueño de la política: tres entregas de un job con tres intentos HTTP cada una pueden generar nueve llamadas.

Una escritura puede terminar en el proveedor y perder su respuesta. Si AEM sólo observa un timeout, repetir un POST podría duplicar el efecto. Una clave de operación ayuda únicamente si el proveedor ofrece y aplica ese contrato de deduplicación. La marca local de la sesión 41 no forma una transacción con el sistema remoto.

## Leer el ejemplo sin atribuirle funciones que no tiene

ExternalStatusService configura conexión y lectura antes de getResponseCode(), añade X-API-Key y desactiva redirecciones. En finally desconecta. ProbeExternalStatusProcess registra el ID del workflow y lanza WorkflowException si el resultado no es OK.

La clasificación del ejemplo agrupa 5xx y los IOException como RETRY para enseñar la decisión. No prueba que el fallo sea transitorio: un 501, un certificado inválido o un host mal configurado pueden necesitar corrección. El cliente no incluye parsing de cuerpo, límite total de duración, Retry-After, backoff ni repetición automática. Si se amplía para leer datos, hay que validar el contrato, limitar el cuerpo y cerrar los streams.

Fuentes de estas decisiones: [AWS Builders’ Library, backoff y jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) y [RFC 9110, idempotencia HTTP](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2).

## 4. Destino y credenciales

El destino remoto debe usar HTTPS. El código sólo permite HTTP cuando el host es `localhost` o `127.0.0.1`, para esta fixture local. El header `X-API-Key` se manda sólo al destino configurado; no se imprime la clave, el cuerpo ni la URL completa en el log. La clave `training-demo-only` no es un secreto real.

En AEM as a Cloud Service, el valor secreto no va en Git: una configuración OSGi puede referir `$[secret:STATUS_API_KEY]`, cuyo valor se administra por ambiente en Cloud Manager. Un endpoint que varía por ambiente puede usar `$[env:TRAINING_STATUS_URL]`; un valor estable puede permanecer inline. **No copies la URL de loopback a Cloud**: allí `127.0.0.1` designa la propia instancia AEM. La preparación de secretos locales mediante `secretsdir` se documenta en Adobe; esta demo rápida usa sólo una credencial ficticia en ConfigMgr. [Adobe, configuración OSGi](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi).

En el ejemplo, `@AttributeDefinition(type = AttributeType.PASSWORD)` sólo enmascara el campo de ConfigMgr; no reemplaza a un almacén de secretos. El servicio resuelve la configuración y envía el valor en `X-API-Key` únicamente al destino HTTPS aprobado. No debe aparecer en `/content`, HTML, JavaScript, parámetros de usuario ni logs. [Adobe, gestión de secretos](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/developing/advanced/secrets).

## 5. Demo del instructor · Author SDK y stub local

Sigue la [preparación completa](examples/session-42/README.md) antes de la reunión. Ejecuta `java --add-modules jdk.httpserver reference/examples/session-42/StubServer.java` desde la raíz del repositorio con el JDK de AEM; el stub escucha **sólo loopback** en el mismo equipo que Author. El código copiable al proyecto AEM está en `reference/examples/session-42/core/`; el modelo se crea en Author. Este repositorio de formación no incluye reactor Maven ni una instancia AEM ejecutándose, así que la observación en SDK indicada aquí es **esperada**, no una ejecución registrada.

1. Verifica el stub: `curl -i -H 'X-API-Key: training-demo-only' http://127.0.0.1:8765/ok` devuelve `200`.
2. Abre `Training: external status probe` en ConfigMgr: `/ok`, clave ficticia, conexión `1000 ms`, lectura `2000 ms`. Inicia el modelo manual con una página existente. Busca `Session 42 upstreamStatus=200 outcome=OK` y el workflow completo.
3. Cambia sólo la clave a `wrong` y lanza **otra** instancia: `401 STOP`. La falla pertenece a credenciales; restaura la clave.
4. Cambia sólo el endpoint a `/unavailable` y lanza otra instancia: `503 RETRY`. Hay respuesta del proveedor; el paso falla deliberadamente y no reintenta solo.
5. Cambia a `/slow` y lanza otra instancia: aparece `SocketTimeoutException RETRY` tras ~2 segundos de espera de lectura. El stub terminará su demora de 3 segundos, pero AEM ya cerró la espera.

El log de la clase `ProbeExternalStatusProcess` incluye el ID del workflow y el resultado. Usa ese ID para correlacionar la instancia; el log del servicio distingue el status HTTP de un problema de transporte. El servidor local también registra la ruta solicitada. No hay un `503` inventado en AEM: lo devuelve el stub real.

## 6. Si local funciona y Cloud falla

Aísla la etapa: configuración OSGi efectiva y secreto → resolución DNS → conexión y proxy/egress → TLS → respuesta HTTP → interpretación de negocio. Un `401` demuestra que **sí hubo una respuesta** del proveedor; un timeout no prueba si falló DNS, conexión o lectura sin más evidencia. Consulta el log del receptor si tienes acceso, sin registrar credenciales.

AEM Cloud permite HTTP/HTTPS saliente en puertos estándar sin Advanced Networking. Un proveedor que exige IP de salida fija, red privada o puertos no estándar puede requerir configuración de red adicional; su elección depende del destino y de la política del proveedor. La configuración avanzada no se prueba en este SDK local. [Adobe, Advanced Networking](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/networking/advanced-networking) · [Adobe, egress](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/security/configuring-advanced-networking).

## Repaso con respuestas

1. **¿Qué muestra `401` frente a un timeout?** `401` es respuesta HTTP recibida y apunta primero a credenciales/permisos; un timeout necesita ubicar la etapa de red o espera.
2. **¿Por qué fijar conexión y lectura por separado?** Miden esperas distintas; conectar rápido no garantiza una respuesta rápida.
3. **¿Dónde va la clave real en Cloud?** En una variable secreta de Cloud Manager referida desde OSGi con `$[secret:...]`, no como literal en Git.
4. **¿Por qué no reintentar `401` automáticamente?** La misma configuración inválida repetirá el rechazo y consumirá recursos sin corregirlo.
5. **¿Qué falta para repetir una escritura remota sin duplicarla?** Identidad de operación, estado durable y una política acotada; la clasificación `RETRY` no ofrece exactamente una vez.
6. **¿Por qué no usar `127.0.0.1` en Cloud?** Es el loopback de la propia instancia, no el equipo donde corre el stub local.

## Fuentes oficiales

- [Adobe, AEM Cloud development guidelines: HTTP saliente y tareas de fondo](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/development-guidelines)
- [Adobe, configuración OSGi y variables secretas](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi)
- [Adobe, Advanced Networking](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/networking/advanced-networking)
- [Adobe, configuración de egress](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/security/configuring-advanced-networking)

- [Oracle Java 11, URLConnection](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/net/URLConnection.html)
- [RFC 9110, HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [AWS Builders’ Library, timeouts, retries, backoff y jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
