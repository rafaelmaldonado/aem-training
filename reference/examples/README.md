# Ejemplos locales · Sesiones 18–46 y práctica 9

Copia los archivos dentro de **tu proyecto AEM**, conservando las rutas relativas. Este repositorio de formación no contiene un reactor Maven AEM.

- `session-18`: servicio OSGi, Sling Model, definición de componente, diálogo, HTL y configuración Author. Instrucciones y archivos completos: [guía 18](../session-18-study-guide.html#practica-local).
- `session-19`: prueba JUnit 5/AEM Mocks del código anterior. [Guía 19](../session-19-study-guide.html#practica-local).
- `session-22`: payload y metadatos de un ZIP FileVault mínimo sobre `/content/aem-training-package-lab`. [Guía 22](../session-22-study-guide.html#practica-local).
- `session-23`: una sola clase `LogPayloadProcess`, que registra el payload de un workflow. [Código completo y pasos para logger y modelo en Author](../session-23-study-guide.html#ejemplos-locales).
- `session-28`: Repo Init para el árbol, grupo, service user y ACL utilizados por las sesiones 28 y 29. [Guía 28](../session-28-study-guide.html#ejemplos-locales).
- `session-29`: mapping por principal, lector OSGi con resolver propio y una prueba de ownership. [Guía 29](../session-29-study-guide.html#ejemplos-locales).
- `session-41`: launcher, workflow y Sling Job sobre dos Guides, con `FAILED` controlado, reintento y replay en Author SDK local. [Archivos y demo](session-41/README.md).
- `session-42`: servicio OSGi y Process Step para una llamada HTTP saliente con timeouts, clasificación y stub local. [Archivos y demo](session-42/README.md).
- `assets-jpeg-800`: guía HTML con el XML y las rutas de un Processing Profile, más pasos de `aio` para un worker personalizado. [Abrir guía](assets-jpeg-800/GUIDE.html).
- `session-46`: test completo de la sesión 19 con un caso adicional para el título compuesto sólo por espacios. [Guía 46](../session-46-study-guide.html).
- `week-9`: [solución interna del instructor](week-9/README.md) que extiende tres archivos ya entregados en la sesión 41 para crear 300 Guides en lotes, reintentar y evitar duplicados. Los participantes no reciben archivos nuevos.
- Las sesiones [20](../session-20-study-guide.html#practica-local) y [21](../session-21-study-guide.html#practica-local) describen acciones en la instancia.

Los ejemplos usan el package y rutas de WKND Sites tradicional. Para Archetype, sigue las sustituciones de prefijo de la guía 18; conserva las versiones y los plugins compatibles con tu baseline.

## Validación realizada

El Java y el HTL se comprobaron en un proyecto Maven temporal aislado, sin modificar ni instalar nada en el proyecto AEM del alumno:

- JDK 21, source/target Java 11; Maven 3.6.3.
- AEM SDK API `2025.4.20626.20250425T133017Z-250400`.
- AEM Mocks `4.1.8`, JUnit Jupiter `5.8.2`, Surefire `3.2.5`.
- Bnd `5.1.2` generó metadatos DS; HTL Maven Plugin `2.0.2-1.4.0` validó y transpiló el script, y la clase generada compiló.
- `TrainingMessageTest`: dos pruebas pasan. Al retirar temporalmente el fallback del mensaje, la prueba correspondiente falla por aserción; al restaurarlo, ambas pasan.
- El ZIP FileVault se construyó con el comando `jar` documentado y se inspeccionaron sus rutas. XML y JSON son sintácticamente válidos.
- Sesión 23: `LogPayloadProcess.java` compiló con la misma API SDK y versión Java indicadas arriba; Bnd generó el descriptor DS con la interfaz `WorkflowProcess` y la etiqueta `Training: log payload`. Los pasos del logger y workflow quedan para ejecutarse en el SDK local.
- Sesión 29: `TrainingGuideReader` y sus dos pruebas compilaron con AEM SDK API `2025.3.19823.20250304T101418Z-250300`; las pruebas comprueban el subservice y el cierre del resolver propio frente al prestado. La ACL efectiva y el resultado en Author quedan para el SDK local.
- Sesión 41: `QueueGuidesProcess` y `GuideBatchJobConsumer` compilaron con la misma API SDK; la prueba JUnit de fallo, reanudación y replay pasó (1 prueba, 0 fallos). Tres configuraciones JSON son válidas. La integración con launcher, workflow y cola queda para el Author SDK local.
- Sesión 42: `ExternalStatusService` y `ProbeExternalStatusProcess` compilaron con AEM SDK API `2025.3.19823.20250304T101418Z-250300`; Bnd generó los componentes y el metatype con clave tipo Password. La prueba JUnit de 200, 401, 503, timeout y URL inválida pasó (1 prueba, 0 fallos). El stub local respondió como se documenta; la integración en Author queda para el SDK local.
- Sesión 46: `TrainingMessageTest` compiló con Java 11, AEM SDK API `2025.3.19823.20250304T101418Z-250300`, AEM Mocks `4.1.8` y metadatos DS generados con Bnd. Pasaron los tres casos. Al retirar temporalmente la condición para títulos sólo con espacios, la prueba nueva falló por aserción con esperado `Weekend Guides` y actual cadena vacía; el modelo de referencia quedó intacto. La petición HTTP y los permisos efectivos quedan para el SDK local.
- Práctica 9: el Process Step de la sesión 41 y el consumidor extendido compilaron con Java 11 y AEM SDK API `2025.3.19823.20250304T101418Z-250300`. La prueba de 300 nodos, checkpoint en 100, reanudación y replay pasó en un ejecutor local; Maven compiló la prueba, pero Surefire no pudo ejecutarla sin una dependencia del plugin ausente en la caché. Repo Init es JSON válido. La instalación y el launcher/modelo quedan por verificar en Author SDK local.

Estas versiones documentan la comprobación, no una instrucción para actualizar tu baseline. Los pasos de instalación, autoría, configuración efectiva, MSM e importación de los tres modos quedan para ejecutarse en tu SDK; no se presentan como observados aquí.

Desde la raíz del repositorio de formación, `python3 scripts/check-session-materials.py` comprueba enlaces locales, anclas, las imágenes disponibles y que los bloques copiables de las guías y lecciones coincidan con los archivos fuente.
