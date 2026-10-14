# Sesión 44 · Evolucionar un modelo CF sin romper consumidores

**Jueves 15 de octubre de 2026 · Semana 9 · 30 minutos**

[Versión HTML](session-44-study-guide.html) · [Slides en inglés](../lessons/0044-content-fragment-model-evolution.html#slide-deck) · [Fundamentos CF de la sesión 24](session-24-study-guide.md)

## Objetivo observable

En una rama de práctica de Author SDK, añadir una referencia a una imagen y otra a un Content Fragment sin cambiar el campo que ya consume una página Sites. Comprobar qué ocurre con un fragmento existente que aún no tiene valores para los campos nuevos, limitar la profundidad del modelo y enumerar las dependencias que habría que publicar.

La sesión 24 separó modelo, fragmento y componente. Esta sesión parte de **un consumidor ya configurado**: la página muestra `summary` de un Guide. El cambio añade relaciones para una futura presentación, pero la página actual debe seguir mostrando el mismo resumen. Los resultados son predicciones hasta ejecutarlos en tu SDK.

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–4 | 1–2 | Caso, fragmentos y página consumidora. |
| 4–8 | 3–4 | Contrato actual y dos tipos de referencia. |
| 8–14 | 5–6 | Cambio aditivo y fragmento anterior sin valores nuevos. |
| 14–20 | 7–8 | Profundidad y comprobación real del componente Sites. |
| 20–25 | 9–10 | Publicación y diagnóstico. |
| 25–29 | 11 | Decisiones clave y repaso. |
| 29–30 | 12 | Preguntas. |

## El caso y el contrato

Prepara una carpeta de Assets de práctica, una página de práctica y dos modelos independientes. `Training guide 44` empieza con un campo **Multi line text** cuyo nombre de propiedad es `summary`. `Training gear 44` tiene un campo **Single line text** llamado `name`. Crea `River walk` con `summary = Bring water.` y `Daypack` con `name = Daypack`. En la página `guide-44-lab` coloca el Core Component **Content Fragment**, selecciona `River walk`, el modo **Single Text Element**, el elemento `summary` y la variación Main/Master. Anota el texto renderizado. El nombre de la variación depende del editor.

```text
guide-44-lab (página Sites)
    └── Content Fragment component → River walk.summary

River walk (CF) → Training guide 44 (modelo)
Daypack (CF)    → Training gear 44 (modelo)
```

La referencia del componente sale de la página hacia el CF. Los nuevos campos del modelo no cambian por sí solos qué elemento eligió el componente. Adobe documenta que el Core Component permite seleccionar fragmento, modo, elementos y variación. [Adobe: Content Fragment Component](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/wcm-components/content-fragment-component).

## Dos referencias, dos destinos

Agrega al modelo `Training guide 44` estos campos **opcionales** y conserva `summary` con el mismo nombre y tipo:

| Propiedad | Tipo | Destino del caso | Para qué sirve |
| --- | --- | --- | --- |
| `heroImage` | Content Reference | Imagen bajo la carpeta de Assets de práctica | Enlaza otro recurso AEM; restringe el tipo a imagen. |
| `gear` | Fragment Reference | CF `Daypack`, del modelo `Training gear 44` | Enlaza contenido estructurado de otro modelo. |

**Content Reference** puede apuntar a otros tipos de contenido, como imágenes, páginas o Experience Fragments. **Fragment Reference** selecciona Content Fragments de los modelos permitidos. Define en `gear` el modelo permitido `Training gear 44` y una ruta raíz que incluya la carpeta de práctica. Evita una referencia de vuelta de Gear a Guide: este ejemplo sólo necesita un salto. La protección contra referencias recursivas no convierte una jerarquía profunda en una buena decisión de diseño. [Adobe: definir Content Fragment Models](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/content-fragments/content-fragment-models#using-references-to-form-nested-content).

El CF `River walk`, creado antes del cambio, puede tener `heroImage` y `gear` sin valor hasta que un autor los complete. Abrirlo y comprobar los campos es parte de la demo; **no se declara una migración automática**. Una nueva validación obligatoria o un cambio de nombre/tipo en `summary` merece revisión de todos los fragmentos y consumidores. Adobe advierte que las modificaciones de modelo afectan fragmentos dependientes y que renombrar o borrar campos puede romper consumidores que los solicitan. Aunque GraphQL no es la vía de esta clase, es una razón adicional para preservar el contrato. [Adobe: modelos y cambios de campos](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/assets/content-fragments/content-fragments-models).

## Demo local · Author SDK

**Preparación previa del instructor, fuera de los 30 minutos:** Author SDK con permisos para modelos, Assets y páginas; Content Fragment Models habilitados en una configuración de práctica; una carpeta Assets con ese modelo permitido mediante Policies; Core Component Content Fragment permitido en el template. Si la sesión 24 ya dejó un setup de laboratorio, úsalo como patrón, pero crea modelos y contenidos de la 44 en una rama desechable para no modificar los compartidos. En el SDK local, usa Tools/Assets según la interfaz disponible; Adobe mantiene más de una consola y editor. [Adobe: habilitar y permitir modelos](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/assets/content-fragments/content-fragments-models) · [Adobe: dos editores de CF](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/content-fragments/authoring).

1. Crea `Training gear 44` con `name`, y `Training guide 44` con `summary`. Habilita los modelos y permítelos sólo en la carpeta Assets de práctica. Crea `Daypack` y `River walk` con los valores indicados. Usa un asset de imagen de esa carpeta; anota su ruta real.
2. Crea `guide-44-lab` en un sitio de práctica. Añade el Core Component Content Fragment, selecciona `River walk`, **Single Text Element → summary**, y registra `Bring water.`. Si tu versión ofrece otra etiqueta para la variación principal, registra cuál usa.
3. Abre `Training guide 44`. Sin tocar `summary`, añade `heroImage` como **Content Reference** de imagen y `gear` como **Fragment Reference** que permita el modelo `Training gear 44`. Guarda. No marques nuevos campos como obligatorios en esta demostración.
4. Reabre `River walk` y observa los campos nuevos antes de asignar valores. Registra si están vacíos. Después selecciona el asset en `heroImage` y `Daypack` en `gear`. Guarda o espera el autosave según el editor. Comprueba que `summary` sigue siendo `Bring water.`.
5. Abre la página y su configuración. Verifica que el Content Fragment Component aún apunta a `River walk.summary` y que la página sigue mostrando `Bring water.`. Los campos nuevos existen en el CF, pero **no aparece una ficha de Gear ni una imagen por el mero cambio del modelo**. Mostrar esos datos requeriría configurar un consumidor que los represente; queda fuera de esta sesión.
6. Dibuja la cadena de dependencias. Si hay Publish local y deseas comprobarlo, publica los dos modelos, los dos CF, la imagen y la página según lo que muestre el asistente de referencias, y comprueba el resultado en Publish. Registra qué elementos fueron incluidos automáticamente y cuáles requirieron selección. Si no hay Publish, la cadena es un plan, no una comprobación ejecutada.

| Evidencia | Antes | Después esperado en Author |
| --- | --- | --- |
| `summary` de `River walk` | `Bring water.` | Igual. |
| `heroImage` y `gear` | No existen en el modelo | Existen; vacíos en el CF anterior hasta asignarles valores. |
| Componente de página | `River walk.summary` | Misma selección y mismo texto visible. |
| Referencias del CF | Modelo Guide | Modelo Guide, imagen y `Daypack`; este último depende del modelo Gear. |

**Limpieza:** guarda evidencia y elimina únicamente la página, carpeta Assets y modelos creados para el laboratorio. Verifica primero que no estén compartidos por otros ejemplos.

## Profundidad y consumo en Sites

La cadena útil aquí es **página → Guide → Gear**, con una imagen que sale de Guide. Añadir Gear → Supplier → Region sin un consumidor que lo necesite agranda la autoría, el rastreo de referencias y la revisión de publicación. El modelo establece relaciones, pero no implementa una UI de página que recorra todos los niveles. En esta demo el Core Component sigue configurado para `summary`; su render no es una prueba de que las referencias nuevas estén publicadas o sean visibles. [Adobe: referencias anidadas](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/content-fragments/content-fragment-models#using-references-to-form-nested-content) · [Adobe: selección de elementos del componente](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/wcm-components/content-fragment-component#configure-dialog).

Si un componente personalizado va a leer `heroImage` o `gear`, primero identifica cada consumidor y define el comportamiento cuando falte el valor en fragmentos antiguos. Sólo entonces se modifica y prueba ese código. Esta clase no añade un componente ni una API: el objetivo es observar el contrato y las dependencias antes de implementarlos.

## Publicación: seguir cada referencia

El modelo debe estar disponible en Publish cuando se publique su CF. Adobe indica que, si falta al publicar el fragmento, el asistente puede ofrecer incluirlo. Un CF referenciado y una imagen son dependencias de contenido, y una página que usa el CF debe tener en Publish la versión correspondiente. Revisa la lista del asistente y comprueba el resultado en la instancia de destino; un preview de Author no demuestra el estado de Publish. [Adobe: publicar modelos](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/assets/content-fragments/content-fragments-models#publishing-a-content-fragment-model) · [Adobe: publicar fragmentos y referencias](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/content-fragments/managing#publishing-and-previewing-a-fragment) · [Adobe: modelo como referencia de la página](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/configuring-and-extending/content-fragments-customizing).

| Síntoma | Primera comprobación |
| --- | --- |
| `gear` no permite elegir `Daypack` | Modelo permitido, ruta raíz, carpeta y modelo real del CF destino. |
| El campo nuevo no aparece en `River walk` | ¿Se guardó el modelo correcto? ¿Se reabrió/refrescó el CF? ¿Editor y variación correctos? |
| La página no muestra Gear o la imagen | El componente sigue configurado para `summary`; no hay presentación automática de esas referencias. |
| La página perdió el resumen | ¿Cambió nombre/tipo de `summary`, su valor, la variación o la selección del componente? |
| Author funciona y Publish no | Estado de publicación de página, ambos CF, ambos modelos, imagen y versión consumida. |

## Repaso con respuestas

1. **¿Content Reference y Fragment Reference son equivalentes?** No. El primero admite otros recursos AEM, como imágenes; el segundo limita la selección a CF de modelos permitidos.
2. **¿Añadir `gear` rellena fragmentos anteriores?** No se debe asumir. Abre cada fragmento afectado y comprueba o completa el valor.
3. **¿Por qué conservar `summary`?** La página ya lo selecciona. Cambiar su nombre o tipo puede dejar sin datos al consumidor.
4. **¿Ver `Bring water.` en Author prueba que Gear está publicado?** No. Sólo prueba el campo y la página observados en Author.
5. **¿Qué publica el caso si se quiere verificar en Publish?** Página, Guide y Gear, sus modelos y la imagen, revisando referencias y resultado real.

## Fuentes

- [Adobe · Defining Content Fragment Models](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/content-fragments/content-fragment-models)
- [Adobe · Content Fragment Models](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/assets/content-fragments/content-fragments-models)
- [Adobe · Core Content Fragment Component](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/wcm-components/content-fragment-component)
- [Adobe · Managing Content Fragments](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/content-fragments/managing)
- [Adobe · Customizing and Extending Content Fragments](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/configuring-and-extending/content-fragments-customizing)
