# Sesión 47 · Pruebas de integración con Cypress

**Martes 20 de octubre de 2026 · Semana 10 · 30 minutos**

[Versión HTML](session-47-study-guide.html) · [Slides](../lessons/0047-cypress-visible-page.html#slide-deck) · [Práctica voluntaria de la semana 10](wknd-project-backlog.html#practice-10)

## Objetivo observable

Especificar una ruta crítica **Author → Publish → visitante** y comprobar con Cypress que el título autorado aparece en la página publicada. Distinguir los datos que se preparan antes de la prueba del comportamiento que observa el navegador. Explicar cómo mantener el caso estable, cómo aislarlo, qué investigar cuando falla de forma intermitente y qué papel cumple `ui.tests` en Cloud Manager.

El ejemplo reutiliza `TrainingMessage` de la [sesión 18](examples/session-18/ui.apps/src/main/content/jcr_root/apps/wknd/components/training-message/training-message.html). La [versión HTL de esta sesión](examples/session-47/training-message.html) sólo añade un selector `data-cy`; el [spec Cypress](examples/session-47/training-message.cy.js) comprueba Publish como visitante anónimo. La autoría y la publicación preparan el fixture de este caso; el spec no automatiza los clics del editor de AEM.

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–5 | 1–2 | Riesgo y ruta Author → Publish → visitante. |
| 5–11 | 3–4 | Contrato técnico, datos y selectores estables. |
| 11–19 | 5–6 | Aislamiento y ejemplo Cypress. |
| 19–25 | 7–8 | Diagnóstico de intermitencias y `ui.tests`. |
| 25–30 | 9–10 | Puntos clave y preguntas. |

## Contrato técnico de una prueba de integración

| Parte | Caso de la sesión |
| --- | --- |
| Riesgo | El visitante ve un título ausente o anterior al aprobado en Author. |
| Precondiciones | Author y Publish locales funcionan; código instalado en ambos; la página de práctica y su título esperado ya están publicados. |
| Datos | URL **real** de Publish y título exacto de esa versión publicada. |
| Acción | Un navegador sin credenciales de Author abre la página de Publish. |
| Aserción | El `h2` de `TrainingMessage` está visible y coincide exactamente con el título esperado. |
| Evidencia | Resultado del spec, URL, instancia, versión de contenido, hora y captura si falla. |
| Limpieza | Restaurar o retirar el contenido de práctica después de la sesión. |

Un unit test del Model, como el de la sesión 46, comprueba el valor del getter en un contexto controlado. Este recorrido observa el HTML entregado por Publish y el estado visible en el navegador. No cubre todos los clics de autoría, ni demuestra el resultado detrás de un Dispatcher o CDN si el test accede directamente a Publish.

## Datos y selectores estables

Usa una página desechable con una sola instancia de `TrainingMessage`; no reutilices una página de equipo que otros pueden editar. Guarda un título conocido, por ejemplo `River walk 47`, y anota qué versión se publicó. La ejecución no debe comenzar mientras la publicación aún está pendiente. Si el título cambia, cambia también el dato esperado **sólo después de confirmar la nueva versión en Publish**.

El HTL del ejemplo agrega `data-cy="training-message"` al `<section>` existente. Cypress localiza el componente por ese atributo y comprueba el texto del `h2`. El selector no depende de `nth-child`, clases CSS ni posición visual. El texto del título sí es parte del contrato, por lo que la comparación exacta debe fallar si cambia.

## Aislamiento: navegador y repositorio

Cypress limpia la página y el estado habitual del navegador entre pruebas E2E cuando `testIsolation` está activo. Esa limpieza no revierte cambios del repositorio AEM ni despublica una página. Cada caso debe tener datos preparados de forma independiente; el spec de la sesión tiene un solo `it` y puede ejecutarse por separado. Si una suite modifica contenido, debe asignar un recurso propio al caso y restaurarlo o retirarlo al terminar.

No uses `cy.wait(5000)` para esperar una publicación incierta. La publicación completa es una **precondición**. Para contenido que aparece de forma asíncrona en el navegador, espera una condición observable con una aserción o una respuesta identificable.

## Preparación del ejemplo local

1. En el proyecto WKND local, instala el componente `TrainingMessage` y la [versión HTL con `data-cy`](examples/session-47/training-message.html) en **Author y Publish**. La policy del template debe permitir el componente.
2. Crea una página de práctica con una sola instancia. En Author escribe `River walk 47`, guarda, publica la página y sus dependencias. Abre su URL de Publish en una ventana privada y verifica el título. La ruta exacta depende del proyecto; no copies el marcador de abajo.
3. En el proyecto que usa **Cypress 16**, coloca el [spec completo](examples/session-47/training-message.cy.js) en `cypress/e2e/training-message.cy.js`. Instala dependencias según su lockfile. Si no existe un proyecto de Cypress, crea uno local de práctica con `npm init -y` y `npm install --save-dev cypress`, y crea `cypress/e2e/`.
4. Desde el directorio del proyecto Cypress, define la URL y el texto esperado (ejemplo de shell POSIX):

```bash
export CYPRESS_publishPageUrl='http://localhost:4503/content/<ruta-real>.html'
export CYPRESS_expectedTitle='River walk 47'
npx cypress run --spec cypress/e2e/training-message.cy.js
```

El spec lee ambos valores con `cy.env()` y falla con un mensaje claro si falta alguno. No lleva credenciales de Author: un visitante debe poder abrir esa URL. El núcleo del spec es:

```js
cy.visit(publishPageUrl)
cy.get('[data-cy="training-message"] h2')
  .should('be.visible')
  .and('have.text', expectedTitle)
```

Para mostrar la frontera de publicación, cambia el título en Author sin publicar: Publish debe seguir mostrando la versión anterior y el test debe continuar pasando con el valor anterior. Después publica la nueva versión **sin** cambiar `expectedTitle`: la comparación debe fallar por texto. Actualiza el valor esperado sólo tras verificar el nuevo título en Publish y repite. Finalmente restaura o elimina la página de práctica.

## Diagnóstico de pruebas intermitentes

| Señal | Primera comprobación | Acción basada en evidencia |
| --- | --- | --- |
| A veces aparece el título anterior | Estado de publicación, URL y versión servida | Completar la publicación antes de ejecutar. |
| Falta el componente | HTL instalado, template y contenido de la página | Mantener una instancia conocida del fixture. |
| Falla sólo después de otro test | Estado compartido del navegador o repositorio | Ejecutar el spec solo y preparar datos independientes. |
| Falla sólo bajo carga | Cronología de request, DOM y aserción | Esperar la condición real; no añadir una pausa arbitraria. |
| Hay 404 o redirect | Ruta de Publish, publicación, acceso anónimo | Corregir el entorno antes de atribuir el fallo al componente. |

Repite el **mismo** caso y guarda URL, hora, captura, comando y primera respuesta distinta. Aumentar el timeout antes de saber qué cambió suele ocultar la causa. Las aserciones de Cypress reintentan el estado del DOM hasta cumplirse o agotar el tiempo configurado.

## Papel de `ui.tests` en Cloud Manager

La ejecución local sirve para iterar y obtener evidencia del SDK. En AEM as a Cloud Service, `ui.tests` empaqueta las pruebas UI para Cloud Manager. Su ejecución exige el contexto Docker del módulo, la activación correspondiente, datos y URLs del ambiente, y reportes JUnit en `REPORTS_PATH`. Copiar un spec al repositorio o verlo pasar localmente no demuestra que el gate de Cloud Manager se haya ejecutado. El caso debe adaptarse a fixtures y URLs estables del ambiente de pipeline.

## Repaso con respuestas

1. **¿Qué debe existir antes de `cy.visit`?** La página y la versión de contenido esperada en Publish.
2. **¿Qué hace estable a `data-cy`?** Identifica el componente sin depender de CSS o posición del DOM.
3. **¿`testIsolation` limpia AEM?** No; sólo el contexto del navegador, no el repositorio ni la publicación.
4. **¿Qué demuestra un pase en Publish local?** El resultado visible para esa URL y versión en esa instancia, no el gate de Cloud Manager.
5. **¿Qué mirar primero ante un test intermitente?** La primera divergencia observable: contenido, URL, respuesta, selector o estado compartido.

## Fuentes

- [Adobe · UI Testing in AEM as a Cloud Service](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/test-results/functional-testing/ui-testing)
- [Cypress · Best Practices](https://docs.cypress.io/app/core-concepts/best-practices)
- [Cypress · Test Isolation](https://docs.cypress.io/app/core-concepts/test-isolation)
- [Cypress · Retry-ability](https://docs.cypress.io/app/core-concepts/retry-ability)
- [Cypress · Environment Variables](https://docs.cypress.io/app/guides/environment-variables)
