# Sesión 43 · Resolver un caso MSM de localización

**Miércoles 14 de octubre de 2026 · Semana 9 · 30 minutos**

[Versión HTML](session-43-study-guide.html) · [Slides en inglés](../lessons/0043-msm-localization-case.html#slide-deck) · [Fundamentos MSM de la sesión 21](session-21-study-guide.md)

## Objetivo observable

En Author SDK local, explicar por qué una Live Copy canadiense conserva una oferta propia mientras recibe un encabezado compartido, y comprobar si un enlace interno apunta a la página canadiense correspondiente. Identificar la configuración de rollout efectiva antes de sincronizar, cancelar y restaurar la herencia sólo en el componente necesario, y distinguir esta distribución de una Language Copy y de la traducción.

La sesión 21 presentó vocabulario y una excepción simple. Aquí resolvemos **un caso con tres evidencias simultáneas**: contenido heredado, contenido local y referencia a otra página. El ejercicio ocurre en una rama de práctica; sus rutas y resultados son predicciones hasta ejecutarlos en tu SDK.

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–4 | 1–2 | Plantear el caso y separar las tres decisiones. |
| 4–8 | 3–4 | Elegir Standard rollout config y predecir el alcance de `referencesUpdate`. |
| 8–12 | 5 | Inspeccionar relación, configuración y referencia antes de actuar. |
| 12–20 | 6–8 | Demo: excepción local, sincronización y diagnóstico del enlace. |
| 20–24 | 9 | Restaurar herencia sin confundirla con sincronizar. |
| 24–27 | 10 | Live Copy, Language Copy y traducción. |
| 27–29 | 11 | Puntos clave. |
| 29–30 | 12 | Preguntas. |

## El caso

Un equipo mantiene Guides en inglés para varios mercados. La página origen tiene un encabezado, una oferta y un botón que apunta a otra página bajo el mismo origen. Canadá necesita su propia oferta, pero debe recibir el encabezado global y enlazar a la página canadiense equivalente.

```text
msm-43-lab/
├── source/
│   ├── guide/       encabezado + oferta + botón → source/contact
│   └── contact/
└── canada/          Live Copy profunda de source
    ├── guide/
    └── contact/
```

El árbol es **ilustrativo** y queda bajo una página de práctica que no sea Live Copy; en WKND local puede ser `/content/wknd/language-masters/en/msm-43-lab` si el template lo permite. No ejecutes Rollout desde sus ancestros. Esto no representa una topología multinacional de producción; mantiene el mismo idioma para aislar MSM. En un sitio real, Adobe recomienda distribuir cada idioma hacia las ramas de mercado del mismo idioma, por ejemplo un origen inglés hacia Canadá/inglés y un origen francés hacia Canadá/francés. [Adobe: MSM y traducción](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm-and-translation).

| Elemento | Dueño en `canada/guide` | Resultado tras cambiar el origen y sincronizar |
| --- | --- | --- |
| Encabezado | Origen; herencia activa | Llega el nuevo encabezado. |
| Oferta | Canadá; herencia cancelada **en ese componente** | Permanece la oferta canadiense. |
| Enlace del botón | Origen; herencia activa | Debe apuntar a `canada/contact` si `referencesUpdate` lo reconoce y la configuración efectiva lo incluye. Se verifica el path, no sólo el texto visible. |

## Rollout: primero la configuración efectiva

Una configuración de rollout combina un **trigger** y acciones. **Standard rollout config** usa *On Rollout* e incluye `contentUpdate`, `contentCopy`, `contentDelete`, `referencesUpdate`, `productUpdate` y `orderChildren`. Un **Rollout** desde la fuente empuja; **Synchronize** desde la Live Copy trae cambios y también ejecuta las configuraciones con *On Rollout*. Crear o guardar contenido en el origen no es, por sí solo, este trigger estándar. [Adobe: configuraciones de sincronización](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/live-copy-sync-config) · [Adobe: crear y sincronizar Live Copies](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/creating-live-copies).

La selección efectiva puede proceder de la página Live Copy, la página blueprint, el padre de la Live Copy o el valor predeterminado, en ese orden documentado. En **Properties → Live Copy**, registra origen, estado y configuraciones antes del cambio. Si el ejercicio usa una página fuente sin blueprint configuration, la operación disponible es **Synchronize en el destino**; no prometas que aparecerá Rollout en la fuente. No modifiques una configuración instalada ni añadas *Push on modify* para hacer funcionar esta demo: el trigger de modificación puede afectar al rendimiento y al orden de eventos. [Adobe: configuración efectiva](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/live-copy-sync-config#specifying-the-rollout-configurations-to-use) · [Adobe: buenas prácticas](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/best-practices).

### Qué puede actualizar `referencesUpdate`

La acción busca referencias de la Live Copy que señalan a un recurso **dentro del árbol origen** y las cambia al recurso relacionado dentro de la Live Copy. Una referencia hacia fuera de ese árbol queda igual. Para el ejercicio, el botón apunta a `source/contact`, cuya contraparte `canada/contact` existe. Verifica el valor guardado del enlace o su destino al abrirlo; la presencia de una página `contact` canadiense no prueba que el botón la use. [Adobe: `referencesUpdate`](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/live-copy-sync-config#synchronization-actions).

Las Live Copies anidadas pueden conservar enlaces al origen si la opción **Update Reference across nested LiveCopies** no está activa. Antes de cambiar OSGi, comprueba si realmente existe una relación anidada, cuál es la configuración efectiva y si el valor es una referencia de página dentro del árbol fuente. [Adobe: diagnóstico de referencias anidadas](https://experienceleague.adobe.com/en/docs/experience-cloud-kcs/kbarticles/ka-21808).

## Demo local · Author SDK (12 minutos en clase; 25–35 minutos de práctica individual)

**Preparación previa:** SDK Author, un sitio y template editable con componentes Text y Button permitidos, permisos para crear páginas y Live Copies. Los nombres de controles pueden variar con la versión o el idioma de AEM. No hace falta código Java ni crear una blueprint configuration.

1. Bajo una página de práctica de tu sitio local que **no sea Live Copy**, crea `msm-43-lab` y, dentro, `source` con dos hijas: `guide` y `contact`. Registra la ruta real. En `source/guide` añade **dos componentes Text distintos**: `Shared heading v1` y `Shared offer v1`. Añade un **Button** con etiqueta `Contact` cuyo enlace selecciones con el picker hacia `source/contact`. Usa componentes editables de la página, no partes bloqueadas del template.
2. Desde Sites, elige **Create → Live Copy**, usa `source` como origen y el padre `msm-43-lab` como destino; nombra la copia `canada`. Mantén los descendientes (copia profunda) y selecciona **Standard rollout config** si el asistente lo pide. Comprueba que existen `canada/guide` y `canada/contact`. No uses Copy/Paste.
3. En **Properties → Live Copy** de `canada/guide`, anota ruta fuente, relación y configuración efectiva. Abre `canada/guide` y registra los tres valores iniciales. Inspecciona el destino real del botón. Si ya es `canada/contact`, registra ese hecho; no supongas que el mapeo ocurre sólo en la siguiente sincronización.
4. En `canada/guide`, selecciona **sólo el segundo Text**, pulsa **Cancel Inheritance** y cambia su contenido a `Canada local offer`. El primer Text y el Button conservan la herencia. Cancelar la herencia del componente protege su contenido completo, no una propiedad individual.
5. Cambia los dos Text de `source/guide` a `Shared heading v2` y `Shared offer v2`. Antes de sincronizar, predice los tres resultados. En la página Live Copy `canada/guide`, usa **Synchronize** con alcance **Page Only**. Si el control ofrece incluir subpáginas, no las incluyas; `canada/contact` ya existe.
6. Recarga `canada/guide`. Comprueba `Shared heading v2`, `Canada local offer` y el **path guardado o navegado** del Button. La tabla anterior muestra la predicción bajo Standard rollout config; si el enlace aún señala `source/contact`, detén la demo y sigue el diagnóstico de abajo. No marques la demo como exitosa sólo porque la página se renderiza.
7. Para mostrar la restauración, registra primero la oferta local. En el segundo Text pulsa **Re-enable Inheritance**. Esto restaura la relación, pero no sincroniza automáticamente el valor. Solicita **Synchronize** por separado y comprueba `Shared offer v2`. Haz esta operación sólo en la rama de práctica: el valor local puede dejar de conservarse. [Adobe: cancelar y restaurar herencia](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/creating-live-copies#cancelling-inheritance-for-a-component).

| Momento | Encabezado | Oferta | Enlace esperado bajo la configuración indicada |
| --- | --- | --- | --- |
| Antes de la excepción | `Shared heading v1` | `Shared offer v1` | `canada/contact`, si se actualizó al crear la Live Copy. |
| Tras cancelar y sincronizar | `Shared heading v2` | `Canada local offer` | `canada/contact`; comprobar destino real. |
| Tras reactivar y sincronizar | `Shared heading v2` | `Shared offer v2` | `canada/contact`. |

**Evidencia mínima:** ruta fuente y destino, nombre de la configuración efectiva, estado de herencia de cada Text, los dos valores posteriores al sync y el destino real del Button. Este repositorio no contiene una instancia AEM ni registra una ejecución de la demo; la tabla describe resultados esperados.

### Si una observación no coincide

| Síntoma | Primera comprobación |
| --- | --- |
| Nada cambia | ¿Es Live Copy o una copia normal? ¿Se ejecutó Synchronize sobre `canada/guide` y terminó? ¿Qué configuración y trigger son efectivos? |
| Cambia la oferta local | ¿Se canceló la herencia en el **segundo Text** antes del sync? ¿Alguien usó Reset? |
| No cambia el encabezado | ¿Sigue heredando el primer Text? ¿Se editó el `source/guide` correcto? |
| Botón apunta al origen | ¿El valor guardado es una referencia al `source/contact` dentro del árbol fuente? ¿Existe `canada/contact`? ¿La configuración incluye `referencesUpdate`? ¿Hay Live Copy anidada? |
| El sitio publicado difiere de Author | Comprueba publicación y entrega después de verificar el valor en Author; otro rollout no demuestra que Publish recibió la página y sus dependencias. |

No uses **Reset** para corregir una sola referencia: elimina cancelaciones de herencia y devuelve la página al estado fuente, incluida la oferta local. **Detach** quita permanentemente la relación MSM. Ambas operaciones exceden la reparación de este caso. [Adobe: Reset y Detach](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/creating-live-copies#resetting-a-live-copy-page).

## Live Copy, Language Copy y traducción

| Concepto | Qué resuelve | Evidencia que buscar |
| --- | --- | --- |
| **Live Copy** | Relación MSM para reutilizar contenido entre una fuente y un destino; permite excepciones. | Fuente en Properties → Live Copy, herencia, configuración y última sincronización. |
| **Language Copy** | Rama de páginas identificada por una raíz de idioma (`en`, `fr`, etc.). | Raíz de idioma y vista **References → Language Copies**. Puede existir sin relación MSM. |
| **Proceso de traducción** | Generar y mantener contenido en otra lengua con proyectos, reglas y conectores. | Proyecto/estado de traducción y texto en la rama traducida. |

Una ruta `canada/fr` no es francesa por ser Live Copy. MSM tampoco traduce `Shared offer v2` al sincronizar. En el patrón recomendado, el contenido francés existe en su language master y MSM distribuye ese **contenido francés** al mercado francés correspondiente. Las referencias también deben conducir a una página del idioma y mercado adecuados; `referencesUpdate` sólo puede mapear destinos relacionados en el árbol de la Live Copy, no inventar una traducción faltante. [Adobe: preparación de Language Copies](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/translation/preparation) · [Adobe: MSM y traducción](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm-and-translation).

## Repaso con respuestas

1. **¿Por qué guardar el origen no cambia necesariamente Canadá?** Standard rollout config responde a *On Rollout*. Usa Rollout en un blueprint configurado o Synchronize en la Live Copy.
2. **¿Qué debe permanecer local tras sincronizar?** El segundo Text con la oferta canadiense, porque se canceló su herencia; el primer Text sigue heredando.
3. **¿Qué prueba un Button que dice “Contact”?** Sólo su etiqueta. Inspecciona el destino real para saber si apunta a `canada/contact`.
4. **¿Cuándo no reescribe `referencesUpdate` una ruta?** Si apunta fuera del árbol fuente, no existe contraparte relacionada, está excluida o la configuración/relación impide aplicarla.
5. **¿Re-enable Inheritance reemplaza enseguida el valor local?** No. Vuelve a vincular el componente; la sincronización del valor es otra operación.
6. **¿Una Language Copy es una Live Copy?** No necesariamente. La primera indica estructura por idioma; la segunda es una relación MSM. La traducción es otro proceso.

**Fuentes principales:** [Adobe, crear y sincronizar Live Copies](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/creating-live-copies) · [Adobe, configuraciones y acciones](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/live-copy-sync-config) · [Adobe, MSM y traducción](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm-and-translation) · [Adobe, Language Copies](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/translation/preparation).

**Limpieza:** después de conservar evidencia, elimina sólo `msm-43-lab` de la rama de práctica. No operes las Live Copies reales de WKND.
