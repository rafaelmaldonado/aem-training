# Ejemplos locales · Sesiones 18–22

Copia los archivos dentro de **tu proyecto AEM**, conservando las rutas relativas. Este repositorio de formación no contiene un reactor Maven AEM.

- `session-18`: servicio OSGi, Sling Model, definición de componente, diálogo, HTL y configuración Author. Instrucciones y archivos completos: [guía 18](../session-18-study-guide.html#practica-local).
- `session-19`: prueba JUnit 5/AEM Mocks del código anterior. [Guía 19](../session-19-study-guide.html#practica-local).
- `session-22`: payload y metadatos de un ZIP FileVault mínimo sobre `/content/aem-training-package-lab`. [Guía 22](../session-22-study-guide.html#practica-local).
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

Estas versiones documentan la comprobación, no una instrucción para actualizar tu baseline. Los pasos de instalación, autoría, configuración efectiva, MSM e importación de los tres modos quedan para ejecutarse en tu SDK; no se presentan como observados aquí.

Desde la raíz del repositorio de formación, `python3 scripts/check-session-materials.py` comprueba enlaces locales, anclas, las 12 imágenes y que los bloques copiables de las guías y lecciones coincidan con los archivos fuente.
