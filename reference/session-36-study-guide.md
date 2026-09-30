# Sesión 36 · Elegir el flujo de entrega

**Lunes 5 de octubre de 2026 · Semana 8 · Núcleo de 30 minutos, ampliable a 60**

[Versión HTML](session-36-study-guide.html) · [Slides en inglés](../lessons/0036-cloud-manager-delivery-path.html#slide-deck) · [Caso guiado](#caso-guiado)

## Objetivo observable

Ante una **ficha de evidencia simulada**, elegir la pipeline de Cloud Manager y explicar qué commit se construiría, qué artefacto produciría y a qué ambiente llegaría. Reconstruir el mapa `commit → repositorio/rama/ruta → ejecución → artefacto → ambiente` y distinguir qué demuestra cada dato. La sesión 37 examinará fallos dentro de la ejecución. Esta sesión es completamente teórica: no requiere cuenta Cloud, terminal ni despliegue.

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–5 | 1–3 | Ubicar programa, ambiente, repositorio y dos clases de pipeline. |
| 5–14 | 4–7 | Elegir tipo según el archivo y quién lo entrega hoy. |
| 14–22 | 8–9 | Trazar un commit hasta la ejecución y resolver la rama equivocada. |
| 22–28 | 10–11 | Clasificar cuatro tarjetas de cambio y defender la evidencia. |
| 28–30 | 12 | Cierre y pregunta de diagnóstico. |

Para 60 minutos, dedica 15 minutos más a comparar las cuatro tarjetas y 15 a discutir variantes del caso simulado. No se realiza ninguna práctica en Cloud Manager ni en la terminal.

## 1. Las coordenadas de una entrega

En Cloud Manager, el **programa** reúne los ambientes y repositorios asociados al proyecto. Una pipeline selecciona repositorio, rama y, para ciertas entregas dirigidas, la ruta de código; una ejecución toma ese origen, construye un resultado y lo entrega a un destino. Registrar sólo “la pipeline pasó” deja sin respuesta qué versión se usó. La selección concreta debe verificarse en la configuración y en el detalle de la ejecución. Cloud Manager admite repositorios administrados por Adobe y repositorios externos compatibles; no presupongas que el commit de tu clon local es el que leyó la pipeline. [Pipelines — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/cicd-pipelines/introduction-ci-cd-pipelines) · [Repositorios — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/managing-code/managing-repositories).

Hay **dos decisiones independientes**:

| Decisión | Opciones relevantes | Qué demuestra |
| --- | --- | --- |
| Destino y propósito | Una pipeline de despliegue no productiva puede entregar a desarrollo; la productiva estándar pasa por stage y después producción. Una pipeline de calidad ejecuta análisis sin desplegar. | Que el resultado se analizó o llegó al ambiente indicado, según el tipo y estado de la ejecución. |
| Contenido entregado | Full-stack, front-end, web tier config o config. | Qué familia de artefactos procesa esa pipeline; no que otro tipo de cambio haya llegado con ella. |

En el flujo productivo estándar, la pipeline entrega primero a **stage** y, tras sus controles y aprobación, a **producción**. Comprueba el estado de cada etapa; una ejecución detenida en stage no prueba producción. Un ambiente de desarrollo se asocia con pipelines no productivas. [Producción — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/cicd-pipelines/configuring-production-pipelines) · [Ambientes — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/manage-environments).

## 2. Elegir por el cambio real

| Cambio | Ruta habitual | Comprobación antes de elegir |
| --- | --- | --- |
| Java, Sling Models, servicios OSGi, Repo Init, paquetes AEM o clientlibs empaquetadas en el proyecto | **Full-stack** | ¿El módulo y sus dependencias están en la rama construida? |
| Tema o aplicación estática gestionada por una pipeline front-end | **Front-end** | ¿El sitio usa ese tema y conserva compatible el HTML/JSON que consume? |
| Vhost, rewrite, filtros o caché de Apache/Dispatcher | **Web tier config** si existe para ese ambiente; si no, revisar cómo el full-stack entrega Dispatcher | ¿Cuál pipeline es dueña de Dispatcher en ese ambiente y cuál es su code location? |
| Reglas CDN admitidas, reenvío de logs o configuración de mantenimiento soportada | **Config** | ¿El archivo usa un tipo de configuración admitido y está bajo la ruta de la pipeline? |

La pipeline full-stack entrega backend y frontend empaquetado como clientlibs. Puede incluir Dispatcher; **si existe una web tier config pipeline para ese ambiente, el full-stack ignora su configuración de Dispatcher**. La pipeline front-end entrega archivos estáticos construidos por separado; no convierte automáticamente cualquier `ui.frontend` o clientlib del proyecto en un despliegue independiente. Para una corrección que cambia a la vez el HTML que AEM produce y el tema que lo consume, coordina el orden y la compatibilidad entre ambas entregas. [Tipos de pipeline — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/cicd-pipelines/introduction-ci-cd-pipelines) · [Contrato front-end — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/developing-with-front-end-pipelines).

Una pipeline **config** sirve para configuraciones compatibles como reglas CDN y log forwarding; no es la vía genérica para `.cfg.json` de OSGi, que viaja con el código de aplicación. La sesión 38 tratará valores de entorno y secretos. [Config pipelines — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/config-pipeline).

## 3. Seguir commit, artefacto y destino

La siguiente ficha es un **ejemplo inventado** para leer una ruta de entrega; no describe una pipeline ni un ambiente disponible para el grupo:

| Campo | Ejemplo didáctico | Dónde buscar la prueba |
| --- | --- | --- |
| Cambio y commit | Vhost corregido en `c36b2` | Diff y SHA en Git. |
| Origen elegido | Repositorio `site`, rama `main`, ruta `dispatcher/` | Configuración de la pipeline. |
| Ejecución | `web-tier-dev`, run `#42` | Detalle de ejecución: origen usado, pasos y estado. |
| Artefacto | Configuración Apache/Dispatcher | Tipo de pipeline y resultado del build. |
| Destino | Ambiente `dev`, capa web | Ambiente seleccionado y despliegue completado. |
| Comprobación | GET con el Host afectado y resultado esperado | Petición y logs en el ambiente de destino. |

El SHA de ejemplo y el número de ejecución son ficticios. En la discusión, identifica qué dato permitiría verificar el commit, el artefacto y el destino si se tuviera acceso al sistema. **Desplegar código, publicar contenido y refrescar cachés son hechos distintos**. La clase 31 trató publicación; las clases 32–34 trataron la respuesta pública. [Pipelines — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/cicd-pipelines/introduction-ci-cd-pipelines).

## Caso guiado

**Traza didáctica simulada; no es una ejecución real de Cloud Manager.** Un vhost de Dispatcher debe aceptar `www.example.test`. El commit `c36b2` corrige la regla en `feature/host-fix`; la rama `main` aún termina en `a36f1`. La pipeline `web-tier-dev` está configurada con el repositorio correcto, `main`, ruta `dispatcher/` y destino `dev`. El run `#42` termina en verde, pero la petición al ambiente dev sigue fallando.

| Pregunta | Evidencia | Respuesta sustentada |
| --- | --- | --- |
| ¿Es la familia de pipeline adecuada? | Cambió un vhost y el ambiente tiene web tier config pipeline. | Sí, web tier config es su dueña. |
| ¿Contiene el run el arreglo? | Run `#42` leyó `main` en `a36f1`; el arreglo sólo existe en `feature/host-fix` en `c36b2`. | No. Verde sólo acredita esa ejecución de `main`. |
| ¿Qué decisión recomendarías? | La rama de entrega no contiene `c36b2`. | Integrar el cambio según el flujo del equipo antes de una futura ejecución; después haría falta evidencia de un nuevo run y del resultado en `dev`. |

La explicación del caso comienza por la rama y el commit que aparecen en la ficha. **Variante:** si el run sí incluye `c36b2` y llegó a dev, revisa el artefacto y la respuesta en la capa web; ése es el punto de partida de la sesión 37. Si el run es de *code quality*, su verde no demuestra ningún despliegue.

## Análisis guiado sin entorno

El instructor muestra la traza simulada del [caso guiado](#caso-guiado) y pausa antes de revelar cada respuesta. No se abren Cloud Manager, Git ni una terminal.

1. Muestra el archivo modificado (`dispatcher/site.vhost`) y pregunta quién entrega esa clase de archivo. **Respuesta:** web tier config si es la pipeline dueña del ambiente; de lo contrario, se comprueba la opción Dispatcher del full-stack.
2. Muestra las dos puntas de rama: `feature/host-fix → c36b2` y `main → a36f1`. Pregunta si un run que lee `main` puede contener el arreglo. **Respuesta:** no, con la evidencia suministrada.
3. Muestra `web-tier-dev`, run `#42`, estado verde y destino `dev`. Pregunta qué prueba y qué no prueba el verde. **Respuesta:** terminó esa ejecución; no demuestra que incluyera `c36b2` ni que producción recibiera cambios.
4. Pide que cada participante formule una conclusión en una frase: “La pipeline elegida corresponde al archivo, pero el run #42 tomó `main` en `a36f1`; por eso no contiene el arreglo `c36b2`”.

**Variante para discusión:** si la ficha dijera que el run usó `c36b2`, ¿qué información adicional pedirías? El artefacto generado, la etapa completada y una comprobación de la respuesta en el destino. La sesión 37 profundizará en cómo leer los fallos de esas etapas. Todos los identificadores y resultados son didácticos.

## Preguntas de aplicación

Discute estas cuatro situaciones hipotéticas. Para cada una, indica la pipeline probable y qué dato haría falta para confirmar el origen y destino; no se ejecuta nada.

1. Se modifica un Sling Model y su configuración OSGi versionada. **Respuesta:** full-stack; comprobar el paquete y el servicio en el ambiente destino.
2. Se modifica el CSS de un tema que el sitio entrega mediante front-end pipeline. **Respuesta:** front-end; comprobar el build estático y la versión del tema que usa la página. Si el CSS va empaquetado como clientlib AEM, es full-stack.
3. Se modifica un rewrite en el vhost de Dispatcher. **Respuesta:** web tier config si existe para ese ambiente; en caso contrario, comprobar la opción de Dispatcher del full-stack. En un entorno real harían falta status y `Location` con el Host correcto.
4. Se modifica una configuración admitida de reenvío de logs. **Respuesta:** config; identificar el archivo, el tipo admitido, la pipeline y el ambiente destino en la ficha suministrada. No afirmar que el cambio está desplegado ni usar esta ruta para `.cfg.json` de OSGi.

## Repaso con respuestas

1. **¿Un run verde significa que mi commit llegó a producción?** No. Compara el SHA usado, el tipo de pipeline y la etapa alcanzada.
2. **¿Una pipeline de calidad entrega código?** No; analiza sin desplegar.
3. **¿Dónde va una clientlib del proyecto AEM?** Normalmente en full-stack. Front-end exige una entrega estática separada y un sitio configurado para consumirla.
4. **¿Quién entrega Dispatcher si existe web tier config para ese ambiente?** Esa pipeline; el full-stack ignora sus archivos Dispatcher allí.
5. **¿Publicar una página es ejecutar la pipeline?** No. La publicación mueve contenido; la pipeline entrega código o configuración.

## Fuentes oficiales

- [Pipelines CI/CD de Cloud Manager — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/cicd-pipelines/introduction-ci-cd-pipelines)
- [Configurar pipeline productiva — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/cicd-pipelines/configuring-production-pipelines)
- [Administrar repositorios — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/managing-code/managing-repositories)
- [Desarrollo con front-end pipeline — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/developing-with-front-end-pipelines)
- [Config pipelines — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/config-pipeline)
