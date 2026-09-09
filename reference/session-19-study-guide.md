# Sesión 19 · JUnit 5 y AEM Mocks para probar modelos y servicios

**Guía profunda de preparación · Jueves 10 de septiembre de 2026 · Español**

[Abrir la versión HTML](session-19-study-guide.html) · [Ver las diapositivas](../lessons/0019-junit-aem-mocks.html#slide-deck) · [Notas del presentador](../slides/lesson-19/speech.md)

Las [sesiones 17](session-17-study-guide.html) y [18](session-18-study-guide.html) dieron un dueño al comportamiento: modelos para la vista y servicios para capacidades reutilizables. La sesión 19 enseña a comprobar que esos dueños cumplen su contrato cuando el contenido o la configuración cambian.

> **Una prueba útil protege lo que observa el consumidor.** Prepara una entrada representativa, utiliza el contrato público y comprueba el resultado. Después demuestra que la prueba detecta la regresión que afirma proteger.

[Ir a la práctica local completa](#practica-local)

## Cómo estudiar esta guía

- **Primera lectura, 20–25 minutos:** sigue una prueba de fallback desde su fixture hasta la aserción.
- **Recuperación, 5–10 minutos:** contesta las preguntas y clasifica cada fallo antes de abrir las soluciones.
- **Antes de la sesión:** explica por qué un error de creación del modelo no demuestra todavía que su fallback esté mal.
- **Después de la sesión:** ejecuta una prueba en tu proyecto AEM y registra evidencia red → green. Los ejemplos de esta guía no equivalen a pruebas ejecutadas en tu SDK o proyecto.

**Resultado esperado:** escribir y explicar una comprobación enfocada, preparar el contexto mínimo de AEM Mocks, pasar por adaptación o activación y reconocer el límite de la prueba. No necesitas dominar Mockito ni fijar un porcentaje de cobertura.

## Índice

1. [Qué comportamiento debes proteger](#contrato)
2. [Arrange, Act, Assert](#aaa)
3. [JUnit 5 y aislamiento](#junit)
4. [Qué representa AEM Mocks](#contexto)
5. [Contenido mínimo y creación de un modelo](#modelo)
6. [Configurado, ausente, inválido y legado](#estados)
7. [Probar un servicio mediante activación](#servicio)
8. [Cuándo usar un doble de prueba](#dobles)
9. [Red → green y comandos Maven](#regresion)
10. [Diagnóstico y mapa de evidencias](#diagnostico)
11. [Repaso con respuestas](#repaso)
12. [Glosario y fuentes](#fuentes)

<a id="contrato"></a>

## 1. Qué comportamiento debes proteger

Empieza con una promesa que un consumidor pueda observar. Para la Guide Card: «Si faltan el título actual y el legado, `getDisplayTitle()` devuelve `Untitled guide`». Para un servicio: «Si la capacidad está habilitada y el destino es inválido, sigue la política de rechazo definida».

| Buen objetivo | Objetivo frágil sin una razón contractual |
| --- | --- |
| Valor que HTL recibe del getter | Nombre de un campo privado. |
| Estado vacío que controla el renderizado | Número de métodos auxiliares. |
| URL que devuelve el servicio | Orden incidental de llamadas internas. |
| Rechazo o deshabilitación documentados | Que se utilice una implementación específica de colección. |

Una refactorización puede cambiar la implementación manteniendo la promesa. La prueba debería seguir pasando en ese caso. A veces una interacción sí forma parte del contrato, como no enviar dos veces una operación externa; entonces hay una razón para verificarla. No conviertas esa excepción en una inspección de todas las llamadas.

El nombre de una prueba puede expresar estado y expectativa: `returnsFallbackWhenBothTitlesMissing`. Es más informativo que `testGetter` o `happyPath`. Base: [notas de la sesión, slides 2 y 3](../slides/lesson-19/speech.md).

<a id="aaa"></a>

## 2. Arrange, Act, Assert

La estructura mínima es:

```text
Arrange: contenido, configuración y colaboradores necesarios
    ↓
Act: ejecutar una operación del contrato público
    ↓
Assert: comparar el resultado observado con la expectativa
```

| Fase | Pregunta que debe responder |
| --- | --- |
| Arrange | ¿Qué estado provoca este comportamiento? |
| Act | ¿Qué contrato real ejecuta el consumidor? |
| Assert | ¿Qué resultado demuestra que se cumplió la promesa? |

Mantén un comportamiento identificable por fallo. Esto no prohíbe varias aserciones coherentes, pero sí aconseja separar escenarios independientes. Si una prueba comprueba título, un error de configuración, un servlet y una integración remota, el primer fallo ocultará el resto.

El setup compartido debería contener sólo lo que todos los casos necesitan. La diferencia que define un escenario debe verse cerca de la prueba; no la escondas detrás de una gran fábrica de fixtures.

<a id="junit"></a>

## 3. JUnit 5 y aislamiento

JUnit Jupiter aporta las anotaciones y aserciones utilizadas en esta sesión. Los imports pertenecen a `org.junit.jupiter`, no a las anotaciones de JUnit 4.

| Elemento | Función |
| --- | --- |
| `@Test` | Marca un método de prueba. |
| `@BeforeEach` | Prepara estado común antes de cada test. |
| `@ExtendWith(AemContextExtension.class)` | Integra el ciclo de vida del contexto AEM mock. |
| `assertEquals(expected, actual)` | Compara resultado esperado y observado. |
| `assertTrue(...)` | Comprueba una condición del contrato. |
| `assertThrows(...)` | Comprueba una excepción esperada. |

Usa un `AemContext` no estático gestionado por la extensión como punto de partida. Evita que un test dependa del contenido o servicios que dejó otro. La limpieza del contexto no arregla cualquier estado estático que tu propio código haya creado.

Para una excepción, ejecuta dentro de `assertThrows` la operación que debe fallar y elige el tipo significativo. Aceptar cualquier `Exception` puede hacer pasar una prueba por un error distinto, como una dependencia sin registrar.

Esta guía enlaza la documentación versionada de **JUnit 5**; un enlace `current` puede conducir a otra versión principal. No actualices ni rebajes dependencias sólo por copiar un tutorial: revisa el POM del proyecto y su compatibilidad. [JUnit 5 User Guide](https://docs.junit.org/5.13.4/user-guide/).

<a id="contexto"></a>

## 4. Qué representa AEM Mocks

`AemContext` ofrece recursos, resolver, request, response y un registro OSGi de prueba, junto con facilidades para modelos y APIs AEM soportadas. Esto permite ejecutar gran parte del Java de un proyecto sin arrancar el SDK.

```text
Prueba JUnit
    └── AemContext
          ├── contenido representativo
          ├── recurso / resolver / request
          ├── modelos registrados
          └── servicios y activación simulada

Fuera de esta prueba: navegador, Dispatcher y despliegue real
```

**AEM Mocks no es una instancia completa de AEM.** Un test que pasa no demuestra resolución real de paquetes OSGi, selección cloud de run modes, permisos completos del repositorio, reglas de Dispatcher ni comportamiento del navegador.

Elige un tipo de resolver mock que soporte la operación probada. Para leer propiedades e hijos normalmente basta una frontera sencilla. Si la prueba necesita semántica JCR específica, confirma que el tipo elegido la implementa. No ejecutes todos los escenarios sobre múltiples resolvers sin una necesidad concreta. Base: [notas de la sesión, slides 5 y 9](../slides/lesson-19/speech.md); consulta las [capacidades de Sling Mocks](https://sling.apache.org/documentation/development/sling-mock.html).

La fidelidad importa más que el tamaño: un árbol pequeño con las propiedades correctas puede probar más que una exportación enorme de contenido cuyo significado nadie entiende.

<a id="modelo"></a>

## 5. Contenido mínimo y creación de un modelo

El recorrido de una prueba de modelo es:

```text
JSON en src/test/resources
    ↓ cargar bajo una ruta conocida
Resource de la tarjeta
    ↓ modelo registrado y dependencias disponibles
ModelFactory.createModel(...)
    ↓ interfaz pública
getDisplayTitle() → resultado esperado
```

Un fixture contiene datos de entrada; no sustituye al código del modelo. Ejemplo ilustrativo para `core/src/test/resources/guide-card.json`:

```json
{
  "missing": {
    "jcr:primaryType": "nt:unstructured",
    "sling:resourceType": "example/components/guidecard"
  }
}
```

Si lo cargas bajo `/content/test`, el recurso del escenario estará en `/content/test/missing`. La falta de `title` y `heading` es deliberada. No uses una ruta de página si el modelo necesita el recurso de la tarjeta.

### Ejemplo de test para adaptar al proyecto

Este ejemplo supone que ya existen `GuideCardImpl`, su interfaz `GuideCard` con `getDisplayTitle()` y el contrato de fallback de la sesión 17. Añade el package e imports de esos tipos reales. Si el modelo tiene más entradas requeridas, deben prepararse explícitamente; el fragmento no las vuelve opcionales.

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

import org.apache.sling.models.factory.ModelFactory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import io.wcm.testing.mock.aem.junit5.AemContext;
import io.wcm.testing.mock.aem.junit5.AemContextExtension;

@ExtendWith(AemContextExtension.class)
class GuideCardImplTest {
    private final AemContext context = new AemContext();

    @BeforeEach
    void setUp() {
        context.addModelsForClasses(GuideCardImpl.class);
        context.load().json("/guide-card.json", "/content/test");
    }

    @Test
    void returnsFallbackWhenBothTitlesMissing() {
        // Arrange
        context.currentResource("/content/test/missing");
        ModelFactory factory = context.getService(ModelFactory.class);
        assertNotNull(factory, "El contexto debe proporcionar ModelFactory");

        // Act
        GuideCard card = factory.createModel(
            context.currentResource(), GuideCard.class);

        // Assert
        assertEquals("Untitled guide", card.getDisplayTitle());
    }
}
```

La implementación debe estar registrada como adapter de `GuideCard` si solicitas esa interfaz. Si tu proyecto expone directamente una clase, utiliza ese contrato real; no añadas una interfaz sólo para imitar el ejemplo.

`addModelsForClasses` hace explícito el registro de prueba. Es útil cuando el descubrimiento del classpath no lo proporciona. `ModelFactory#createModel` aporta un fallo de creación más diagnóstico que recibir `null` y fallar después al llamar al getter. [Patrón de pruebas de modelos — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/getting-started-wknd-tutorial-develop/project-archetype/unit-testing).

**Si el modelo adapta request:** utiliza `context.request()` como entrada y prepara los atributos o bindings que requiere. Seleccionar un recurso actual no crea todas las variables del contexto de scripting. La prueba debe respetar el mismo contrato de adaptables estudiado en la sesión 17.

<a id="estados"></a>

## 6. Configurado, ausente, inválido y legado

Protege estados diferentes con expectativas concretas. Esta matriz continúa el contrato ilustrativo de título actual → legado → fallback:

| Estado | Entrada | Resultado esperado |
| --- | --- | --- |
| Configurado | `title = "  Ruta nueva  "` | `Ruta nueva`. |
| Ausente | Sin `title` ni `heading` | `Untitled guide`. |
| Blanco | `title = "   "`, sin legado | `Untitled guide`. |
| Legado admitido | Sin título actual; `heading = "Ruta histórica"` | `Ruta histórica`. |
| Prioridad | Título actual y legado presentes | Gana el título actual. |

Una propiedad ausente y una cadena en blanco no son la misma entrada. Una prueba del primer caso puede pasar aunque la normalización del segundo esté rota.

Para contenido inválido, primero consulta el contrato de producción. Puede corresponder rechazar, normalizar o deshabilitar; una prueba no debe inventar una regla distinta sólo para conseguir verde.

El estado `isEmpty()` requiere su propia definición: si hay un título de respaldo, no deduzcas automáticamente que la tarjeta es renderizable. Prueba el contenido mínimo que el producto exige, por ejemplo un destino válido cuando éste sea parte del contrato.

Una prueba del getter demuestra el resultado Java, no el HTML final ni el placeholder de authoring. Para esos comportamientos necesitas evidencia de la vista. Base: [notas de la sesión, slides 6 y 7](../slides/lesson-19/speech.md).

<a id="servicio"></a>

## 7. Probar un servicio mediante activación

En el modelo, la frontera era la adaptación. En el servicio configurado, prepara dependencias y ejercita inyección y activación:

1. Registra los colaboradores que el componente requiere realmente.
2. Suministra las propiedades de un estado representativo.
3. Usa `registerInjectActivateService(...)` para inyectar, activar y registrar la implementación.
4. Recupera el servicio por su interfaz pública.
5. Comprueba el resultado de su capacidad o el fallo seguro definido.

Fragmento ilustrativo dentro de un test cuyo `context` ya está preparado:

```java
context.registerInjectActivateService(
    new GuideUrlServiceImpl(),
    "enabled", true,
    "baseUrl", "https://guides.example.test",
    "timeoutMs", 2000
);

GuideUrlService service = context.getService(GuideUrlService.class);
assertNotNull(service);
```

Los nombres son propiedades efectivas, sin los sufijos de tipo usados en `.cfg.json`. Aquí suministras valores Java como `boolean` e `int`. La API del servicio real determinará la llamada y aserción de comportamiento que deben seguir: **`assertNotNull` sólo prueba disponibilidad, no que la capacidad funcione**.

A diferencia de usar `new` como atajo en producción, aquí entregas el objeto al entorno mock para que procese su frontera OSGi. Los metadatos DS generados deben estar disponibles para que ese procesamiento conozca referencias y servicios. Registrar un objeto con `registerService` no es lo mismo que pedir su inyección y activación. [Registro y activación en AEM Mocks — wcm.io](https://wcm.io/testing/aem-mock/usage.html).

### Elige el fallo que corresponde

| Política del componente | Expectativa de prueba |
| --- | --- |
| Configuración válida | La operación pública devuelve el resultado esperado. |
| Capacidad opcional deshabilitada | El consumidor observa el estado deshabilitado documentado. |
| Configuración inválida que debe rechazarse | Falla la activación por esa razón específica. |
| Colaborador requerido ausente | Falla la preparación de esa dependencia, no una validación de URL. |

El helper puede envolver la excepción de activación según la versión de mocks. Comprueba el tipo y causa reales en vez de aceptar cualquier fallo como éxito.

Estos tests suministran propiedades ya preparadas: **no prueban la selección de `config.author.dev`, la interpolación de secretos de Cloud Manager ni el PID desplegado**. Esas evidencias operativas siguen el recorrido de la sesión 18. Usa datos ficticios, nunca secretos reales en fixtures.

<a id="dobles"></a>

## 8. Cuándo usar un doble de prueba

Detente en la opción más sencilla que represente honestamente la frontera:

| Opción | Cuándo usarla |
| --- | --- |
| Objeto real | Código barato y determinista que puede ejecutarse en memoria. |
| AEM Mocks | Recursos, modelos y OSGi dentro de las capacidades implementadas. |
| Stub pequeño o Mockito | Colaborador externo o no soportado por el contexto. |
| Prueba de integración | Dependencia de semántica real del repositorio, HTTP o runtime desplegado. |

Un stub de una API externa puede devolver una respuesta conocida para que el servicio real procese ese dato. Si simulas el propio `GuideUrlService` y luego compruebas el valor que tú le programaste devolver, no has probado su lógica.

Tampoco reemplaces todas las llamadas de un resolver por una larga cadena de mocks si AEM Mocks ya representa ese recurso. La prueba debe mostrar el estado y el contrato, no recrear cada paso de la implementación. Base: [notas de la sesión, slide 9](../slides/lesson-19/speech.md).

<a id="regresion"></a>

## 9. Red → green y comandos Maven

Una prueba verde aislada no demuestra que detecte el fallo que te preocupa. El recorrido de evidencia es:

```text
Contrato nombrado y contexto válido
    ↓
Comportamiento protegido ausente → fallo esperado (RED)
    ↓
Restaurar la implementación mínima
    ↓
Mismo test y misma entrada → éxito (GREEN)
    ↓
Suite completa de core
```

Desde la raíz del proyecto Maven AEM, con nombres ajustados a sus tests:

```sh
mvn -pl core -Dtest=GuideCardImplTest test
mvn -pl core '-Dtest=GuideCardImplTest#returnsFallbackWhenBothTitlesMissing' test
mvn -pl core test
```

La primera orden ejecuta la clase, la segunda el método concreto y la tercera amplía la comprobación a `core`. Las comillas evitan que el shell interprete caracteres del selector. La sintaxis de selección corresponde a [Maven Surefire](https://maven.apache.org/surefire/maven-surefire-plugin/examples/single-test.html).

Estos comandos pertenecen a tu proyecto AEM con POM y módulo `core`; este repositorio de materiales no proporciona por sí solo ese proyecto ejecutable. Reutiliza su configuración de build. Si faltan dependencias de otros módulos, resuelve ese requisito según el reactor del proyecto; no confundas descarga o compilación fallida con una regresión del modelo.

### Qué cuenta como rojo útil

Para la promesa del fallback, rojo útil significa que la aserción esperaba `Untitled guide` y obtuvo otro resultado al quitar ese comportamiento. No cuentan como esa prueba:

- JSON que no se puede cargar.
- Clase que no compila.
- Modelo que no se registra.
- Servicio requerido ausente.
- Maven que no ejecutó ningún test.

Si haces una retirada temporal del fallback, hazla en tu entorno de desarrollo y restáurala antes de terminar. No dejes ni publiques la regresión usada para demostrar el test. Tras recuperar verde, ejecuta la suite de `core` y registra cuántos tests corrieron realmente.

<a id="diagnostico"></a>

## 10. Diagnóstico y mapa de evidencias

Lee el primer fallo que explica la causa, no sólo el último `NullPointerException`.

| Síntoma | Qué revisar primero |
| --- | --- |
| No encuentra el fixture | Ruta de classpath y ubicación en `src/test/resources`. |
| No existe el recurso del caso | Raíz de carga JSON y ruta seleccionada. |
| No puede crear el modelo | Registro, adapter solicitado, adaptable e inyecciones. |
| Falla la activación del servicio | Metadatos DS, colaboradores y propiedades suministradas. |
| Aserción devuelve el dato equivocado | Contrato de prioridad, normalización y valor observado. |
| Sólo pasa después de otro test | Estado compartido, contenido o registros no aislados. |
| Maven termina bien pero no hay pruebas | Descubrimiento, nombres, filtros, skips y reporte de ejecución. |
| Pasa en mocks y falla en AEM | Diferencia de fidelidad o contexto que la prueba no representa. |

En proyectos que usan Surefire, consulta también `core/target/surefire-reports`. Un reporte útil conserva el nombre del test, resultado esperado y observado, comando y razón del rojo.

| Campo de evidencia | Qué registrar |
| --- | --- |
| Contrato | Promesa que el consumidor necesita. |
| Escenario | Contenido o configuración representativos. |
| Contexto | Recurso/request, modelos, servicios y resolver necesarios. |
| Operación | Getter o método público ejecutado. |
| Aserción | Resultado o fallo específico esperado. |
| Red | Cambio temporal y fallo que demuestra su detección. |
| Green | Restauración y resultado con el mismo comando. |
| Gate final | Suite de `core` y número de pruebas ejecutadas. |
| Límite | Lo que esta prueba no valida en el runtime real. |

**Criterio de preparación:** explicar por qué la prueba falla al quitar el comportamiento protegido, por qué pasa al restaurarlo y qué evidencia adicional necesitarías para confiar en el despliegue.

<a id="repaso"></a>

## 11. Repaso con respuestas

Contesta antes de desplegar las soluciones. Las preguntas son preparación personal y no sustituyen el cierre pasivo del deck.

<details>
<summary>1. ¿Qué protege una prueba útil de un Sling Model?</summary>
<p>Un valor o estado que su consumidor observa, como el título de respaldo o la condición vacía. No la distribución de campos privados.</p>
</details>

<details>
<summary>2. ¿Qué debe quedar explícito en Arrange, Act y Assert?</summary>
<p>El estado representativo, la operación real del contrato y el resultado esperado. El nombre del test debe ayudar a identificar la promesa que falló.</p>
</details>

<details>
<summary>3. ¿Por qué utilizar un contexto no estático gestionado por la extensión?</summary>
<p>Para facilitar preparación y limpieza independientes. No deberías depender del orden de ejecución ni del contenido dejado por otro test.</p>
</details>

<details>
<summary>4. ¿AEM Mocks demuestra que el bundle resuelve en el SDK?</summary>
<p>No. Representa fronteras de prueba en memoria, no toda la resolución de paquetes ni el despliegue real. Necesitas evidencia del runtime para esa afirmación.</p>
</details>

<details>
<summary>5. ¿Por qué ModelFactory ayuda a diagnosticar una creación fallida?</summary>
<p>Porque puede proporcionar una excepción de creación más concreta, en lugar de devolver null y provocar después una desreferencia que oculta la causa.</p>
</details>

<details>
<summary>6. ¿Una prueba de título ausente cubre también un título con espacios?</summary>
<p>No necesariamente. Son entradas distintas: el segundo caso requiere la normalización o validación definida por el contrato.</p>
</details>

<details>
<summary>7. ¿Registrar un objeto como servicio equivale a probar su activación?</summary>
<p>No. Usa la frontera de inyección y activación cuando ése es el comportamiento que debe ejercitarse, y después verifica la capacidad pública.</p>
</details>

<details>
<summary>8. ¿Un test verde prueba que detecta la regresión prevista?</summary>
<p>Por sí solo no. La evidencia red → green muestra que el test falla por el comportamiento ausente y pasa cuando se restaura.</p>
</details>

### Cuatro casos para identificar el fallo correcto

<details>
<summary>Caso A · El test del fallback falla porque no encuentra guide-card.json. ¿Es la regresión esperada?</summary>
<p>No. Falló la preparación. Corrige la ubicación y ruta del fixture antes de evaluar el comportamiento del modelo.</p>
</details>

<details>
<summary>Caso B · El servicio recibe baseUrl válida, pero falta un colaborador @Reference. ¿Has probado la validación de configuración?</summary>
<p>No. El componente todavía no supera su dependencia requerida. Registra el colaborador apropiado y luego aísla el caso de configuración que quieres comprobar.</p>
</details>

<details>
<summary>Caso C · Simulas getDisplayTitle para devolver el fallback y luego verificas ese mismo valor. ¿Qué lógica probaste?</summary>
<p>La respuesta configurada en tu doble, no el fallback del modelo real. Ejecuta el modelo de producción sobre contenido representativo.</p>
</details>

<details>
<summary>Caso D · La suite pasa, pero Author usa otra baseUrl al desplegar. ¿Qué evidencia falta?</summary>
<p>La selección e interpolación efectivas de configuración en ese tier. Una prueba con propiedades Java suministradas no valida los archivos por run mode ni las variables de Cloud Manager.</p>
</details>

Si necesitas ayuda, comparte el nombre del test, el contrato esperado y el primer fallo útil. Pregunta al agente si el problema corresponde a preparación, creación, comportamiento o al límite de los mocks; no compartas secretos del entorno.

<a id="fuentes"></a>

## 12. Glosario y fuentes

| Término | Definición de referencia |
| --- | --- |
| Unidad bajo prueba | Código real cuyo comportamiento se verifica. |
| Contrato observable | Resultado, estado o fallo que el consumidor puede percibir. |
| Fixture | Datos representativos que preparan un escenario. |
| Aserción | Comprobación de una expectativa. |
| Aislamiento | Independencia respecto al estado de otras pruebas. |
| AemContext | Contexto de prueba que ofrece fronteras AEM soportadas. |
| Stub | Colaborador controlado que devuelve resultados conocidos. |
| Regresión | Pérdida de un comportamiento que debía conservarse. |
| Red → green | Evidencia de detección del fallo y satisfacción posterior del contrato. |
| Surefire | Plugin Maven que ejecuta las pruebas unitarias en este flujo. |

**Lectura principal:** [AEM Mocks Usage — wcm.io](https://wcm.io/testing/aem-mock/usage.html). Prioriza JUnit 5, carga de contenido, registro de modelos y servicios. Conserva las versiones compatibles del POM de tu proyecto.

Fuentes de preparación, consultadas el 8 de septiembre de 2026:

- [Sesión 19 y diapositivas](../lessons/0019-junit-aem-mocks.html), [outline](../slides/lesson-19/outline.md) y [notas del presentador](../slides/lesson-19/speech.md).
- [Unit testing — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/getting-started-wknd-tutorial-develop/project-archetype/unit-testing): ejemplo de pruebas de un modelo WKND. Sus instrucciones de versiones corresponden al tutorial, no a una orden de cambiar tu proyecto.
- [Sling Mocks — Apache Sling](https://sling.apache.org/documentation/development/sling-mock.html): tipos de resolver y capacidades simuladas.
- [JUnit 5 User Guide](https://docs.junit.org/5.13.4/user-guide/): lifecycle, Jupiter y aserciones.
- [Running a Single Test — Maven Surefire](https://maven.apache.org/surefire/maven-surefire-plugin/examples/single-test.html): selección de clases y métodos.

**Alcance:** pruebas enfocadas de modelos y servicios con estado representativo. Los fragmentos son material de estudio para adaptar al proyecto AEM; esta guía no instala dependencias ni afirma haber ejecutado esos tests. La integración contra SDK, navegador o Dispatcher necesita su propia evidencia y no queda certificada por una prueba en memoria.

<a id="practica-local"></a>

## Práctica local · Probar el componente de la sesión 18 (20–30 min)

**Requisitos:** copia primero los archivos completos de la [práctica 18](session-18-study-guide.html#practica-local). El test usa esas clases reales, no `GuideCardImpl` ni interfaces que tengas que inventar. Conserva el mismo package en producción y pruebas.

Tu `core/pom.xml` debe tener JUnit Jupiter y `io.wcm:io.wcm.testing.aem-mock.junit5` con scope `test`, y Surefire con soporte JUnit 5. WKND/Archetype suelen gestionarlos desde el POM padre: reutiliza sus versiones. Si faltan, añade estas dependencias **dentro del bloque dependencies existente**, con versiones gestionadas compatibles con tu baseline; no copies un segundo bloque de proyecto ni actualices a ciegas las versiones del curso.

```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>io.wcm</groupId>
    <artifactId>io.wcm.testing.aem-mock.junit5</artifactId>
    <scope>test</scope>
</dependency>
```

El build de `core` debe generar los descriptores DS antes de las pruebas: `registerInjectActivateService` los usa para activar el servicio. Un error “No OSGi SCR metadata” es de preparación del build, no un fallo del fallback.


### Archivo: `core/src/test/java/com/adobe/aem/guides/wknd/core/training/TrainingMessageTest.java`

```java
package com.adobe.aem.guides.wknd.core.training;

import io.wcm.testing.mock.aem.junit5.AemContext;
import io.wcm.testing.mock.aem.junit5.AemContextExtension;
import org.apache.sling.api.resource.Resource;
import org.apache.sling.models.factory.ModelFactory;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

import static org.junit.jupiter.api.Assertions.assertEquals;

@ExtendWith(AemContextExtension.class)
class TrainingMessageTest {
    private final AemContext context = new AemContext();

    @Test
    void rendersAuthoredTitleAndConfiguredServiceMessage() {
        context.registerInjectActivateService(new TrainingMessage(), "message", "  Local Author  ");
        context.addModelsForClasses(TrainingMessageModel.class);
        Resource resource = context.create().resource("/content/training/message", "title", "  My guide  ");

        TrainingMessageModel model = context.getService(ModelFactory.class)
                .createModel(resource, TrainingMessageModel.class);

        assertEquals("My guide", model.getTitle());
        assertEquals("Local Author", model.getMessage());
    }

    @Test
    void usesFallbackWhenTitleIsMissingAndConfigurationIsBlank() {
        context.registerInjectActivateService(new TrainingMessage(), "message", "   ");
        context.addModelsForClasses(TrainingMessageModel.class);
        Resource resource = context.create().resource("/content/training/message");

        TrainingMessageModel model = context.getService(ModelFactory.class)
                .createModel(resource, TrainingMessageModel.class);

        assertEquals("Weekend Guides", model.getTitle());
        assertEquals("Welcome to Weekend Guides", model.getMessage());
    }
}
```

### Ejecutar y demostrar que detecta la regresión

Desde la raíz de tu proyecto AEM:

```sh
mvn -pl core -Dtest=TrainingMessageTest test
```

**Verde esperado:** dos pruebas, cero fallos y cero errores. La primera comprueba título y mensaje configurados, incluyendo trim; la segunda combina título ausente y configuración vacía. `ModelFactory.createModel` conserva el diagnóstico si falta una inyección obligatoria.

1. En `TrainingMessage.activate`, sustituye temporalmente la asignación con fallback por `message = value.trim();`. No cambies el test.
2. Ejecuta sólo la segunda prueba:

```sh
mvn -pl core '-Dtest=TrainingMessageTest#usesFallbackWhenTitleIsMissingAndConfigurationIsBlank' test
```

3. **Rojo esperado:** la aserción del mensaje espera `Welcome to Weekend Guides` y recibe una cadena vacía. Un error de compilación o de activación no cuenta como ese rojo.
4. Restaura la asignación original y ejecuta ambos tests; después ejecuta la suite de `core`:

```sh
mvn -pl core -Dtest=TrainingMessageTest test
mvn -pl core test
```

**Aceptación:** guarda el fallo de aserción y el resultado verde con el mismo test, más una explicación de dos frases sobre el contrato. No dejes el cambio roto en el source code.

**Límite:** AEM Mocks comprueba adaptación, activación y salida Java; no valida render HTL, selección de run modes, instalación del ZIP ni publicación. La página de la sesión 18 aporta la comprobación visual. No hace falta arrancar AEM para estos tests.

Fuente: [uso de AEM Mocks y JUnit 5](https://wcm.io/testing/aem-mock/usage.html).
