# Sesión 46 · Elegir la prueba que demuestra el riesgo

**Lunes 19 de octubre de 2026 · Semana 10 · 30 minutos**

[Versión HTML](session-46-study-guide.html) · [Slides](../lessons/0046-risk-based-testing.html#slide-deck) · [Práctica voluntaria de la semana 10](wknd-project-backlog.html#practice-10)

## Objetivo observable

Ante un riesgo concreto, identificar el resultado observable, su valor esperado y el entorno que puede demostrarlo. Aplicar el criterio a un Sling Model, un servicio OSGi, la resolución de un servlet y los permisos de un service user. El `TrainingMessageModel` sirve como demo de una prueba negativa que detecta una regresión; no es el único tipo de prueba de la sesión.

Esta clase continúa la [sesión 19](session-19-study-guide.html) y usa exactamente las clases de las [sesiones 18](examples/session-18/core/src/main/java/com/adobe/aem/guides/wknd/core/training/TrainingMessageModel.java) y [19](examples/session-19/core/src/test/java/com/adobe/aem/guides/wknd/core/training/TrainingMessageTest.java). El archivo de ejemplo de esta sesión es [el test completo con un tercer caso](examples/session-46/TrainingMessageTest.java). Se reemplaza el test anterior en un proyecto local; no se añade una clase duplicada con el mismo nombre.

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–5 | 1–2 | Riesgo, observación, resultado esperado y entorno. |
| 5–10 | 3–4 | Capas de pruebas AEM y alcance de AEM Mocks. |
| 10–19 | 5–7 | Casos negativos y demo roja/verde del Model. |
| 19–26 | 8–10 | Servicio OSGi, resolución Sling y permisos efectivos. |
| 26–29 | 11 | Puntos clave. |
| 29–30 | 12 | Preguntas. |

## Concepto: qué demuestra una prueba

Una prueba útil empieza por un riesgo para un autor, visitante u operación de AEM. Después define **qué salida pública** lo revelaría y **qué salida espera** para una entrada concreta. El entorno donde corre es parte de la afirmación: un getter ejecutado en AEM Mocks, una respuesta HTTP del Author SDK y una interacción del navegador observan cosas diferentes. Un test negativo comprueba el comportamiento ante una entrada o condición adversa; cuando el producto la maneja correctamente, el test debe **pasar**.

| Nivel | Sitio habitual en AEM | Observa | Ejemplo de riesgo |
| --- | --- | --- | --- |
| Unit test | `core`, JUnit 5 con AEM Mocks o Mockito | Lógica Java, recursos, modelos y servicios registrados en un contexto controlado. | Un Model devuelve vacío ante contenido válido pero incompleto. |
| HTTP funcional | SDK local; módulo `it.tests` en Cloud Manager | Ruta instalada, método, status, cuerpo e identidad de la petición. | Sling elige otro servlet o un filtro rechaza la petición. |
| UI en navegador | Recorrido local; módulo `ui.tests` en Cloud Manager | Interacción de autor o visitante con la página real. | Un control no se puede usar en el flujo completo. |

Adobe describe [unit tests, pruebas funcionales HTTP y pruebas UI](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/test-results/functional-testing/functional-testing) como capas con objetivos distintos. Esta sesión no monta una suite de cada tipo: elige la primera comprobación capaz de observar el riesgo. El recorrido UI se desarrolla en la sesión 47. El resultado local tampoco demuestra por sí solo un gate del pipeline.

## Elegir por comportamiento observable

| Riesgo | Comprobación apropiada | Qué observa | Límite |
| --- | --- | --- | --- |
| `title` contiene sólo espacios y la página pierde su texto de fallback | JUnit 5 con AEM Mocks sobre el getter público | Valor que HTL recibiría de `getTitle()` | No renderiza la página ni prueba el runtime completo. |
| El servicio devuelve un valor inválido ante configuración vacía | JUnit 5 con activación del servicio o un stub controlado | Resultado y decisión del servicio | No prueba configuración efectiva del SDK o Cloud. |
| Un servlet acepta un método o selector indebido | Prueba de contrato del servlet y, si importa el registro/routing, petición HTTP al SDK | Respuesta del método y luego ruta real | Un request mock no prueba Sling servlet resolution. |
| Un service user puede leer o escribir más de lo autorizado | Identidad efectiva en SDK y lectura/escritura acotada | Resultado de ACL y mapping instalados | Un resolver in-memory no aplica el Repo Init real. |
| La página responde con el título esperado | Petición HTTP al Author SDK local | Código, cuerpo y capa HTTP observada | No demuestra el estado de Publish o Cloud. |

Para diseñar un negativo, cambia una condición por vez. En el caso del Model, la propiedad existe pero contiene espacios. En el [servicio HTTP de la sesión 42](examples/session-42/core/src/test/java/com/adobe/aem/guides/wknd/core/training/ExternalStatusServiceTest.java), el stub devuelve `503` o tarda más que el timeout. En un servlet, un método o selector no admitido debe seguir el contrato de rechazo o quedar fuera del handler pretendido; el status final depende del routing instalado.

## Caso central: `TrainingMessageModel`

El modelo existente hace `trim()` del título y devuelve `Weekend Guides` cuando el valor es nulo o queda vacío. El test de la sesión 19 cubre un título normal y el caso **ausente**. Un campo presente con `"   "` es una entrada distinta y merece un caso negativo. La nueva aserción observa el getter público, que es el contrato de la vista.

El ejemplo completo está en [`TrainingMessageTest.java`](examples/session-46/TrainingMessageTest.java). La parte nueva es:

```java
@Test
void usesFallbackWhenTitleContainsOnlySpaces() {
    context.registerInjectActivateService(new TrainingMessage(), "message", "Local Author");
    context.addModelsForClasses(TrainingMessageModel.class);
    Resource resource = context.create().resource("/content/training/message", "title", "   ");

    TrainingMessageModel model = context.getService(ModelFactory.class)
            .createModel(resource, TrainingMessageModel.class);

    assertEquals("Weekend Guides", model.getTitle());
}
```

No hagas `assertEquals` contra el campo privado ni reproduzcas la lógica `trim()` dentro del test. Eso sólo compararía dos implementaciones. La salida esperada proviene de la promesa para el consumidor. La [guía oficial de Adobe sobre unit tests de WKND](https://experienceleague.adobe.com/en/docs/experience-manager-learn/getting-started-wknd-tutorial-develop/project-archetype/unit-testing) muestra JUnit, Mockito y AEM Mocks en el proyecto.

## Demo local: prueba roja y verde

**Preparación:** tener el proyecto WKND local de las sesiones 18 y 19 con `TrainingMessage`, `TrainingMessageModel` y `TrainingMessageTest`. En `core/src/test/java/com/adobe/aem/guides/wknd/core/training/`, sustituir el test anterior por [esta versión completa](examples/session-46/TrainingMessageTest.java). Ejecutar desde la raíz del proyecto local:

```bash
mvn -pl core -Dtest=TrainingMessageTest test
```

1. Ejecuta las tres pruebas sobre el modelo intacto. La tercera debe pasar. Si el proyecto usa otro nombre de módulo o dependencias, ajusta el comando al POM local.
2. En una rama desechable, elimina **sólo** la condición `title.trim().isEmpty()` del ternario en `getTitle()`. Repite el mismo comando: la tercera prueba debe fallar porque ahora devuelve `""`.
3. Restaura esa condición. Repite el comando: la prueba vuelve a pasar. Verifica con `git diff` que no queda la mutación temporal.
4. Explica el alcance: se demostró la política del getter para esa entrada. La prueba no observó una petición HTTP, ACL ni configuración instalada.

Si la primera ejecución falla por creación del modelo, registro del servicio o dependencias de Maven, corrige el setup antes de atribuir el fallo al fallback. No presentes como “roja” una prueba que no llegó a la aserción. Mantén el nombre del test y el error de aserción visibles en la demo.

## Cómo aplica a otros límites de AEM

**Servicio OSGi con HTTP saliente.** El [`ExternalStatusServiceTest` de la sesión 42](examples/session-42/core/src/test/java/com/adobe/aem/guides/wknd/core/training/ExternalStatusServiceTest.java) usa un servidor HTTP local controlado: `200 → OK`, `401 → STOP`, `503 → RETRY` y timeout `→ RETRY`. Comprueba la **clasificación** del servicio ante respuestas reales del stub, sin depender de un proveedor externo. No prueba que el endpoint configurado, el secreto o la salida de red funcionen en AEM instalado. Para esos riesgos, inspecciona la configuración efectiva y ejecuta una comprobación acotada en Author SDK. [Adobe: pruebas funcionales HTTP](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/test-results/functional-testing/functional-testing).

**Servlet de Sling.** Una prueba que llama el método del servlet con un request mock puede comprobar respuesta, validación y manejo de errores. La selección del servlet para una URL depende del recurso y su `sling:resourceType`, además de selector, extensión, método y registros disponibles. Por eso, si el riesgo es «¿responde mi servlet a esta URL y método?», solicita la ruta real en el SDK y registra status, cuerpo y handler observado. `GET /content/training/guide.status.json` es un ejemplo **ilustrativo**, no una ruta implementada en este repositorio. Un selector o método incorrecto no garantiza un status universal: otra ruta o el servlet por defecto puede responder. [Apache Sling: Servlets and Scripts](https://sling.apache.org/documentation/the-sling-engine/servlets.html).

**Service user y Repo Init.** El [`TrainingGuideReaderTest` de la sesión 29](examples/session-29/core/src/test/java/com/adobe/aem/guides/wknd/core/training/TrainingGuideReaderTest.java) prueba que el código solicita el subservice `training-guide-read` y cierra el resolver que creó. Mockito suministra ese resolver; no carga el mapping ni las ACL. Para afirmar «esta identidad puede leer esta ruta y no otra», comprueba mapping, Repo Init y acceso efectivo con el service user real en el SDK. Prueba la ruta permitida y una que la política pretende restringir; anota el resultado, incluidos permisos heredados. [Adobe: service users](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/developing/advanced/service-users).

## Límite del mock y siguiente comprobación

`AemContext` proporciona recursos y servicios para pruebas rápidas. El resolver elegido cambia qué capacidades simula. La [documentación de wcm.io](https://wcm.io/testing/aem-mock/usage.html) indica que AEM Mocks no implementa toda la pila de editable templates y policies. Los [tipos de ResourceResolver](https://wcm.io/testing/aem-mock/junit5/apidocs/org/apache/sling/testing/mock/sling/ResourceResolverType.html) tienen diferencias concretas: `RESOURCERESOLVER_MOCK` no usa JCR; `JCR_MOCK` no cubre todas las funciones JCR, como búsqueda, versionado y eventos. Incluso `JCR_OAK` no sustituye una instancia AEM con bundles, configuración, filtros y permisos reales.

Para una pregunta HTTP, instala el componente de la sesión 18 en un **Author SDK local de práctica** y solicita una página de práctica que lo use:

```bash
curl -sS -o /tmp/session-46-page.html -w '%{http_code}\n' \
  'http://localhost:4502/content/<ruta-de-practica>.html'
```

Comprueba el código de estado y busca `Weekend Guides` en el archivo de respuesta. Si la página requiere autenticación, usa la sesión local autorizada del entorno de práctica y no compartas credenciales. La ruta real, template y componente deben existir antes; esta orden no crea contenido. Si el riesgo es ACL, la petición HTTP de administrador no responde la pregunta: usa la identidad técnica real y verifica una lectura permitida y otra denegada en el SDK, según las [sesiones 28](session-28-study-guide.html) y [29](session-29-study-guide.html). No infieras permisos a partir de un mock que creó los recursos.

Las pruebas funcionales Java de Cloud Manager usan el módulo [`it.tests`](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/test-results/functional-testing/java-functional-testing). Aquí no se ejecuta Cloud Manager y ninguna captura local se presenta como resultado de su pipeline.

## Repaso con respuestas

1. **¿Por qué el test de título ausente no cubre `"   "`?** El recurso tiene la propiedad, pero su valor queda vacío tras `trim()`. Es una rama de entrada distinta.
2. **¿Qué prueba la tercera aserción?** El valor que devuelve `getTitle()` para esa entrada con el servicio registrado.
3. **¿Qué resultado invalida la demo roja?** Un error de setup previo a la aserción; no demuestra la regresión buscada.
4. **¿Puede AEM Mocks demostrar permisos Repo Init instalados?** No. Hay que verificar la identidad efectiva y sus ACL en una instancia.
5. **¿Qué prueba `curl` contra Author?** Sólo la ruta y respuesta observadas en ese Author, con su contenido y configuración actuales.
6. **¿Qué falta tras el test de `ExternalStatusService` con stub?** La configuración efectiva y la conectividad del AEM instalado.
7. **¿Qué falta tras probar directamente `doGet`?** La resolución del servlet para la URL real, incluidos método, selector y registro.

## Fuentes

- [Adobe · Functional testing in AEM as a Cloud Service](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/test-results/functional-testing/functional-testing)
- [Adobe · Java functional tests and `it.tests`](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/test-results/functional-testing/java-functional-testing)
- [Adobe · WKND unit testing tutorial](https://experienceleague.adobe.com/en/docs/experience-manager-learn/getting-started-wknd-tutorial-develop/project-archetype/unit-testing)
- [wcm.io · AEM Mocks usage](https://wcm.io/testing/aem-mock/usage.html)
- [wcm.io · ResourceResolverType](https://wcm.io/testing/aem-mock/junit5/apidocs/org/apache/sling/testing/mock/sling/ResourceResolverType.html)
- [Apache Sling · Servlets and Scripts](https://sling.apache.org/documentation/the-sling-engine/servlets.html)
- [Adobe · Service users](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/developing/advanced/service-users)
