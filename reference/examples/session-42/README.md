# Sesión 42 · HTTP saliente desde AEM con un stub local

Esta demo usa **Author SDK local y un servidor HTTP de prueba en el mismo equipo**. El servicio OSGi fija destino, credencial y timeouts; un Process Step manual hace una sola llamada y registra su clasificación. No hay servlet público, llamada desde el render de página ni reintento automático. Los resultados en Author son esperados hasta ejecutarlos en tu SDK.

## Archivos copiables

| Archivo | Función |
| --- | --- |
| [ExternalStatusService.java](core/src/main/java/com/adobe/aem/guides/wknd/core/training/ExternalStatusService.java) | GET con timeout de conexión y lectura, header de autenticación y clasificación. |
| [ProbeExternalStatusProcess.java](core/src/main/java/com/adobe/aem/guides/wknd/core/training/ProbeExternalStatusProcess.java) | Process Step para iniciar la comprobación manualmente en Author. |
| [ExternalStatusServiceTest.java](core/src/test/java/com/adobe/aem/guides/wknd/core/training/ExternalStatusServiceTest.java) | Prueba local de 200, 401, 503, timeout y rechazo de HTTP remoto. |
| [StubServer.java](StubServer.java) | Servidor de prueba con el JDK, ligado sólo a `127.0.0.1:8765`. |

El ejemplo supone el package WKND `com.adobe.aem.guides.wknd.core.training`. En Archetype, cambia el package de los tres Java de `core/`. `StubServer.java` se ejecuta aparte y no se copia al bundle AEM. No requiere dependencia HTTP adicional: utiliza `HttpURLConnection`, disponible en el JDK y contemplado por [Adobe para HTTP saliente](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/development-guidelines#outgoing-http-connections). Tu baseline ya debe incluir AEM SDK API, anotaciones OSGi, SLF4J, JUnit 5 y Mockito como en la sesión 41.

## Preparación antes de la clase

1. Arranca el Author SDK local directamente en el equipo donde ejecutarás el stub. En otra terminal, desde la raíz de este repositorio, ejecuta `java --add-modules jdk.httpserver reference/examples/session-42/StubServer.java` con el mismo JDK 11 o posterior que usas para AEM; detén el servidor con Ctrl+C al terminar. Prueba `curl -i -H 'X-API-Key: training-demo-only' http://127.0.0.1:8765/ok`: debe responder `200`. La clave es **ficticia y sólo local**.
2. Copia los dos Java de `core/src/main/java` y la prueba de `core/src/test/java` a tu proyecto AEM. Ejecuta `mvn -pl core -Dtest=ExternalStatusServiceTest test`, o el comando equivalente. Instala tu paquete en Author; en WKND suele usarse `mvn clean install -PautoInstallSinglePackage`.
3. En `/system/console/configMgr`, abre **Training: external status probe** y establece `endpoint=http://127.0.0.1:8765/ok`, `apiKey=training-demo-only`, `connectTimeoutMs=1000`, `readTimeoutMs=2000`. Después, en `/system/console/components`, confirma que `ExternalStatusService` y `ProbeExternalStatusProcess` están activos; el servicio requiere configuración para activarse. Exige HTTPS para destinos remotos y sólo permite HTTP para `localhost` o `127.0.0.1`.
4. En **Tools → Workflow → Models**, crea `Training probe external status`: Start → Process Step → End. Elige `Training: probe external status`, activa **Handler Advance**, deja argumentos vacíos y pulsa **Sync**. No crees un launcher: la ejecución es manual. Usa como payload una página que ya exista, por ejemplo `/content/wknd/us/en` en WKND; en Archetype usa la raíz real de tu sitio.
5. Si no aparece el registro INFO en `crx-quickstart/logs/error.log`, configura un logger local para el package `...core.training`, como en la [sesión 23](../../session-23-study-guide.html#ejemplos-locales). Filtra `Session 42`. El código registra estado y clase de error, nunca la clave ni el cuerpo HTTP.

## Demo en vivo · 8 minutos

| Configura `endpoint` | Inicia el mismo modelo con el mismo payload | Evidencia esperada en `error.log` |
| --- | --- | --- |
| `/ok` con clave correcta | Una instancia | `upstreamStatus=200 outcome=OK`; workflow termina. |
| `/ok` con clave `wrong` | Otra instancia | `upstreamStatus=401 outcome=STOP`; el paso falla; restaura la clave ficticia antes de continuar. |
| `/unavailable` | Otra instancia | `upstreamStatus=503 outcome=RETRY`; el paso falla y pide diagnóstico; **no** se reintenta solo. |
| `/slow` | Otra instancia | `transportFailure=SocketTimeoutException outcome=RETRY` tras el read timeout; no esperes los 3 segundos del stub. |

Cada cambio de endpoint se hace en ConfigMgr antes de iniciar una **nueva** instancia. No reinicies ciegamente un workflow fallido: mira el estado, corrige configuración o servicio y decide si corresponde un nuevo intento. El ejemplo clasifica `429` y `5xx` como `RETRY`; otros códigos distintos de `200`, incluido `401`, son `STOP`. Un fallo de transporte se clasifica como `RETRY` para someterlo a una política acotada del llamador. La sesión 41 enseña la cola para esa política; este Process Step no la configura ni la ejecuta.

## Si la observación difiere

| Síntoma | Primera comprobación |
| --- | --- |
| No aparece el servicio | Configuración válida, DS component, package y bundle activo. |
| `Connection refused` | Stub activo en `127.0.0.1:8765` y Author en la misma red local. |
| `401` inesperado | Clave ficticia del ConfigMgr; no la copies a Git ni a un log. |
| `503` | Ruta `/unavailable`; respuesta del stub, no conectividad rota. |
| Timeout | Distingue conexión de lectura; `/slow` tarda 3 segundos y el cliente lee como máximo 2. |
| En Cloud falla pero local funciona | Comprueba destino, proxy/egress, DNS, allowlist, secreto OSGi y log del servicio receptor; `127.0.0.1` en Cloud apunta a la instancia AEM, no al equipo del instructor. |

En Cloud, define el endpoint HTTPS por configuración y usa `$[secret:STATUS_API_KEY]` en `ui.config` con el secreto creado en Cloud Manager; **nunca publiques el valor**. Si el proveedor exige IP fija, puerto no estándar o red privada, revisa [Advanced Networking](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/networking/advanced-networking) y el [enrutamiento de egress](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/security/configuring-advanced-networking). HTTP(S) por puertos estándar no exige por sí solo esa configuración. Esta demo no despliega ni prueba conectividad Cloud.

Fuentes: [Adobe, HTTP saliente y timeouts](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/development-guidelines#outgoing-http-connections) · [Adobe, configuración OSGi y secretos](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi) · [Adobe, Advanced Networking](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/networking/advanced-networking).

**Comprobación realizada:** los dos Java de `core/` compilaron con source/target 11 frente a AEM SDK API `2025.3.19823.20250304T101418Z-250300`; Bnd `5.1.2` generó los descriptores DS y el campo OSGi Password. La prueba JUnit pasó (1 prueba, 0 fallos) con un servidor HTTP en proceso. El stub de Java respondió 200, 401, 503 y timeout en loopback. La instalación y ejecución en Author SDK siguen pendientes en tu proyecto AEM.

## Cómo interpretar sus límites

`Outcome.RETRY` es un enum propio: no es `JobResult.FAILED` y no activa Sling Jobs. El ejemplo agrupa todos los 5xx y los IOException para facilitar la demo; un 501, un certificado inválido o un host mal configurado pueden requerir corrección. Los dos timeouts no equivalen a un deadline total, y la sonda sólo comprueba el código HTTP. Las slides explican validación del cuerpo, presupuesto global, backoff, jitter e idempotencia remota como decisiones de integración; este código no las implementa.
