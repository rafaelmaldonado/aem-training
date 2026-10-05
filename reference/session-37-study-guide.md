# Sesión 37 · Leer un fallo de pipeline

**Martes 6 de octubre de 2026 · Semana 8 · Núcleo de 30 minutos, ampliable a 60**

[Versión HTML](session-37-study-guide.html) · [Slides en inglés](../lessons/0037-pipeline-failure.html#slide-deck)

## Objetivo

Leer una ficha de ejecución y nombrar **el primer error accionable**, la etapa y el ambiente afectados, y una recuperación compatible con el estado del código y el contenido. Todos los identificadores, logs y resultados de pipeline de esta guía son **ejemplos didácticos inventados**. No se necesita Cloud Manager ni despliegue; JaCoCo es una demostración local opcional del instructor, sin ejercicio para participantes.

## Recorrido de 30 minutos

| Minutos | Slides | Explicación |
| --- | --- | --- |
| 0–6 | 1–2 | Presentar la ruta y localizar la primera etapa fallida. |
| 6–11 | 3 | Leer un error de build y sus mensajes derivados. |
| 11–20 | 4–5 | Relacionar code quality con un reporte local de JaCoCo. |
| 20–25 | 6 | Leer un fallo de prueba en stage. |
| 25–28 | 7–8 | Compatibilidad entre versiones y recuperación. |
| 28–30 | 9 | Preguntas y cierre. |

En 60 minutos, dedica el tiempo adicional a mostrar el reporte local de JaCoCo y a recorrer lentamente los ejemplos de build y stage. No se asigna ninguna actividad.

## 1. Leer la ejecución por etapas

La vista de una pipeline productiva full-stack puede incluir validación, build y pruebas unitarias, análisis de código, creación de imágenes, despliegue a stage, pruebas en stage, aprobación y despliegue a producción. Las etapas y gates concretos dependen del tipo y configuración de la pipeline: **el diagrama de los slides es una simplificación para leer un fallo, no una secuencia universal**. Las reglas de seguridad de código se evalúan dentro de code quality; en AEM as a Cloud Service no hay una etapa explícita de security testing. Una pipeline de calidad no despliega. Las pruebas funcionales, de UI y las auditorías están asociadas al flujo full-stack según su configuración. [Desplegar código — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/deploy-code) · [Code quality testing — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/test-results/code-quality-testing).

Para leer un run, registra en este orden: **SHA y origen** de la sesión 36 → **primera etapa con fallo o pausa** → **primera línea que explica una causa** → **etapas no alcanzadas** → **ambiente que sí recibió el artefacto**. No atribuyas a producción un fallo ocurrido antes de desplegar allí. El resumen rojo suele ser menos útil que el log o informe de la etapa concreta.

| Frontera | Evidencia útil | Conclusión limitada |
| --- | --- | --- |
| Build | Error de compilación, dependencia o empaquetado; log del primer fallo | No hay artefacto válido de ese run. |
| Calidad, incluidos hallazgos de seguridad | Regla, componente afectado, severidad y estado del gate | Una pausa o fallo del gate no demuestra despliegue. |
| Pruebas | Nombre, petición, dato de entrada, esperado y obtenido | Se conoce el comportamiento fallido en el ambiente probado. |
| Despliegue | Artefacto, ambiente, paso y error de instalación o salud | Se delimita qué ambiente llegó a actualizarse y cuál no. |

Adobe distingue incidencias **critical**, que detienen la pipeline; **important**, que pueden pausarla y sujetarse a la decisión autorizada; e **info**, que sólo se informa. La decisión concreta debe leerse en el gate del run; no se omite una incidencia por conveniencia. [Code quality testing — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/test-results/code-quality-testing).

### Ver cobertura con JaCoCo en un proyecto local

**Ejemplo opcional para el instructor, no ejercicio:** en el módulo Java `core` de un proyecto AEM Maven se puede declarar el plugin JaCoCo en `core/pom.xml`:

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.15</version>
</plugin>
```

Desde `core/`, con las dependencias Maven disponibles, **una sola invocación** prepara el agente, ejecuta las pruebas y genera el reporte:

```sh
mvn jacoco:prepare-agent test jacoco:report
```

Abrir `core/target/site/jacoco/index.html` desde la raíz del proyecto permite ver líneas y ramas ejecutadas por las pruebas. Los porcentajes mostrados en la lámina 5 son ficticios. La cobertura local **no reproduce todo el gate de Cloud Manager**: Adobe combina cobertura de líneas y condiciones en su propia métrica y además evalúa reglas de código y paquetes. Una línea marcada como cubierta tampoco demuestra que el test haya comprobado el comportamiento correcto; conviene inspeccionar ramas omitidas y aserciones. Si el proyecto ya configura `argLine` en Surefire, debe conservar el argumento del agente de JaCoCo al ejecutar tests. Cloud Manager invoca `prepare-agent` en su build; el ejemplo local sólo sirve para entender la evidencia de cobertura. [JaCoCo Maven plugin](https://www.jacoco.org/jacoco/trunk/doc/maven.html) · [prepare-agent](https://www.jacoco.org/jacoco/trunk/doc/prepare-agent-mojo.html) · [Build de Cloud Manager — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/create-application-project/build-environment-details) · [Code quality — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/test-results/code-quality-testing).

## 2. Ejemplo: un build que nunca produjo artefacto

**Log ficticio, abreviado:**

```text
[ERROR] Could not resolve com.example:site-core:jar:1.4.2
[ERROR] Failed to execute goal
Tests skipped
```

La primera línea explica la causa investigable: falta resolver una dependencia concreta. “Failed to execute goal” resume la caída; “Tests skipped” es una consecuencia. La revisión se dirige a coordenadas, versión y repositorio de dependencias declarados para ese commit. Como el build no terminó, esta ficha **no prueba** que el código haya llegado a stage o producción. Tampoco autoriza a concluir que las pruebas fallaron.

## 3. Ejemplo: fallan pruebas después de desplegar a stage

**Ficha ficticia de run `#43`, distinta del run `#42` de la sesión 36:**

| Etapa | Estado de ejemplo |
| --- | --- |
| Build y code quality, incluidos sus hallazgos de seguridad | Superados en la ficha. |
| Despliegue a stage | Completado. |
| Prueba funcional en stage | `GET /content/site/en.html`: esperado `200`, obtenido `404`. |
| Despliegue a producción | No iniciado. |

El primer error accionable de esta ficha es la **aserción de la prueba en stage**. El `404` todavía no identifica la causa: puede ser una URL de prueba equivocada, contenido ausente/no publicado, una regla de la capa web o código que no entrega la ruta prevista. Para distinguirlas se compararían la URL y el Host de la prueba, el contenido disponible en stage, el artefacto de ese SHA y la respuesta/logs en la capa que devuelve el `404`. La decisión inmediata es corregir la causa verificada y volver a validar el run; no describirlo como un fallo de build ni como un despliegue productivo.

## 4. Compatibilidad durante la actualización

En AEM as a Cloud Service, un despliegue gradual puede mantener **código antiguo y nuevo activos a la vez** mientras comparten contenido mutable. Además, volver al código anterior no deshace automáticamente los cambios de contenido mutable. Por eso, un cambio que renombra un campo de contenido debe planearse para que ambas versiones toleren el estado que puedan encontrar. [Despliegue gradual y compatibilidad — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/overview).

**Ejemplo didáctico:** una tarjeta leía `old_field` y ahora leerá `new_field`.

1. **Versión A:** el lector acepta ambos campos y conserva el comportamiento anterior. Se verifica con contenido antiguo y con contenido que ya tenga el nuevo campo.
2. **Versión B:** después de que A esté operativa, el productor empieza a escribir `new_field`, sin eliminar inmediatamente la lectura de `old_field`.
3. **Limpieza posterior:** sólo se retira el soporte antiguo cuando se haya comprobado que ya no es necesario para contenido existente ni para una posible reversión del código.

La secuencia es un patrón de diseño para el ejemplo, no una afirmación de que Cloud Manager migre los campos. Si el contenido ya quedó en una forma incompatible con el código anterior, restaurar sólo el código puede reintroducir el fallo.

## 5. Elegir la recuperación según la frontera

| Situación ilustrativa | Siguiente decisión |
| --- | --- |
| Fallo antes de crear el artefacto | Corregir la causa del build o gate y validar una nueva ejecución. |
| Fallo en prueba de stage | Inspeccionar la evidencia de stage y corregir la causa verificada antes de considerar producción. |
| Fallo durante el despliegue | Confirmar el paso y ambiente afectados; revisar el estado real antes de reintentar. |
| Problema tras llegar a producción | Contener el impacto y valorar el mecanismo de restauración de código disponible para ese ambiente, comprobando por separado el contenido mutable. |

Adobe documenta **Restore previous code deployed** para regresar al último build exitoso cuando se cumplen sus condiciones. Esa opción restaura código; **no revierte el contenido mutable**. Una recuperación concreta depende del ambiente y de la evidencia del incidente; esta guía no presupone acceso ni ejecuta esa operación. [Restaurar código anterior — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/restore-previous-code-deployed) · [Despliegue y contenido mutable — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/overview).

## Método de lectura en una frase

“El run del SHA indicado llegó hasta **[etapa/ambiente]**; el primer error explicativo es **[dato del log o informe]**; **[etapas posteriores]** no se completaron; la siguiente acción es **[corrección o inspección verificable]**, manteniendo compatibles código y contenido”.

## Fuentes oficiales

- [Deploy your code — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/deploy-code)
- [Code quality testing — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/test-results/code-quality-testing)
- [JaCoCo Maven plugin](https://www.jacoco.org/jacoco/trunk/doc/maven.html)
- [Deploying to AEM as a Cloud Service — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/overview)
- [Restore previous code deployed — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/operations/restore-previous-code-deployed)
