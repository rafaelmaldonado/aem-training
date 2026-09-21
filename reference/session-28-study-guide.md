# Sesión 28 · Modelar permisos como código

**Miércoles 23 de septiembre de 2026 · Semana 6 · Núcleo de 30 minutos, ampliable a 60**

[Versión HTML](session-28-study-guide.html) · [Slides en inglés](../lessons/0028-permissions-as-code.html#slide-deck) · [Ejemplo local](#ejemplos-locales)

Un cambio de contenido necesita una identidad y permisos sobre una ruta concreta. Que una persona pueda entrar en Author no demuestra que pueda modificar una página. Tampoco basta con encontrar una regla `allow` para un grupo: el resultado puede depender de sus otras membresías, de los antecesores y de reglas aplicadas directamente al usuario. La pregunta útil es **qué identidad intenta realizar qué operación sobre qué recurso**.

En esta sesión modelamos esa intención con Repo Init: una configuración versionada crea un grupo editorial, una identidad técnica y un pequeño árbol de prueba. El grupo puede leer el árbol y modificar propiedades únicamente en `guides`, siempre que no existan otras concesiones. Después inspeccionamos las ACL y contrastamos una operación permitida con otra fuera del alcance. El ejemplo usa carpetas del repositorio; no pretende configurar un rol completo de autoría de Sites.

- Un usuario representa una identidad; un grupo permite asignar responsabilidades compartidas.
- IMS autentica a las personas en Cloud Author; las ACL regulan operaciones en el repositorio.
- Un service user pertenece al repositorio y sirve al código, sin contraseña para iniciar sesión.
- Mínimo privilegio combina **operación, ruta e identidad**, no sólo un nombre de rol.
- La ACL visible de un grupo es una parte del acceso efectivo.
- Repo Init hace reproducible una configuración; hay que comprobar también los accesos que deberían quedar excluidos.

## Recorrido de la sesión

| Minutos | Slides | Contenido |
|---|---|---|
| 0–5 | 1–3 | Identidades y separación entre acceso Cloud y autorización. |
| 5–11 | 4–6 | ACL, privilegios concretos y acceso heredado. |
| 11–23 | 7–9 | Leer el script e inspeccionar el ejemplo preparado. |
| 23–27 | 10 | Comprobar el alcance y explicar una diferencia. |
| 27–30 | 11–12 | Key takeaways y preguntas. |

Para llegar a 60 minutos, añade 20 de instalación/inspección guiada y 10 de preguntas. El instructor prepara el ejemplo antes de clase; no depende de prácticas previas. Las actividades son demostraciones y consulta voluntaria, sin entrega por sesión.

<a id="identidades"></a>
## 1. Personas, grupos e identidades técnicas

| Elemento | Para qué sirve | Ejemplo de esta sesión |
|---|---|---|
| Usuario humano | Realizar acciones interactivas con una identidad identificable. | `training-permissions-demo`, creado sólo en el SDK. |
| Grupo | Asociar permisos a una responsabilidad, reutilizable entre personas. | `training-guide-editors`. |
| Service user | Dar al código una identidad técnica con acceso específico. | `training-guide-reader`. |
| Principal | Identidad a la que se refiere una entrada de control de acceso. | El principal del grupo o del service user. |

En Cloud Author, Admin Console e IMS gestionan el acceso de las personas al entorno. Los grupos sincronizados pueden integrarse con grupos locales de AEM que tienen permisos sobre contenido. Mantén las responsabilidades editoriales en esos grupos y revisa cómo llega la membresía desde IMS; crear una persona con contraseña en Repo Init no reproduce ese proceso. [IMS y permisos en AEM — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/security/ims-support).

El service user no es una cuenta humana compartida ni una credencial OAuth para una integración externa. Hoy creamos su identidad y una ACL de lectura. La configuración que relaciona bundle y subservice, la obtención del resolver y su cierre pertenecen a la sesión 29. Crear el usuario por sí solo no cambia la identidad con la que se ejecuta el código. [Service users — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/developing/advanced/service-users).

<a id="acl"></a>
## 2. Una ACL y el acceso efectivo

Una ACL es una lista de entradas, o ACE. Cada entrada vincula un principal, privilegios y una decisión allow/deny al recurso donde está definida; puede incluir restricciones. Por ejemplo: permitir `jcr:modifyProperties` al grupo editorial en `/content/training-permissions/guides`.

| Privilegio | Operación que expresa |
|---|---|
| `jcr:read` | Leer nodos y propiedades ordinarios. |
| `jcr:modifyProperties` | Añadir, cambiar o quitar propiedades ordinarias. |
| `jcr:addChildNodes` | Añadir nodos hijos. |
| `jcr:removeNode` y `jcr:removeChildNodes` | La eliminación necesita permisos sobre el nodo y su padre. |
| `jcr:write` | Agrega varios privilegios de escritura; supera lo necesario para cambiar una propiedad. |
| `jcr:modifyAccessControl` | Modificar políticas de acceso; no es edición de contenido. |

Las operaciones de Sites pueden requerir más privilegios que un cambio de propiedad, según la acción y los tipos de nodo. No traduzcas “editor” a `jcr:all`. [Privilegios JCR — especificación](https://developer.adobe.com/experience-manager/reference-materials/spec/jcr/2.0/16_Access_Control_Management.html).

El resultado efectivo considera principales del usuario y sus grupos, entradas locales/heredadas y restricciones. En el modelo por defecto de Oak, las entradas de usuario tienen precedencia sobre las de grupo; dentro del mismo tipo importan proximidad y orden. Por eso **“deny siempre gana” no es una regla general correcta**. Para diagnosticar, examina el caso concreto. [Evaluación de permisos — Oak](https://jackrabbit.apache.org/oak/docs/security/permission/evaluation.html).

Una concesión estrecha tampoco revoca otra más amplia. Si el usuario pertenece a un grupo que escribe en todo `/content`, permitir edición sólo en `guides` no limita esa otra autorización. No añadas denegaciones globales para ocultar una membresía incorrecta.

<a id="ejemplos-locales"></a>
## 3. Ejemplo completo en Author local

### A. Punto de partida independiente

Necesitas un SDK Author local, una cuenta administradora para preparar la demo y un proyecto WKND o Archetype con `ui.config`. No necesitas Cloud Manager ni las páginas de las sesiones 26 y 27.

1. Inicia sesión como administrador en `http://localhost:4502`.
2. Comprueba que `/content/training-permissions` y los IDs `training-guide-editors`, `training-guide-reader`, `training-permissions-demo` no correspondan a trabajo ajeno. Usa otro prefijo en todo el ejemplo si ya existen.
3. Conserva la sesión de administración separada de la del usuario de prueba. No uses `admin` para demostrar mínimo privilegio.
4. La demo creará dos carpetas `sling:Folder`: `guides` y `outside`. No son páginas ni aparecerán como páginas editables de Sites.

### B. Leer el script completo

[Descargar permissions.repoinit](examples/session-28/permissions.repoinit)

```text
create path (sling:Folder) /content/training-permissions
create path (sling:Folder) /content/training-permissions/guides
create path (sling:Folder) /content/training-permissions/outside

create group training-guide-editors
create service user training-guide-reader with forced path system/cq:services/training

set ACL for training-guide-editors
    allow jcr:read on /content/training-permissions
    allow jcr:modifyProperties on /content/training-permissions/guides
end

set ACL for training-guide-reader
    allow jcr:read on /content/training-permissions/guides
end
```

El grupo recibe lectura en la raíz del ejemplo y modificación de propiedades en `guides`. `outside` es un hermano, por lo que esa concesión de modificación no se hereda allí. La ACL del service user concede lectura en `guides`; su acceso efectivo debe revisarse según el modo de autenticación utilizado. No afirmamos que sea incapaz de leer cualquier otro recurso por el solo hecho de tener esta regla.

Usamos **ACL basadas en recursos** (`set ACL`), almacenadas en los recursos objetivo. No las confundas con `set principal ACL` o `ensure principal ACL`: son instrucciones para otro modelo de políticas. Aquí no hacen falta para enseñar el alcance del permiso. [Control de acceso basado en recursos — Oak](https://jackrabbit.apache.org/oak/docs/security/accesscontrol/default.html).

`create path` permite usar el ejemplo con parsers antiguos del SDK: crea los nodos que faltan, sin cambiar el tipo de los existentes. Sling actual lo considera obsoleto y recomienda `ensure nodes`, que comprueba/ajusta el estado con semántica distinta. No reemplaces la instrucción sin revisar la versión del bundle y sus tipos de nodo. [Repo Init y compatibilidad — Sling](https://sling.apache.org/documentation/bundles/repository-initialization.html).

### C. Instalar la configuración

Copia el archivo completo en tu proyecto WKND:

`ui.config/src/main/content/jcr_root/apps/wknd/osgiconfig/config.author/org.apache.sling.jcr.repoinit.RepositoryInitializer~training-permissions.cfg.json`

[Descargar configuración JSON](examples/session-28/ui.config/src/main/content/jcr_root/apps/wknd/osgiconfig/config.author/org.apache.sling.jcr.repoinit.RepositoryInitializer~training-permissions.cfg.json)

```json
{
  "scripts": [
    "create path (sling:Folder) /content/training-permissions\ncreate path (sling:Folder) /content/training-permissions/guides\ncreate path (sling:Folder) /content/training-permissions/outside\n\ncreate group training-guide-editors\ncreate service user training-guide-reader with forced path system/cq:services/training\n\nset ACL for training-guide-editors\n    allow jcr:read on /content/training-permissions\n    allow jcr:modifyProperties on /content/training-permissions/guides\nend\n\nset ACL for training-guide-reader\n    allow jcr:read on /content/training-permissions/guides\nend\n"
  ]
}
```

1. Para Archetype, cambia `/apps/wknd` por la raíz de aplicación de tu proyecto y conserva el PID y el sufijo de instancia `~training-permissions`. El árbol `/content/training-permissions` puede mantenerse.
2. `scripts` contiene **un string con el script entero**. Los `\n` son saltos de línea escapados en JSON; no separes las líneas de un bloque ACL en scripts independientes.
3. Usa el perfil Maven local de tu baseline para construir e instalar. En un WKND estándar suele ser `mvn clean install -PautoInstallSinglePackage`, ejecutado desde la raíz del **proyecto AEM**, no desde este repositorio de formación. Conserva las opciones Java/SDK y autenticación documentadas por tu baseline.
4. En [OSGi Configuration Manager local](http://localhost:4502/system/console/configMgr), busca `org.apache.sling.jcr.repoinit.RepositoryInitializer` y la instancia `training-permissions`. Comprueba el script efectivo sin guardar cambios manuales adicionales.
5. Revisa `crx-quickstart/logs/error.log` si faltan nodos o identidades: busca `repoinit`, `RepositoryInitializer` y los IDs del ejemplo. La presencia del archivo en `/apps` no demuestra que el script se haya aplicado.

El directorio `config.author` limita esta configuración a Author. En Cloud se distribuye como código mediante el pipeline del proyecto; no se propone editar producción desde una consola. [Configuración OSGi — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi), [Repo Init en despliegues — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/overview#repoinit).

### D. Inspeccionar identidades y ACL

1. En [CRXDE Lite local](http://localhost:4502/crx/de/index.jsp), abre `/content/training-permissions` y sus dos carpetas. Confirma sus tipos `sling:Folder`.
2. En **Tools → Security → Groups**, busca `training-guide-editors`.
3. En **Tools → Security → Users**, busca `training-guide-reader`. También puedes inspeccionar `/home/users/system/cq:services/training` en CRXDE. Verifica que la identidad creada sea `rep:SystemUser`. Su ubicación organiza la identidad, no concede permisos sobre contenido.
4. En **Tools → Security → Permissions**, busca el grupo y comprueba sus dos entradas: lectura en la raíz y modificación en `guides`. Busca el service user y su entrada de lectura en `guides`.
5. Cuando tu SDK tenga **Node View**, selecciona las rutas y revisa también las ACL de sus antecesores. En **Audit View** o la vista filtrada equivalente, selecciona usuario/ruta e incluye las membresías de grupo. Los nombres y disponibilidad de estas vistas dependen del SDK.

La vista por principal lista entradas asignadas; por sí sola no es una ejecución con esa identidad. Si tu SDK no tiene Audit View, inspecciona ACL y antecesores mediante el panel **Access Control** de CRXDE; identifica los principales de cada entrada y las membresías por separado. No presentes esa inspección como una prueba de guardado. [Vistas de permisos — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/security/touch-ui-principal-view).

### E. Comprobar el alcance con una persona local

1. Como administrador, abre **Tools → Security → Users → Create User** y crea `training-permissions-demo`. Define una contraseña local fuera de los archivos del curso.
2. Añádelo a `training-guide-editors` desde la administración del usuario/grupo y guarda. No lo añadas a `administrators`, `content-authors` ni a otro grupo con escritura; revisa también membresías automáticas y `everyone`.
3. Inspecciona sus ACL aplicables en `guides` y `outside`. Usa esta matriz para anticipar la operación, antes de intentarla.

| Identidad | Operación | Ruta | Expectativa en el fixture sin otros grants de escritura |
|---|---|---|---|
| `training-permissions-demo` | Leer | `/content/training-permissions/guides` | Permitido. |
| `training-permissions-demo` | Modificar una propiedad | `/content/training-permissions/guides` | Permitido. |
| `training-permissions-demo` | Modificar una propiedad | `/content/training-permissions/outside` | Denegado. |

**Comprobación operativa, si CRXDE está accesible al usuario local:** abre un perfil/ventana privada, inicia sesión explícitamente como `training-permissions-demo` y verifica la identidad mostrada. En CRXDE, selecciona `guides`, añade la propiedad String `trainingNote` con valor `demo` y pulsa **Save All**. Debe guardarse. Selecciona `outside`, intenta añadir la misma propiedad y guardar: debe fallar por autorización. Descarta/refresca los cambios pendientes después del fallo. Desde la sesión administradora comprueba que la propiedad existe sólo en `guides`.

Si CRXDE o sus recursos de interfaz no están accesibles a esa identidad, no amplíes los permisos para forzar la demo. Completa la inspección de ACL y deja la ejecución como pendiente; el instructor puede mostrar su SDK preparado. Un bloqueo de interfaz no demuestra por sí solo una ACL de escritura incorrecta. Tampoco un HTTP 403 identifica automáticamente la causa: la sesión 29 separará identidad, ACL y protección HTTP.

**Resultados esperados, no ejecución registrada:** el material no se instaló en tu SDK durante su preparación. Una operación inesperadamente permitida requiere revisar otras concesiones. Una operación inesperadamente denegada requiere revisar identidad, aplicación del script, ruta y restricciones. No se “corrige” dando privilegios de administrador.

### F. Repetición y cambios posteriores

Reinstala la misma configuración y comprueba que conservas los mismos IDs y entradas previstas. La intención de Repo Init es declarar un estado repetible, pero no es un reconciliador que borre todo lo que ya no aparece. Quitar un `allow` del archivo o desinstalar la configuración **no garantiza revocar la ACE existente**. La retirada requiere una modificación explícita y revisada de las reglas que posea tu aplicación, seguida de la misma comprobación de alcance.

No incluyas un borrado de `/content` ni de ACL compartidas en una “limpieza”. Para repetir desde cero utiliza otro prefijo de demo o un SDK desechable. Conserva las identidades y permisos de otras funcionalidades.

<a id="repaso"></a>
## 4. Repaso con respuestas

**Una persona entra en Cloud Author, pero no puede editar una página. ¿Contradice el acceso IMS?** No. Autenticación/acceso al entorno y permiso sobre esa operación son comprobaciones distintas.

**El grupo sólo tiene escritura en `guides`, pero el usuario también escribe en `outside`. ¿Qué revisarías primero?** La identidad real, todos sus grupos y las ACL heredadas o asignadas directamente; esa regla no revoca otras concesiones.

**¿Por qué `jcr:write` es excesivo para esta demo?** El requisito es modificar propiedades. El agregado incluye operaciones adicionales que no necesitamos conceder.

**¿El service user ya puede usarse porque aparece en Users?** Su identidad existe. El código necesita el mapping y el mecanismo de autenticación adecuados, además de permisos; se trabajan en la 29.

**¿Eliminar una línea del script retira automáticamente su permiso?** No. Hay que diseñar y verificar una retirada explícita del permiso existente.

**¿Qué demuestra la tabla de permisos?** Ayuda a explicar el resultado esperado. La operación realizada con la identidad correcta aporta la comprobación operativa; no debemos confundir ambas evidencias.

## Referencias oficiales

- [IMS y acceso a AEM Cloud](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/security/ims-support).
- [Service users](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/developing/advanced/service-users).
- [Administración de permisos](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/security/touch-ui-principal-view).
- [Repo Init: lenguaje y versiones](https://sling.apache.org/documentation/bundles/repository-initialization.html).
- [Evaluación de permisos Oak](https://jackrabbit.apache.org/oak/docs/security/permission/evaluation.html).
