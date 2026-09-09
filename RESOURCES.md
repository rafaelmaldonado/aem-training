# AEM Training Resources

## Knowledge

- [AEM as a Cloud Service documentation — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service)
  Fuente principal para arquitectura, desarrollo, seguridad, operación y cambios actuales del producto.
- [Introduction to AEM as a Cloud Service — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/overview/introduction)
  Explica el modelo cloud-native, actualizaciones continuas, escalamiento y responsabilidades del equipo.
- [AEM as a Cloud Service architecture — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/overview/architecture)
  Fuente para distinguir Author, Replication Service, Publish, código inmutable y pipelines de despliegue.
- [Content Delivery Flow — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/overview)
  Secuencia oficial Browser → CDN → Dispatcher → Publish y decisiones de caché usadas en la primera lección.
- [AEM as a Cloud Service onboarding journey — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/onboarding/journey/overview)
  Útil para acceso, ambientes y para distinguir Publish Delivery de Edge Delivery Services.
- [AEM as a Cloud Service SDK — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/aem-as-a-cloud-service-sdk)
  Referencia para Quickstart, API Jar, Dispatcher Tools y desarrollo local.
- [Local Development Environment for AEM as a Cloud Service — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/overview)
  Secuencia oficial para herramientas, runtime local y Dispatcher Tools.
- [Set up the local AEM SDK — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/aem-runtime)
  Instrucciones actuales para JDK, descarga del SDK y servicios Author/Publish locales.
- [Cloud Manager build environment — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/create-application-project/build-environment-details)
  Referencia teórica para las versiones administradas y el modelo de build; el curso no requiere acceso a Cloud Manager.
- [Oracle JDK 21.0.12 release notes — Oracle](https://www.oracle.com/java/technologies/javase/21-0-12-relnotes.html)
  Versión local exacta del curso: Oracle JDK 21.0.12+7.
- [Node.js 24.18.1 release files — Node.js](https://nodejs.org/download/release/v24.18.1/)
  Baseline frontend del curso; incluye npm 11.16.0.
- [Apache Maven 3.9.4 binaries — Apache](https://archive.apache.org/dist/maven/maven-3/3.9.4/binaries/)
  Binarios de la misma versión documentada para Cloud Manager.
- [AEM Sites project setup — Adobe WKND tutorial](https://experienceleague.adobe.com/en/docs/experience-manager-learn/getting-started-wknd-tutorial-develop/project-archetype/project-setup)
  Referencia para módulos Maven, build e instalación local de un proyecto tradicional.
- [AEM Core Components — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/introduction)
  Base para componentes authorables del stack tradicional y patrón proxy.
- [WKND tutorial — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/getting-started-wknd-tutorial-develop/overview)
  Tutorial práctico oficial para contrastar el proyecto del curso con una implementación conocida.
- [WKND full-stack repository — Adobe](https://github.com/adobe/aem-guides-wknd)
  Base del proyecto de mantenimiento. Fijar un commit de la rama principal y trabajar sobre un fork o repositorio individual.

## Session 16 · Java, OSGi and Resource API

- [Java API Best Practices in AEM — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/foundation/development/understand-java-api-best-practices)
  Lectura principal: selección de APIs AEM, Sling, JCR y OSGi y ejemplos de adaptación.
- [Declarative Services — OSGi](https://docs.osgi.org/specification/osgi.cmpn/8.1.0/service.component.html)
  Componentes, referencias, descriptores y activación diferida.
- [Life Cycle Layer — OSGi](https://docs.osgi.org/specification/osgi.core/8.0.0/framework.lifecycle.html)
  Estados y ciclo de vida de bundles.
- [Web Console — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developer-tools/web-console)
  Inspección local y distinción respecto de Developer Console cloud.
- [Resource — Apache Sling](https://sling.apache.org/apidocs/sling12/org/apache/sling/api/resource/Resource.html)
  Contrato de recursos, propiedades, hijos y adaptación.
- [ValueMap — Apache Sling](https://sling.apache.org/apidocs/sling12/org/apache/sling/api/resource/ValueMap.html)
  Lectura tipada y valores predeterminados.
- [ResourceResolver — Apache Sling](https://sling.apache.org/apidocs/sling12/org/apache/sling/api/resource/ResourceResolver.html)
  Acceso a recursos, ciclo de vida y concurrencia.

Consultadas el 5 de septiembre de 2026. Estas referencias explican contratos; las dependencias del proyecto determinan las versiones de las APIs del SDK.

## Session 17 · Sling Models, delegation and JSON

- [Apache Sling Models](https://sling.apache.org/documentation/bundles/models.html)
  Lectura principal: adaptables, registro, inyección, opcionalidad, selección por resource type y exporter.
- [Customizing Core Components — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/customizing)
  Proxy y delegación del contrato público para extender comportamiento.
- [Core Components Guidelines — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/guidelines)
  Separación entre lógica en Sling Models y markup en HTL.
- [Understand Sling Model Exporter — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/foundation/development/understand-sling-model-exporter)
  Reutilización del contrato de un modelo para una representación JSON.
- [Develop Sling Model Exporter — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/foundation/development/develop-sling-model-exporter)
  Exporter, opciones y anotaciones de Jackson para controlar la representación.

Consultadas el 5 de septiembre de 2026. Las dependencias del proyecto determinan las APIs y variantes de request compatibles con el SDK.

## Session 18 · OSGi configuration and servlet boundaries

- [Configuring OSGi for AEM as a Cloud Service — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi)
  Lectura principal: archivos por PID, run modes, interpolación y valores efectivos.
- [Environment Variables — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/environment-variables)
  Valores no sensibles y secretos por entorno y tier.
- [Metatype — OSGi](https://docs.osgi.org/specification/osgi.cmpn/8.1.0/service.metatype.html)
  Definición tipada del contrato operativo.
- [Servlets and Scripts — Apache Sling](https://sling.apache.org/documentation/the-sling-engine/servlets.html)
  Registro por recurso y resolución de métodos, selectores y extensiones.

Consultadas el 8 de septiembre de 2026. Complementar con la referencia DS de la sesión 16 para distinguir activación inicial y modificación; una excepción de modificación no garantiza rollback.

## Session 19 · JUnit 5 and AEM Mocks

- [AEM Mocks Usage — wcm.io](https://wcm.io/testing/aem-mock/usage.html)
  Lectura principal: contexto JUnit 5, contenido, registro de modelos y activación de servicios.
- [Unit testing — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/getting-started-wknd-tutorial-develop/project-archetype/unit-testing)
  Ejemplo WKND de fixtures y pruebas de modelos; no trasladar sus versiones históricas automáticamente al proyecto.
- [Sling Mocks — Apache Sling](https://sling.apache.org/documentation/development/sling-mock.html)
  Tipos de resolver y límites de la frontera simulada.
- [JUnit 5 User Guide](https://docs.junit.org/5.13.4/user-guide/)
  Referencia versionada de Jupiter, lifecycle y aserciones; conservar las dependencias compatibles del proyecto.
- [Running a Single Test — Maven Surefire](https://maven.apache.org/surefire/maven-surefire-plugin/examples/single-test.html)
  Selección de clases y métodos para el ciclo de regresión.

Consultadas el 8 de septiembre de 2026. Los tests de mocks no certifican despliegue, resolución real de bundles, configuración cloud ni Dispatcher.

## Session 21 · Multi-Site Management foundations

- [Reusing Content: Multi Site Manager and Live Copy — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/overview)
  Lectura principal: vocabulario, relaciones, language masters y Live Copies.
- [Creating and Synchronizing Live Copies — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/creating-live-copies)
  Herencia, Synchronize, Rollout, Resume, Reset y efectos de Detach.
- [Configuring Live Copy Synchronization — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/live-copy-sync-config)
  Configuración efectiva, triggers y acciones de sincronización.
- [Live Copy Overview Console — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/live-copy-overview)
  Inspección de la estructura y estado de las relaciones.
- [MSM Best Practices — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/best-practices)
  Mantenimiento y límites de sincronización automática.
- [Multi Site Manager and Translation — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm-and-translation)
  Separación de reutilización MSM y traducción de contenido.

Consultadas el 8 de septiembre de 2026. Reanudar herencia y sincronizar son decisiones distintas; comprobar alcance y diferencias locales antes de Reset o Detach.

## Wisdom (Communities)

- [Experience League Community: Adobe Experience Manager](https://experienceleaguecommunities.adobe.com/t5/adobe-experience-manager/ct-p/adobe-experience-manager-community)
  Para contrastar decisiones, investigar problemas reales y practicar preguntas técnicas de calidad.

## Scope guardrails

- La plataforma confirmada es AEM Sites tradicional sobre AEM as a Cloud Service y el equipo tiene acceso al SDK.
- Añadir sólo las fuentes específicas de Edge Delivery, Headless, Assets o Forms que el alcance confirmado requiera.

## Sesiones 20 y 22 · Preparación y práctica local

- [Sesión 20: revisión de backend](reference/session-20-study-guide.html) y [sesión HTML](lessons/0020-backend-practice-review.html); revisión semanal sin slides.
- [Sesión 22: estructura compatible con Cloud](reference/session-22-study-guide.html), [Markdown](reference/session-22-study-guide.md) y [slides + práctica](lessons/0022-cloud-compatible-structure.html).
- Las sesiones 18–22 incluyen prácticas locales en sus HTML; los archivos copiables están en `reference/examples/session-18`, `session-19` y `session-22`.
