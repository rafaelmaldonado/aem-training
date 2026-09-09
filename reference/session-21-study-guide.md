# Sesión 21 · Fundamentos de Multi-Site Management en AEM

**Guía profunda de preparación · Lunes 14 de septiembre de 2026 · Español**

[Abrir la versión HTML](session-21-study-guide.html) · [Ver las diapositivas](../lessons/0021-msm-foundations.html#slide-deck) · [Notas del presentador](../slides/lesson-21/speech.md)

La sesión 21 abre la semana 5 con Multi-Site Management, o MSM. El objetivo es seguir una relación desde una fuente hasta su Live Copy, predecir qué cambiará al sincronizar y conservar una excepción local deliberada. El caso central utiliza un origen en inglés y dos sitios de mercado del mismo idioma.

> **La cadena que debes poder explicar es fuente → herencia → acción → resultado.** Dos páginas iguales no prueban una relación MSM; una relación activa tampoco demuestra que todos sus componentes estén sincronizados.

[Ir a la práctica local completa](#practica-local)

## Cómo estudiar esta guía

- **Primera lectura, 20–25 minutos:** sigue la página de Canadá y distingue lo heredado de lo que su equipo mantiene localmente.
- **Recuperación, 5–10 minutos:** responde las preguntas antes de abrir sus soluciones y predice los cambios de la matriz del caso práctico.
- **Antes de la sesión:** explica sin mirar las diferencias entre Synchronize, Rollout, Reset y Detach.
- **Después de la sesión:** registra una relación real y una sincronización controlada en el entorno de práctica. Si sólo estudias la guía, conserva las predicciones como hipótesis; no las presentes como resultados observados en AEM.

**Resultado esperado:** demostrar de dónde hereda una página, identificar una excepción a nivel de componente y justificar el alcance de la acción seleccionada. El curso se centra en AEM Sites tradicional sobre AEM as a Cloud Service; esta preparación no diseña una topología MSM de producción ni modifica contenido real.

## Índice

1. [MSM es una relación mantenida](#relacion)
2. [Fuente, blueprint y Live Copy](#objetos)
3. [Idioma y mercado en el árbol de sitios](#idiomas)
4. [Herencia y propiedad local](#herencia)
5. [Inspeccionar antes de actuar](#inspeccion)
6. [Synchronize y Rollout](#sincronizacion)
7. [Trigger y acciones de rollout](#configuracion)
8. [Cancelar, suspender, restablecer o separar](#acciones)
9. [MSM, traducción e i18n](#localizacion)
10. [Caso integrado y evidencia](#caso)
11. [Repaso con respuestas](#repaso)
12. [Glosario y fuentes](#fuentes)

<a id="relacion"></a>

## 1. MSM es una relación mantenida

MSM permite reutilizar contenido en distintas ubicaciones de AEM Sites conservando relaciones entre recursos equivalentes. La fuente proporciona contenido; el destino puede recibir cambios posteriores mediante sincronización.

```text
Fuente ── relación mantenida ──► Live Copy
   └── cambios posteriores ───► sincronización según configuración

Fuente ── copia puntual ──────► contenido independiente
```

Una copia puntual puede tener el mismo texto y diseño que la fuente. Esa igualdad sólo describe el estado actual; no prueba que mañana reciba cambios.

Tampoco interpretes «Live» como actualización inmediata permanente. La propagación depende del trigger, las acciones configuradas, el alcance y el estado de herencia. Con una configuración de sincronización explícita, guardar la fuente no significa que el destino ya haya recibido el cambio.

El valor práctico de MSM es equilibrar reutilización y variaciones locales. Sin un origen claro, varios equipos duplican el mismo mantenimiento. Sin excepciones explícitas, una actualización central puede entrar en conflicto con necesidades de un mercado. Base: [notas de la sesión, slides 2 y 5](../slides/lesson-21/speech.md).

<a id="objetos"></a>

## 2. Fuente, blueprint y Live Copy

Estas palabras se relacionan, pero no identifican el mismo objeto:

| Concepto | Qué representa | Pregunta que responde |
| --- | --- | --- |
| Source o fuente | Página o rama de contenido de origen. | ¿De dónde provienen los valores heredados? |
| Blueprint configuration | Configuración que identifica un sitio fuente y habilita flujos de creación y rollout. | ¿Qué origen está preparado para ese flujo de autoría? |
| Live Copy | Contenido destino con relaciones mantenidas hacia su origen. | ¿Qué sitio o rama recibe los cambios? |
| LiveRelationship | Relación efectiva de un recurso destino con su contraparte fuente. | ¿Este recurso concreto sigue relacionado? |
| Rollout configuration | Reglas de cuándo y cómo se sincroniza. | ¿Qué evento ejecuta qué acciones? |

En la documentación, **blueprint** también puede referirse a la fuente. Por eso conviene decir «página fuente» o «configuración de blueprint» cuando la diferencia importa.

Una Live Copy puede crearse a partir de una fuente normal sin blueprint configuration. El flujo Create Site usa un blueprint predefinido; una Live Copy creada directamente puede sincronizarse desde el destino aunque no disponga del mismo botón Rollout en la fuente. [Vocabulario y flujos de MSM — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/overview).

No confundas esta herencia de contenido con la herencia Java ni con el `sling:resourceSuperType` de componentes estudiado en la [sesión 17](session-17-study-guide.html#delegacion). Reutilizar una implementación de Core Component no crea por sí solo una relación Live Copy entre dos páginas.

<a id="idiomas"></a>

## 3. Idioma y mercado en el árbol de sitios

El ejemplo WKND distingue la fuente de cada idioma de las variantes para mercados:

```text
/content/wknd
    language-masters
        en                 ← fuente principal en inglés
        fr                 ← fuente principal en francés
    us
        en                 ← posible Live Copy del origen inglés
    ca
        en                 ← posible Live Copy del origen inglés
        fr                 ← posible Live Copy del origen francés
```

Las rutas son representativas. Su existencia en un proyecto no demuestra que las relaciones ya estén configuradas.

Un **language root** identifica la rama de un idioma. El **language master** es la fuente principal de autoría para ese idioma dentro de esta organización. Una rama de mercado como Canadá/inglés puede reutilizar ese contenido y mantener diferencias locales.

El recorrido del ejemplo es:

```text
/content/wknd/language-masters/en
        ├── MSM → /content/wknd/us/en
        └── MSM → /content/wknd/ca/en
```

El idioma y el mercado son dimensiones diferentes: compartir inglés no obliga a compartir todas las ofertas, y pertenecer a Canadá no convierte inglés y francés en una misma rama de contenido.

La distribución dentro del mismo idioma es el patrón de esta sesión, no un motor de traducción ni una afirmación de que MSM traduzca al conectar rutas con distintos códigos de idioma. Base: [notas de la sesión, slide 4](../slides/lesson-21/speech.md).

<a id="herencia"></a>

## 4. Herencia y propiedad local

Imagina una página con Header, Hero y Offer. Canadá necesita un mensaje específico en Hero, pero debe seguir recibiendo el encabezado y la oferta comunes.

| Componente de la Live Copy | Estado deseado | Dueño del contenido |
| --- | --- | --- |
| Header | Heredado | Equipo del origen. |
| Hero | Herencia cancelada para una variación local | Equipo de Canadá. |
| Offer | Heredado | Equipo del origen. |

La acción adecuada es cancelar herencia en el componente que necesita la excepción, no desconectar la página completa. Los hermanos conservan su relación y reciben los cambios elegibles de una sincronización ordinaria.

**Cancelar herencia del componente afecta a ese componente, no sólo al campo que tienes en mente.** Si el requisito es «un título local», comprueba qué otros valores quedan bajo mantenimiento local al cancelar su herencia. No prometas una protección por propiedad cuando la acción elegida tiene alcance de componente.

Una excepción debería tener responsable y motivo. «Hero local porque existe una campaña canadiense» explica por qué debe sobrevivir al siguiente rollout; «alguien desbloqueó esto» no permite decidir si la diferencia es correcta.

### Restaurar la relación no es actualizar el contenido

Re-enable Inheritance devuelve al origen la capacidad de aportar contenido. La sincronización sigue siendo una operación distinta. No interpretes el botón como una garantía de que ya se copiaron los valores actuales de la fuente.

Antes de sincronizar después de reactivar herencia, identifica el valor local que dejará de estar protegido. Si debe conservarse como referencia, registra la evidencia antes del cambio. Base: [notas de la sesión, slide 5](../slides/lesson-21/speech.md).

<a id="inspeccion"></a>

## 5. Inspeccionar antes de actuar

Empieza por la ubicación exacta del síntoma. «La página de Canadá está desactualizada» todavía no identifica qué relación falla.

1. Registra la ruta destino y el componente o propiedad que observas.
2. En las propiedades de la página, revisa la pestaña Live Copy.
3. Identifica la fuente, la herencia y las configuraciones de rollout aplicables.
4. Comprueba el estado del componente concreto; el estado general de la página no basta.
5. Desde la fuente, usa References → Live Copies → Live Copy Overview para comparar relaciones y estructura donde ese flujo esté disponible.

La consola de overview ayuda a situar las Live Copies respecto a su fuente y ofrece acciones relacionadas con su estado. Las opciones visibles dependen del contexto seleccionado y de los permisos. [Live Copy Overview — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/live-copy-overview).

| Evidencia | Lo que demuestra |
| --- | --- |
| Dos páginas visualmente iguales | Coincidencia actual del resultado. |
| Ruta fuente en las propiedades Live Copy | Origen configurado de esa relación. |
| Estado del componente | Si ese recurso hereda o mantiene una excepción. |
| Configuración aplicable | Qué desencadena y ejecuta la sincronización. |
| Valores antes y después | Efecto concreto observado de una acción. |

Si el repositorio o Author ya tienen el valor esperado y sólo la web publicada muestra otro, has llegado a otra frontera de diagnóstico. Revisa publicación y entrega según corresponda; repetir MSM sin comprobar el contenido destino no aporta evidencia.

<a id="sincronizacion"></a>

## 6. Synchronize y Rollout

Las dos acciones llevan cambios de la fuente al destino. Lo que cambia es el punto desde el que se inicia y selecciona la operación.

| Aspecto | Synchronize | Rollout |
| --- | --- | --- |
| Inicio manual | Live Copy. | Fuente/blueprint en el flujo disponible. |
| Perspectiva | El destino solicita cambios de su fuente. | El origen envía cambios a los destinos seleccionados. |
| Destinos | Live Copy seleccionada y alcance elegido. | Una o varias Live Copies, según selección. |
| Reglas de actualización | Configuración de rollout efectiva. | Configuración de rollout efectiva. |

**Synchronize no sube los cambios de Canadá al language master.** Pull describe que el destino solicita la actualización, no que se invierta el origen del contenido.

Antes de ejecutar cualquiera, completa esta frase:

> Desde esta fuente actualizaré estos destinos, con este alcance y configuración. Espero que cambien estos componentes y que permanezca local esta excepción.

«Una página» y «esa página con descendientes» son alcances diferentes. Tampoco ejecutar Rollout significa necesariamente afectar a todas las Live Copies existentes: comprueba la selección del diálogo y el ámbito real.

Una Live Copy puede ser superficial, de una página, o profunda, incluyendo descendientes. Esa característica de la relación no sustituye revisar el alcance de la operación elegida. Esta guía no propone cambiar la profundidad como atajo para resolver un componente desactualizado.

Base: [notas de la sesión, slide 7](../slides/lesson-21/speech.md).

<a id="configuracion"></a>

## 7. Trigger y acciones de rollout

Separa **cuándo** empieza una sincronización de **qué** hace:

```text
Trigger → configuración de rollout → acciones → cambios elegibles
```

La configuración estándar utiliza el trigger **On Rollout**, tanto para la orden Rollout como para Synchronize. Puede ejecutar operaciones de actualización, copia, eliminación, ordenación y actualización de referencias.

| Nombre representativo | Tipo de operación |
| --- | --- |
| `contentUpdate` | Actualizar contenido elegible. |
| `contentCopy` | Copiar contenido fuente que falta en el destino. |
| `contentDelete` | Eliminar contenido dentro de las reglas de la acción. |
| `referencesUpdate` | Actualizar referencias según sus reglas. |
| `orderChildren` | Ajustar el orden de hijos. |

La tabla es un mapa de lectura, no un listado completo ni una promesa de afectar todo nodo. Comprueba exclusiones y comportamiento de las acciones instaladas. Las configuraciones efectivas pueden proceder de la Live Copy, su fuente, la jerarquía o el valor predeterminado; no deduzcas cuál se usa por el nombre del sitio.

Otros triggers responden a modificación, activación o desactivación. **On Modification** puede afectar al rendimiento; activarlo para no tener que pensar cuándo sincronizar cambia el contrato operativo. [Configuración de sincronización — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/live-copy-sync-config).

La sincronización estándar no equivale por sí sola a publicar el destino. Si una configuración añade acciones de activación, ése es un comportamiento adicional que debes comprobar.

Empieza por la configuración instalada que cumple el requisito. Crear una acción personalizada de rollout añade mantenimiento y consecuencias sobre muchos destinos; no forma parte del objetivo de esta sesión. [Buenas prácticas de MSM — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/best-practices).

<a id="acciones"></a>

## 8. Cancelar, suspender, restablecer o separar

Elige la acción por su alcance y su efecto sobre la relación, no por el parecido entre sus nombres.

| Acción | Intención | Impacto que debes anticipar |
| --- | --- | --- |
| Cancel Inheritance | Permitir una excepción local en el componente seleccionado. | Ese componente deja de recibir cambios heredados ordinarios. |
| Re-enable Inheritance | Devolver al origen la propiedad del contenido heredado. | Restablece la herencia; sincronizar el contenido es otra decisión. |
| Suspend | Pausar temporalmente la relación de una página en el alcance elegido. | Detiene su propagación heredada mientras permanezca suspendida. |
| Resume | Recuperar una relación suspendida. | Puede acompañarse de sincronización si se solicita. |
| Reset | Retirar cancelaciones y devolver el alcance afectado al estado fuente. | Sobrescribe cambios locales afectados. |
| Detach | Eliminar permanentemente la relación. | No tiene un Resume que deshaga la separación. |

**Reset no es un refresco inocuo.** Si el Hero local tiene que conservarse, resetear la página puede contradecir directamente ese requisito. «Quiero recibir lo heredado» y «quiero descartar mis diferencias locales» son intenciones distintas.

**Detach tampoco es una pausa.** La operación elimina la relación MSM. En una subrama cuyo padre sigue relacionado, un rollout posterior del padre puede producir conflictos, renombrar páginas separadas y crear nuevas Live Copies. No lo interpretes como un modo universal de proteger una rama frente a cualquier operación del ancestro.

En Resume, el diálogo puede permitir solicitar sincronización además de restaurar la herencia. Distingue ambas decisiones al explicar el resultado. [Acciones y alcance de Live Copy — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/creating-live-copies).

Para una necesidad pequeña, utiliza la acción más pequeña que la resuelve. Antes de Reset o Detach en una práctica, identifica el ámbito exacto y las diferencias que perderías; no los uses como pasos de diagnóstico por defecto.

<a id="localizacion"></a>

## 9. MSM, traducción e i18n

Un texto localizado incorrecto puede pertenecer a tres problemas distintos:

| Capa | Qué resuelve | Ejemplo |
| --- | --- | --- |
| MSM | Reutilización y distribución de contenido entre ubicaciones relacionadas. | Inglés del language master hacia Canadá/inglés. |
| Traducción | Creación y mantenimiento de contenido authored en otro idioma. | Texto de una página inglesa a su versión francesa. |
| i18n | Etiquetas de interfaz del componente. | Traducción de la etiqueta fija «Read more». |

Una campaña canadiense redactada en inglés puede ser una excepción comercial local sin involucrar traducción. Una página francesa incompleta no se arregla automáticamente sincronizando texto inglés. Una etiqueta fija sin traducir exige revisar el contrato de i18n del componente, no cancelar la herencia de toda la página.

En el patrón del curso, primero existe contenido fuente para cada idioma y después MSM lo distribuye a los mercados correspondientes. Las decisiones de traducción y reutilización se coordinan, pero siguen siendo responsabilidades distintas. [MSM y traducción — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm-and-translation).

No todo texto dentro de un componente es una etiqueta de diccionario: un título escrito por el autor es contenido. Clasifica primero quién lo produce y dónde se almacena.

<a id="caso"></a>

## 10. Caso integrado y evidencia

Utiliza una página de práctica y su Live Copy del mismo idioma. Estos paths y valores son ilustrativos; no afirman que existan en tu SDK:

```text
Fuente:  /content/wknd/language-masters/en/adventures
Destino: /content/wknd/ca/en/adventures
```

### Primero predice el resultado

Supón que Header y Offer siguen heredando, Hero tiene la herencia cancelada y la configuración ejecuta las actualizaciones ordinarias de contenido dentro del alcance elegido:

| Componente | Fuente después de editar | Destino antes de sincronizar | Destino esperado después |
| --- | --- | --- | --- |
| Header heredado | `Explore the outdoors` | `Welcome to WKND` | `Explore the outdoors` |
| Hero local | `Summer adventures` | `Explore Canada` | `Explore Canada` |
| Offer heredado | `New guided routes` | `Weekend routes` | `New guided routes` |

El éxito tiene dos partes: **se actualiza lo que debe heredar y se conserva lo que debe permanecer local**. Comprobar sólo Header dejaría sin verificar la excepción que justificaba el ejercicio.

### Después ejecuta en el entorno de práctica

1. Confirma fuente, destino y relación real antes de editar.
2. Registra los valores iniciales y la configuración aplicable.
3. Si el ejercicio lo requiere, cancela herencia sólo en Hero y establece su valor local.
4. Cambia valores de la fuente con alcance controlado.
5. Anota la predicción y ejecuta una Synchronize o Rollout explícita con la selección revisada.
6. Compara los tres resultados y registra diferencias entre predicción y observación.

Si no coincide el resultado, revisa la relación y la acción antes de modificar más contenido:

| Síntoma | Primera investigación |
| --- | --- |
| Nada cambió | Fuente, destino, trigger ejecutado, alcance y suspensión. |
| Sólo un componente quedó distinto | Cancelación local y reglas de ese recurso. |
| Se perdió una excepción | Acción utilizada, estado previo y alcance de un posible Reset. |
| El texto coincide pero el orden cambió | Herencia del contenedor y acciones de ordenación. |
| Author está bien y Publish no | Publicación y entrega tras comprobar el contenido destino. |
| El idioma o etiqueta es incorrecto | Contenido traducido o i18n, según su procedencia. |

### Mapa de evidencias

| Campo | Qué registrar |
| --- | --- |
| Fuente | Ruta y componente origen. |
| Destino | Ruta y recurso equivalente. |
| Relación | Evidencia de Live Copy, estado de página y estado de componente. |
| Propiedad local | Responsable, motivo y valores que deben conservarse. |
| Configuración | Trigger y acciones efectivamente aplicables. |
| Operación | Synchronize o Rollout, punto de inicio y selección. |
| Alcance | Página, descendientes y destinos incluidos. |
| Predicción | Qué debería cambiar y qué debería mantenerse. |
| Resultado | Valores antes/después y explicación de cualquier diferencia. |

**Criterio de preparación:** explicar la tabla completa sin apoyarte sólo en capturas del aspecto final. El ejercicio exige evidencia de contenido y relación, no simplemente que dos páginas se vean parecidas.

<a id="repaso"></a>

## 11. Repaso con respuestas

Responde antes de desplegar cada solución. Este repaso es personal; el cierre de la presentación sigue reservado a preguntas de la audiencia.

<details>
<summary>1. ¿Dos páginas idénticas prueban que una es Live Copy de la otra?</summary>
<p>No. Sólo prueban igualdad actual. Debes comprobar la relación, la fuente configurada y el estado del recurso.</p>
</details>

<details>
<summary>2. ¿Un language master es lo mismo que una blueprint configuration?</summary>
<p>No. El primero es contenido fuente organizado por idioma; la segunda configura un origen para determinados flujos de creación y rollout.</p>
</details>

<details>
<summary>3. ¿Qué dirección tienen los datos al usar Synchronize desde Canadá?</summary>
<p>Van de la fuente hacia Canadá. El destino solicita la actualización; no envía sus cambios locales de vuelta al language master.</p>
</details>

<details>
<summary>4. ¿Cómo conservarías un Hero local sin desconectar Header y Offer?</summary>
<p>Cancelaría la herencia en Hero, comprobaría el alcance de esa excepción y mantendría vinculados los otros componentes.</p>
</details>

<details>
<summary>5. ¿Re-enable Inheritance garantiza que ya se copiaron los valores de la fuente?</summary>
<p>No. Restaurar herencia y sincronizar contenido son decisiones distintas. Comprueba qué acción se solicitó y qué valores cambiaron.</p>
</details>

<details>
<summary>6. ¿Qué distingue un trigger de una acción de rollout?</summary>
<p>El trigger determina cuándo se ejecuta; la acción determina qué operación realiza sobre el contenido. La configuración reúne esas reglas.</p>
</details>

<details>
<summary>7. ¿Por qué Reset no es un reemplazo habitual de Synchronize?</summary>
<p>Porque Reset elimina cancelaciones y devuelve el alcance al estado fuente, sobrescribiendo diferencias locales afectadas. Puede destruir la excepción que pretendías conservar.</p>
</details>

<details>
<summary>8. ¿MSM traduce el contenido al copiarlo a otra rama de idioma?</summary>
<p>No. MSM reutiliza contenido mediante relaciones. La traducción de contenido y los diccionarios i18n resuelven otras responsabilidades.</p>
</details>

### Cuatro casos para elegir la siguiente acción

<details>
<summary>Caso A · Header cambia tras sincronizar y Hero conserva «Explore Canada». ¿Hay un fallo?</summary>
<p>No necesariamente. Si Header hereda y Hero tiene una excepción local deliberada, ése es el resultado esperado. Confirma el estado de ambos componentes.</p>
</details>

<details>
<summary>Caso B · Reanudaste una página suspendida, pero conserva texto anterior. ¿Qué comprobarías?</summary>
<p>Si sólo restauraste la relación o también solicitaste sincronización. Después comprueba configuración, alcance y cancelaciones de componentes antes de ejecutar otra acción.</p>
</details>

<details>
<summary>Caso C · Quieres una variación local temporal y alguien propone Detach. ¿Qué revisarías?</summary>
<p>Detach es permanente y no tiene una reanudación inversa. Para una excepción de componente, revisa Cancel Inheritance; para una pausa de página, Suspend con el alcance adecuado.</p>
</details>

<details>
<summary>Caso D · El contenido francés está bien, pero «Read more» aparece en inglés. ¿Por dónde empezarías?</summary>
<p>Por la procedencia de la etiqueta. Si es una cadena fija de interfaz, revisa su i18n y contexto de idioma, en vez de resetear la Live Copy o repetir la traducción de la página.</p>
</details>

Si algo no está claro, pregunta al agente con las rutas, el estado de herencia, la acción elegida y el resultado esperado. Puedes pedir otro caso para practicar la predicción antes de ver su solución.

<a id="fuentes"></a>

## 12. Glosario y fuentes

| Término | Definición de referencia |
| --- | --- |
| MSM | Multi Site Manager: reutilización de contenido mediante relaciones Live Copy. |
| Fuente | Contenido desde el que se hereda. |
| Blueprint configuration | Configuración que identifica un sitio fuente para flujos MSM. |
| Live Copy | Destino que mantiene relaciones hacia contenido fuente. |
| LiveRelationship | Relación efectiva de un recurso con su contraparte fuente. |
| Language master | Fuente principal de autoría de un idioma en el patrón del curso. |
| Herencia | Participación del recurso en la recepción de contenido fuente al sincronizar. |
| Override local | Diferencia mantenida deliberadamente por el destino. |
| Rollout configuration | Reglas de trigger y acciones de sincronización. |
| Shallow / deep | Live Copy de una página / incluyendo páginas descendientes. |
| i18n | Internacionalización de cadenas de interfaz, distinta de traducir contenido authored. |

**Lectura principal:** [Reusing Content: Multi Site Manager and Live Copy — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/overview). Prioriza vocabulario, composición de Live Copies y el ejemplo de language masters.

Fuentes de preparación, consultadas el 8 de septiembre de 2026:

- [Sesión 21 y diapositivas](../lessons/0021-msm-foundations.html), [outline](../slides/lesson-21/outline.md) y [notas del presentador](../slides/lesson-21/speech.md).
- [Creating and Synchronizing Live Copies — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/creating-live-copies): herencia, sincronización, Reset y Detach.
- [Configuring Live Copy Synchronization — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/live-copy-sync-config): triggers y acciones.
- [Live Copy Overview Console — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/live-copy-overview): inspección y operación de relaciones.
- [MSM Best Practices — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/best-practices): límites y decisiones de mantenimiento.
- [Multi Site Manager and Translation — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm-and-translation): separación entre distribución y traducción.

**Alcance:** relaciones de páginas AEM Sites, herencia y operaciones estándar. El diseño de topologías de producción, las acciones personalizadas, los conectores de traducción y Assets MSM quedan fuera de esta preparación. Las rutas y resultados del caso son ilustrativos; no se ha ejecutado ninguna operación MSM al crear esta guía.

<a id="practica-local"></a>

## Práctica local · Una Live Copy con una excepción (25–35 min)

**Requisitos:** Author SDK local, permisos para crear páginas y Live Copies y un template editable con dos componentes Title o Text permitidos. No hace falta código ni blueprint configuration: se usará **Synchronize desde el destino**. Los nombres de controles pueden variar con el SDK o el idioma de la interfaz.

1. En `http://localhost:4502/sites.html/content`, dentro de un sitio funcional de tu baseline (por ejemplo `/content/wknd/us/en`), crea una página contenedora llamada `msm-lab` usando su template. Registra su ruta real; todos los pasos siguientes ocurren debajo de esa rama.
2. Bajo `msm-lab`, crea una página `source` y añade **dos componentes de contenido editables**. Escribe `Shared heading v1` en el primero y `Shared offer v1` en el segundo. No uses componentes bloqueados por la estructura del template para esta demostración.
3. En Sites selecciona `msm-lab`, elige **Create → Live Copy**, indica `source` como origen, elige `msm-lab` como destino y llama `canada` a la copia. Mantén el mismo idioma. Selecciona **Standard rollout config** si el asistente lo solicita y finaliza. No uses Copy/Paste.
4. En las propiedades de `canada`, abre **Live Copy** y confirma la ruta fuente exacta y la configuración de rollout. Registra esa evidencia antes de editar.
5. Abre `canada` en el editor. Selecciona sólo el **segundo componente**, usa **Cancel Inheritance** (icono de enlace/candado según SDK), confirma y cambia su texto a `Canada local offer`. Deja el primer componente heredado.
6. En `source`, cambia los textos a `Shared heading v2` y `Shared offer v2`; guarda. Predice por escrito qué debe quedar en `canada`.
7. Regresa a Sites, selecciona `canada` y usa **Synchronize** desde la barra o las propiedades Live Copy. Confirma origen y alcance: sólo esta página, sin descendientes. La acción no requiere un Rollout en la fuente.
8. Recarga `canada`: el primer componente debe mostrar `Shared heading v2`, y el segundo debe conservar `Canada local offer`. Si no sucede, inspecciona estado del componente, configuración y alcance antes de repetir.
9. En el segundo componente reactiva herencia. Si el diálogo ofrece sincronizar ahora, deja esa opción sin marcar para observar las dos operaciones por separado. Luego solicita Synchronize explícitamente y comprueba `Shared offer v2`.

| Momento | Primer componente | Segundo componente |
| --- | --- | --- |
| Tras crear Live Copy | Shared heading v1 | Shared offer v1 |
| Tras excepción y Synchronize | Shared heading v2 | Canada local offer |
| Tras reactivar y sincronizar | Shared heading v2 | Shared offer v2 |

**Aceptación:** captura de la relación y de las dos salidas posteriores, con ruta fuente, destino y componente que perdió la protección local. La matriz es una predicción a comprobar, no evidencia de una instancia ya ejecutada.

**Limpieza:** elimina sólo la rama `msm-lab` cuando termines y después de conservar evidencia. No uses Reset ni Detach como parte de esta práctica: no son necesarios para demostrar una excepción de componente. No ejecutes acciones contra las Live Copies reales de WKND.

Fuente: [crear y sincronizar Live Copies — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/creating-live-copies).
