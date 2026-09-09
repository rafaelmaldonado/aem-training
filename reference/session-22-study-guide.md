# Sesión 22 · Estructura compatible con AEM Cloud

**Guía profunda de preparación · Martes 15 de septiembre de 2026 · Español**

[Versión HTML](session-22-study-guide.html) · [Diapositivas](../lessons/0022-cloud-compatible-structure.html#slide-deck) · [Práctica local](#practica-local)

Un cambio puede compilar, instalarse y verse bien en un SDK, y aun así no ser una forma válida de mantener AEM as a Cloud Service. Esta sesión conecta la ubicación del recurso, el dueño del dato, el módulo que lo empaqueta y el resultado de volver a instalarlo sobre contenido que un autor ya modificó.

> **Antes de instalar, completa esta frase: este paquete cubre estas rutas, con este modo, y por eso estos valores cambiarán y estos otros se conservarán.**

## Cómo estudiar esta guía

- Primera lectura, 15–20 minutos: sigue el cambio de un título desde el paquete hasta la edición del autor y la reinstalación.
- Recuperación, 5–10 minutos: predice la matriz de importación antes de consultar el resultado.
- Práctica, 25–35 minutos: construye un ZIP pequeño y compara tres instalaciones en una rama aislada del SDK.
- Evidencia: separa el resultado esperado de los valores que realmente observaste. No necesitas acceso a Cloud Manager.

## Índice

1. [Dos recorridos de cambio](#recorridos)
2. [Mutable e inmutable](#fronteras)
3. [Responsabilidades de los módulos](#modulos)
4. [Tipos de paquete y contenedor](#paquetes)
5. [Leer un filtro](#filtros)
6. [Modos de importación](#modos)
7. [Contenido authored y reinstalaciones](#propiedad)
8. [Diagnóstico por evidencia](#diagnostico)
9. [Repaso con respuestas](#repaso)
10. [Glosario y fuentes](#fuentes)
11. [Práctica local completa](#practica-local)

<a id="recorridos"></a>

## 1. Dos recorridos de cambio

En la sesión 18, el título del componente se guardaba con el diálogo; el comportamiento Java y el script HTL se construían desde el repositorio del desarrollador. Ambos influyen en el HTML, pero no tienen el mismo ciclo de mantenimiento.

```text
Desarrollador → Git → build y validación → despliegue → código de la aplicación
Autor → diálogo → guardar en Author → publicar → contenido disponible en Publish
```

Instalar un paquete en Author no equivale a publicar una página. Modificar un archivo con CRXDE Lite en el SDK tampoco deja una fuente reproducible para el siguiente despliegue. Cuando el resultado cambia, localiza primero si cambió contenido, configuración o implementación.

**Caso del curso:** `title` pertenece al recurso de una instancia de Training Message; `training-message.html` pertenece a la definición del componente; el mensaje de entorno pertenece al PID OSGi. Un paquete de aplicación puede transportar los tres por subpaquetes distintos, sin convertirlos en una sola responsabilidad.

<a id="fronteras"></a>

## 2. Mutable e inmutable

En Cloud, `/apps` y `/libs` son inmutables durante el runtime. Los cambios de aplicación en `/apps` requieren despliegue; `/libs` pertenece al producto. `/content` y `/conf` son mutables, sujetos a permisos. `/oak:index` es una excepción relevante: aunque es mutable, sus definiciones se entregan como código por el proceso de índices. [Estructura AEM Cloud — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/aem-project-content-package-structure).

| Recurso del ejemplo | Responsabilidad |
| --- | --- |
| `/apps/wknd/components/training-message` | Implementación del componente. |
| `/apps/wknd/osgiconfig/config.author` | Configuración OSGi mantenida con código. |
| Instancia de componente bajo `/content/.../jcr:content` | Valores introducidos por el autor. |
| Política del template bajo `/conf/.../settings/wcm` | Configuración de autoría; revisar su propietario antes de empaquetar. |

Mutable responde si el runtime permite cambiar; **no** responde si el build debe sobrescribir ese recurso. Un repositorio local editable no cambia el contrato de Cloud.

<a id="modulos"></a>

## 3. Responsabilidades de los módulos

| Módulo | Artefacto o contenido esperado | Comprobación concreta |
| --- | --- | --- |
| `core` | Bundle Java: modelos y servicios. | JAR, manifiesto y descriptores DS. |
| `ui.apps` | Definiciones de componentes, HTL y clientlibs. | Árbol de código en el ZIP. |
| `ui.config` | Archivos OSGi por PID y run modes. | Ruta, nombre y propiedades del `.cfg.json`. |
| `ui.content` | Baseline mutable expresamente entregado. | Filtro y riesgo sobre contenido authored. |
| `all` | Contenedor de artefactos desplegables. | Embeds de bundles y subpaquetes. |
| `dispatcher` | Configuración del servidor de entrega. | Archivos de Dispatcher, fuera del contenido JCR. |

La tabla aplica el reparto del baseline al componente del curso. No requiere crear más módulos. Si tu proyecto separa contenido de muestra, localiza cuál se instala y en qué perfil; no asumas que toda página del tutorial tiene que viajar a producción.

<a id="paquetes"></a>

## 4. Tipos de paquete y contenedor

Los nombres Maven ayudan a navegar; la estructura efectiva se comprueba en los ZIP. En el patrón Adobe, `ui.apps` transporta código, `ui.content` contenido mutable y `all` contiene artefactos embebidos. `ui.config` se marca como `container` por transportar configuración OSGi. No mezcles `/apps` y `/content` como payload de un mismo paquete. [Estructura y tipos — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/aem-project-content-package-structure).

```text
all (container)
  ├── core.jar
  ├── ui.apps.zip     → código de componentes
  ├── ui.config.zip   → configuración OSGi
  └── ui.content.zip  → baseline mutable acordado
```

El dibujo representa contención lógica, no rutas literales de ZIP. Revisa las ubicaciones `target` de los embeds y los filtros del contenedor en tu POM. La dependencia entre artefactos debe ser explícita: una página que usa un componente no prueba que ese componente ya esté disponible al instalar cualquier ZIP por separado.

<a id="filtros"></a>

## 5. Leer un filtro

`META-INF/vault/filter.xml` define el ámbito de importación/exportación. Una raíz abarca su subárbol según includes/excludes; los patrones se evalúan en orden y prevalece el último coincidente. Las propiedades pueden filtrarse específicamente con `matchProperties`. [Workspace Filter — Apache](https://jackrabbit.apache.org/filevault/filter.html).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<workspaceFilter version="1.0">
    <filter root="/content/aem-training-package-lab" mode="merge_properties"/>
</workspaceFilter>
```

Para la práctica, una única raíz aislada hace visible el alcance. No necesitamos una expresión regular. Con `replace`, también importa lo que falta dentro del ámbito: un filtro amplio puede eliminar recursos omitidos. Por eso revisar sólo el número de archivos del ZIP no basta.

**Tres lecturas distintas:** el árbol fuente muestra lo que intentaste construir; el ZIP muestra lo que construiste; el log de instalación y el repositorio muestran lo que ocurrió. Si discrepan, sigue ese orden antes de editar más contenido.

<a id="modos"></a>

## 6. Modos de importación

Para propiedades ordinarias, `replace` puede reemplazar o eliminar estado cubierto. `merge_properties` conserva valores existentes y añade los ausentes; `update_properties` actualiza los suministrados y conserva los omitidos. [Contrato de ImportMode — Apache](https://jackrabbit.apache.org/filevault/apidocs/org/apache/jackrabbit/vault/fs/api/ImportMode.html).

Los nombres legacy `merge` y `update` tienen diferencias por serialización. FileVault introdujo los modos con sufijo `_properties` en 3.5.0 para un comportamiento más predecible. No prometas equivalencia entre ambos grupos, y comprueba la versión instalada. Las ACLs se gobiernan por `acHandling`, no por esta matriz. [Import Mode — Apache](https://jackrabbit.apache.org/filevault/importmode.html).

Ejemplo original del laboratorio: el repositorio tiene `title=Local title` y `localOnly=Keep me`; el paquete contiene `title=Package title` y `packageOnly=Added by package`.

| Modo | ¿Qué título gana? | ¿Sobrevive localOnly? | ¿Se crea packageOnly? |
| --- | --- | --- | --- |
| `merge_properties` | El local. | Sí. | Sí. |
| `update_properties` | El del paquete. | Sí. | Sí. |
| `replace` | El del paquete. | No, está cubierto y omitido. | Sí. |

La tabla es una predicción sobre este nodo `nt:unstructured`. No generalices a usuarios, grupos, ACLs, UUIDs o archivos binarios. Tampoco significa que un nombre de modo pueda proteger cualquier cambio editorial.

<a id="propiedad"></a>

## 7. Contenido authored y reinstalaciones

La primera instalación suele ocultar el problema: el repositorio no tiene valores que conservar. El ensayo útil ocurre después de que alguien lo cambie.

```text
Paquete inicial → autor modifica título → mismo paquete vuelve a instalarse
                                          ↓
                             ¿gana el paquete o gana el autor?
```

Antes de entregar un baseline, pregunta quién mantiene cada valor tras la primera instalación. Si una política la modifica un administrador en Author, no presupongas que `ui.content` puede reemplazarla en cada release. Si un dato sí es propiedad del build, registra esa decisión y comprueba el cambio previsto.

En nuestro caso, el nombre de un componente en `/apps` se mantiene con código. El título escrito en una instancia del componente pertenece al autor. Meter la página completa en un paquete de instalación recurrente requiere decidir expresamente qué debe ocurrir con esa edición.

**Caso de diagnóstico:** después de actualizar el bundle, el título volvió al texto del tutorial. Antes de culpar al getter, revisa si el despliegue instaló un paquete de contenido con esa página. Observa el valor persistido: si ya cambió en JCR, el síntoma comenzó antes del render.

<a id="diagnostico"></a>

## 8. Diagnóstico por evidencia

| Síntoma | Primera evidencia útil | Siguiente comprobación |
| --- | --- | --- |
| Falló el build del paquete. | Mensaje del validador y módulo. | Tipo, raíces y archivos incluidos. |
| El paquete se instaló, pero falta un recurso. | ZIP realmente cargado. | Filtro efectivo, ruta y log de instalación. |
| Desapareció una edición local. | Valores antes/después. | Payload suministrado, modo y ámbito. |
| El Java nuevo no se observa. | Bundle instalado y estado DS. | Versión, componente y configuración efectiva. |
| Author está correcto y Publish no. | Estado en cada instancia. | Publicación y referencias; después entrega/caché. |

“Build verde” y “contenido preservado” son afirmaciones distintas. El primero requiere salida del build; el segundo exige comparar un estado authored representativo después de instalar. Del mismo modo, la práctica local demuestra importación en ese SDK, no un pipeline de Cloud ejecutado.

Para revertir, identifica qué estado quieres recuperar y de dónde sale. Un ZIP anterior puede restaurar código sin recuperar un texto editorial eliminado. No presentes Uninstall como garantía universal de restauración; usa el procedimiento y la copia de contenido apropiados al entorno.

<a id="repaso"></a>

## 9. Repaso con respuestas

<details><summary>1. Cambié HTL con CRXDE Lite local y funciona. ¿Está listo para Cloud?</summary><p>No. Lleva el cambio al source code de ui.apps, construye y valida. La edición directa del SDK no prueba un despliegue reproducible.</p></details>

<details><summary>2. /conf es mutable. ¿Puedo reemplazarlo completo en cada build?</summary><p>La mutabilidad no asigna propiedad al build. Revisa las políticas/configuración authored, limita rutas y predice el efecto de reinstalar.</p></details>

<details><summary>3. ¿Dónde viajan el modelo, el HTL y el título de Training Message?</summary><p>Modelo en core; HTL en ui.apps; título en el recurso de contenido authored. Sólo un baseline deliberado debería empaquetar ese título mediante ui.content.</p></details>

<details><summary>4. ¿all debe contener copias directas de todo jcr_root?</summary><p>No. En el patrón del curso, all reúne artefactos embebidos; las responsabilidades de payload se mantienen en sus subpaquetes.</p></details>

<details><summary>5. Quiero actualizar title sin borrar localOnly. ¿Qué resultado predice el laboratorio?</summary><p>update_properties cambia title al valor del paquete y conserva localOnly. Eso no preserva el título que el autor había escrito.</p></details>

<details><summary>6. ¿Un recurso omitido del ZIP siempre queda intacto?</summary><p>No. Si está cubierto por un filtro con replace, puede eliminarse. Revisa ámbito y modo además de la presencia en el archivo.</p></details>

<details><summary>7. ¿Las reglas de esta tabla protegen ACLs?</summary><p>No. Las ACLs tienen reglas de acHandling. El laboratorio no incluye permisos ni authorizables.</p></details>

<details><summary>8. ¿Por qué reiniciar la línea base antes de cada ensayo?</summary><p>Porque de otro modo compararías distintos estados iniciales, además de distintos modos, y no podrías atribuir el resultado al modo.</p></details>

### Caso para defender una decisión

El equipo propone ampliar el filtro a `/content/wknd` para corregir una página de ejemplo que faltó en el ZIP. Tu siguiente paso es localizar esa página en el artefacto y comparar el filtro, no aceptar automáticamente la ampliación. Explica qué páginas authored quedarían cubiertas y diseña una comprobación de reinstalación con un cambio local. El objetivo es corregir la causa sin convertir una omisión puntual en sobrescritura masiva.

<a id="fuentes"></a>

## 10. Glosario y fuentes

| Término | Significado práctico |
| --- | --- |
| Runtime | Instancia en ejecución, después de su preparación/despliegue. |
| Baseline | Estado inicial que la aplicación entrega deliberadamente. |
| Payload | Recursos que el paquete pretende importar. |
| Filter root | Raíz del ámbito de un filtro. |
| Import mode | Regla de combinación con el estado existente. |
| Embed | Artefacto incluido dentro del paquete contenedor. |
| Author ownership | Responsabilidad de conservar y mantener un valor editorial. |
| Reinstalación | Aplicar de nuevo un paquete sobre un repositorio que ya tiene estado. |

Lectura principal: [estructura del proyecto AEM — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/aem-project-content-package-structure). Para contrastar el laboratorio: [filtros](https://jackrabbit.apache.org/filevault/filter.html), [modos](https://jackrabbit.apache.org/filevault/importmode.html), [Javadoc de ImportMode](https://jackrabbit.apache.org/filevault/apidocs/org/apache/jackrabbit/vault/fs/api/ImportMode.html) y [metadatos del paquete](https://jackrabbit.apache.org/filevault/properties.html).

Fuentes consultadas el 8 de septiembre de 2026. El curso se limita a AEM Sites tradicional. No se ejecuta un pipeline remoto ni se realiza una migración de producción en esta preparación.
<a id="practica-local"></a>

## Práctica local · Qué hace un paquete al reinstalarse (25–35 min)

**Objetivo:** comparar tres modos sobre un nodo `nt:unstructured`, sin templates, bundles ni cambios en `/apps`. Se crea un ZIP FileVault mínimo; XML no se compila como Java, se empaqueta y se importa. Necesitas el comando `jar` del JDK y un Author SDK local con Package Manager y CRXDE Lite. Los modos `merge_properties` y `update_properties` requieren FileVault 3.5.0 o posterior: comprueba la versión del bundle `org.apache.jackrabbit.vault` en `/system/console/bundles`.

**Ubicación:** crea una carpeta `package-lab` en tu repositorio de práctica y coloca estos tres archivos dentro. No mezcles `META-INF` dentro de `jcr_root`. Esta carpeta es un laboratorio aislado, no sustituye los módulos `ui.content` y `all` de tu aplicación.


### Archivo: `META-INF/vault/filter.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<workspaceFilter version="1.0">
    <filter root="/content/aem-training-package-lab" mode="merge_properties"/>
</workspaceFilter>
```

### Archivo: `META-INF/vault/properties.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
    <entry key="group">aem-training</entry>
    <entry key="name">package-lab</entry>
    <entry key="version">1.0.0</entry>
    <entry key="packageType">content</entry>
    <entry key="description">Local lab: ordinary content property import modes</entry>
</properties>
```

### Archivo: `jcr_root/content/aem-training-package-lab/.content.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:jcr="http://www.jcp.org/jcr/1.0"
    jcr:primaryType="nt:unstructured"
    title="Package title"
    packageOnly="Added by package"/>
```

### Construir e inspeccionar el ZIP

Desde la carpeta `package-lab` que contiene `META-INF` y `jcr_root`:

```sh
jar --create --file ../package-lab.zip --no-manifest -C . META-INF -C . jcr_root
jar --list --file ../package-lab.zip
```

La lista debe contener `META-INF/vault/filter.xml`, `META-INF/vault/properties.xml` y `jcr_root/content/aem-training-package-lab/.content.xml`. Puedes abrir el ZIP con tu explorador y revisar el filtro antes de instalarlo. No incluyas un directorio `package-lab/` adicional dentro del ZIP.

### Instalar y establecer una línea base

1. En `http://localhost:4502/crx/de/index.jsp`, comprueba que `/content/aem-training-package-lab` no contiene trabajo previo. Si existe y no es tu laboratorio, usa otro nombre y actualiza la ruta del filtro y la carpeta del payload de forma coherente.
2. En `http://localhost:4502/crx/packmgr/index.jsp`, usa **Upload Package**, carga `package-lab.zip`, revisa el grupo `aem-training` y usa **Install**. El modo inicial es `merge_properties`.
3. En CRXDE Lite refresca el árbol y selecciona `/content/aem-training-package-lab`. Deben aparecer `title=Package title` y `packageOnly=Added by package`. Este nodo no es una página Sites y no se espera que renderice HTML.
4. Prepara la línea base para cada ensayo: cambia `title` a `Local title`, añade una propiedad String `localOnly=Keep me` y elimina sólo `packageOnly` si existe. Pulsa **Save All**. No cambies `jcr:primaryType`.
5. Antes de reinstalar, copia estos tres valores iniciales a tu evidencia. Cada ensayo debe comenzar exactamente en ese estado.

### Comparar los modos

1. Reinstala el paquete original con `merge_properties`. Confirma que `title` sigue local, que `localOnly` se conserva y que aparece `packageOnly`.
2. Restablece la línea base del paso 4. En tu archivo fuente `filter.xml`, cambia **sólo** `mode="merge_properties"` a `mode="update_properties"`. Reconstruye el ZIP con el mismo comando. En Package Manager vuelve a cargarlo con **Force Upload** para reemplazar el archivo de la misma versión; revisa el filtro recién cargado y reinstala. No uses Build en Package Manager: exportaría el estado actual y cambiaría el payload del experimento.
3. Restablece otra vez la línea base. Cambia el modo a `replace`, reconstruye, carga y reinstala siguiendo el mismo procedimiento. Comprueba únicamente el nodo aislado del laboratorio.

| Modo | title después | localOnly después | packageOnly después |
| --- | --- | --- | --- |
| merge_properties | Local title | Keep me | Added by package |
| update_properties | Package title | Keep me | Added by package |
| replace | Package title | Ausente | Added by package |

**Interpretación:** `update_properties` conserva lo omitido, pero sí sobrescribe un valor authored incluido en el paquete. `replace` también puede eliminar contenido cubierto que falta en el payload. Estos resultados se refieren a propiedades ordinarias de este nodo; ACLs, usuarios, binarios y UUIDs necesitan revisar sus reglas específicas. No cambies los modos a los legacy `merge`/`update` suponiendo que son equivalentes.

**Aceptación:** ZIP inspeccionado, versión FileVault registrada y una tabla de valores observados para los tres ensayos. Si un modo es rechazado, conserva el error y verifica la versión; no lo cambies por `replace` sólo para lograr una instalación verde.

**Volver al proyecto:** identifica en tus POM qué contiene `ui.apps`, `ui.content`, `ui.config` y `all`; abre el ZIP generado por tu build y localiza los filtros de los subpaquetes. Anota qué pasaría con un título modificado por un autor si reinstalas. No amplíes los filtros de la aplicación para incluir todo `/content`.

**Limpieza:** al finalizar, elimina sólo `/content/aem-training-package-lab` y el paquete `aem-training:package-lab` de tu Author local. Devuelve el filtro fuente a `merge_properties` si conservarás el ejemplo. No tomes Uninstall como estrategia general de rollback del contenido authored.

Fuentes: [workspace filters](https://jackrabbit.apache.org/filevault/filter.html), [modos de importación](https://jackrabbit.apache.org/filevault/importmode.html) y [propiedades del paquete](https://jackrabbit.apache.org/filevault/properties.html).
