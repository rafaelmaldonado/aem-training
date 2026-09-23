# Sesión 29 · Acceder al repositorio con la identidad correcta

**Jueves 24 de septiembre de 2026 · Semana 6 · Núcleo de 30 minutos, ampliable a 60**

[Versión HTML](session-29-study-guide.html) · [Slides en inglés](../lessons/0029-resource-resolver-identity.html#slide-deck) · [Ejemplo local](#ejemplos-locales)

Un `ResourceResolver` permite trabajar con recursos bajo un contexto de acceso. Elegirlo también significa elegir qué permisos se aplican. En una acción del usuario, el resolver de la petición conserva ese contexto; en una tarea técnica independiente, un service resolver usa los principales configurados para el servicio. Sustituir uno por otro para conseguir que una lectura funcione puede exponer contenido que el solicitante no tenía permitido consultar.

Esta sesión conecta la identidad y la ACL de la sesión 28 con una clase Java pequeña. Un mapping relaciona el bundle que pide el acceso con un subservice y un principal; el código obtiene un resolver propio, lee una carpeta fija y lo cierra. Separaremos los fallos de autenticación del servicio, de lectura del recurso y de protección HTTP. El instructor suministra el fixture completo: no hace falta haber realizado una práctica anterior.

- El resolver de la petición conserva el acceso del solicitante; Sling administra su cierre.
- Un service resolver sirve a una tarea técnica concreta; quien lo crea debe cerrarlo.
- El mapping combina **Bundle-SymbolicName, subservice y principal**, con nombres exactos.
- El mapping selecciona identidad; las ACL autorizan operaciones sobre recursos.
- Devuelve valores independientes del resolver, no recursos que dependan de él después del cierre.
- Un HTTP 403 necesita diagnóstico de la capa que rechaza la petición antes de tocar permisos.

## Recorrido de la sesión

| Minutos | Slides | Contenido |
|---|---|---|
| 0–6 | 1–3 | Elegir identidad y reconocer un resolver prestado. |
| 6–13 | 4–6 | Mapping, permisos y ciclo de vida. |
| 13–23 | 7–9 | Leer el ejemplo e inspeccionar configuración y fallos. |
| 23–27 | 10 | Separar CSRF de autorización del repositorio. |
| 27–30 | 11–12 | Key takeaways y preguntas. |

Para ampliar a 60 minutos: 20 de instalación y lectura guiada del log, y 10 de preguntas. Es material de consulta y demostración; no añade entrega ni práctica obligatoria por sesión. El viernes se retoma la práctica semanal con participación voluntaria.

<a id="identidad"></a>
## 1. Elegir el contexto de acceso

| Situación | Resolver apropiado | Propiedad del cierre |
|---|---|---|
| Un servlet o Sling Model lee contenido para la persona que hace la petición. | `request.getResourceResolver()` o resolver recibido del contexto. | Prestado: no lo cierres. |
| Un trabajo técnico sin petición necesita leer una ruta delimitada. | `ResourceResolverFactory.getServiceResourceResolver(authInfo)`. | Propio: ciérralo con `try-with-resources`. |
| Un helper recibe un resolver como parámetro. | Usa el recibido bajo el contrato del caller. | El helper no adquiere su propiedad al recibirlo. |

Una operación privilegiada disparada por HTTP requiere autorización explícita del solicitante y validación de los datos antes del acceso técnico. Que el service user pueda leer una ruta no autoriza al usuario a obtener su contenido. Este ejemplo se activa como componente OSGi local y no publica un servlet privilegiado.

El resolver y sus recursos no se deben compartir entre peticiones o hilos. No guardes un resolver en un campo de un servicio singleton. Un `Resource`, un iterador o un objeto adaptado pueden depender de su ciclo de vida: copia el dato necesario dentro del bloque. Adaptar el resolver a una `Session` no crea otra sesión de tu propiedad; no hagas `logout()` sobre esa sesión prestada. [Contrato de ResourceResolver — Sling](https://sling.apache.org/apidocs/sling12/org/apache/sling/api/resource/ResourceResolver.html).

<a id="mapping"></a>
## 2. Los tres nombres del mapping

```text
wknd.core:training-guide-read=[training-guide-reader]
```

| Parte | Significado | Dónde comprobarla |
|---|---|---|
| `wknd.core` | Nombre simbólico del bundle que obtiene el factory y solicita el resolver. | Manifest `Bundle-SymbolicName` y consola local de bundles. |
| `training-guide-read` | Subservice: una tarea del bundle. | Constante usada con `ResourceResolverFactory.SUBSERVICE`. |
| `[training-guide-reader]` | Lista de nombres de principales de service users. | Identidad creada con Repo Init y propiedad `rep:principalName`. |

No uses el package Java, el nombre visible del bundle ni su ID numérico como sustitutos del nombre simbólico. La configuración se añade con el factory PID `org.apache.sling.serviceusermapping.impl.ServiceUserMapperImpl.amended` y la propiedad `user.mapping`. La documentación de Sling describe también fallbacks; no dependas de un mapping global para ocultar un error de nombre. [Service Authentication — Sling](https://sling.apache.org/documentation/the-sling-engine/service-authentication.html).

El formato con corchetes realiza login por principales y no expande membresías de grupos, incluido `everyone`. Declara directamente los permisos necesarios para los principales mapeados. El formato antiguo sin corchetes mapea por ID y está obsoleto. [Buenas prácticas de mappings — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/security/best-practices-for-sling-service-user-mapping-and-service-user-definition).

**Login por principales y ACL basada en principales no son lo mismo.** El primero define cómo se forma la identidad; la segunda es un modelo de política. Podemos usar el mapping con corchetes y la ACL basada en recursos (`set ACL`) que ya concede lectura a `training-guide-reader` en la sesión 28. No hay que cambiarla por `set principal ACL` para realizar esta demostración.

<a id="ejemplos-locales"></a>
## 3. Ejemplo completo en Author local

### A. Preparar un punto de partida independiente

1. Usa un SDK Author local en `http://localhost:4502` y un proyecto WKND o Archetype que ya compile. Los archivos siguientes van en ese proyecto AEM, no se compilan como un reactor desde el repositorio del curso.
2. Comprueba que las rutas e identidades `training-permissions` y `training-guide-reader` no pertenezcan a otro trabajo. Si hay colisión, cambia el prefijo de forma coherente en Java, Repo Init y mapping.
3. Instala la [configuración Repo Init suministrada en la sesión 28](examples/session-28/ui.config/src/main/content/jcr_root/apps/wknd/osgiconfig/config.author/org.apache.sling.jcr.repoinit.RepositoryInitializer~training-permissions.cfg.json). No exige una entrega previa: el archivo crea el árbol y la identidad. [Script legible](examples/session-28/permissions.repoinit) y [pasos de instalación](session-28-study-guide.html#ejemplos-locales).
4. Como administrador, comprueba en CRXDE local que existe `/content/training-permissions/guides`, de tipo `sling:Folder`, y que `training-guide-reader` es un `rep:SystemUser` con `jcr:read` asignado directamente en esa ruta. No es una página de Sites.
5. Para el resultado inicial no necesitas añadir propiedades: el lector devolverá `guides` si no existe `jcr:title`. Opcionalmente, como administrador local, añade `jcr:title` de tipo String con valor `Training guides` y guarda para ver el otro caso.

No crees contraseñas para el service user ni uses un resolver administrativo. La cuenta administradora prepara el fixture; la lectura de la clase usa el mapping.

### B. Añadir el mapping y habilitar la demo sólo en Author

Copia los dos JSON en `ui.config/src/main/content/jcr_root/apps/wknd/osgiconfig/config.author/`.

**Mapping:** `org.apache.sling.serviceusermapping.impl.ServiceUserMapperImpl.amended~training-guide-reader.cfg.json`

[Descargar org.apache.sling.serviceusermapping.impl.ServiceUserMapperImpl.amended~training-guide-reader.cfg.json](examples/session-29/ui.config/src/main/content/jcr_root/apps/wknd/osgiconfig/config.author/org.apache.sling.serviceusermapping.impl.ServiceUserMapperImpl.amended~training-guide-reader.cfg.json)

```json
{
  "user.mapping": [
    "wknd.core:training-guide-read=[training-guide-reader]"
  ]
}
```

**Activación de la demo:** `com.adobe.aem.guides.wknd.core.training.TrainingGuideReader.cfg.json`

[Descargar com.adobe.aem.guides.wknd.core.training.TrainingGuideReader.cfg.json](examples/session-29/ui.config/src/main/content/jcr_root/apps/wknd/osgiconfig/config.author/com.adobe.aem.guides.wknd.core.training.TrainingGuideReader.cfg.json)

```json
{}
```

El segundo archivo es intencionalmente vacío: su presencia satisface `ConfigurationPolicy.REQUIRE`. Sin esa configuración el componente de demostración no se activa. `config.author` limita ambas configuraciones a Author. Para Archetype cambia la raíz `/apps/wknd`, el package Java y el nombre del PID de la clase; cambia también `wknd.core` por el nombre simbólico real. Conserva el subservice idéntico en Java, la referencia DS y el mapping.

### C. Clase Java completa

Copia el archivo en `core/src/main/java/com/adobe/aem/guides/wknd/core/training/TrainingGuideReader.java`.

[Descargar TrainingGuideReader.java](examples/session-29/core/src/main/java/com/adobe/aem/guides/wknd/core/training/TrainingGuideReader.java)

```java
package com.adobe.aem.guides.wknd.core.training;

import java.util.Collections;
import org.apache.sling.api.resource.LoginException;
import org.apache.sling.api.resource.Resource;
import org.apache.sling.api.resource.ResourceResolver;
import org.apache.sling.api.resource.ResourceResolverFactory;
import org.apache.sling.serviceusermapping.ServiceUserMapped;
import org.osgi.service.component.annotations.Activate;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.ConfigurationPolicy;
import org.osgi.service.component.annotations.Reference;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Component(service = TrainingGuideReader.class, immediate = true,
    configurationPolicy = ConfigurationPolicy.REQUIRE,
    reference = @Reference(name = "serviceMapping", service = ServiceUserMapped.class,
        target = "(subServiceName=training-guide-read)"))
public class TrainingGuideReader {
    private static final Logger LOG = LoggerFactory.getLogger(TrainingGuideReader.class);
    private static final String PATH = "/content/training-permissions/guides";

    @Reference
    ResourceResolverFactory resolverFactory;

    public String readWithService() throws LoginException {
        try (ResourceResolver resolver = resolverFactory.getServiceResourceResolver(
                Collections.singletonMap(ResourceResolverFactory.SUBSERVICE, "training-guide-read"))) {
            return readWith(resolver);
        }
    }

    // Borrowed resolver: its caller owns the lifecycle.
    public String readWith(ResourceResolver resolver) {
        Resource resource = resolver.getResource(PATH);
        if (resource == null) {
            throw new IllegalStateException("Folder missing or unreadable: " + PATH);
        }
        return resource.getValueMap().get("jcr:title", resource.getName());
    }

    @Activate
    protected void activate() {
        try {
            LOG.info("Training guide title: {}", readWithService());
        } catch (LoginException e) {
            LOG.error("Training service login failed; inspect mapping and principal", e);
        } catch (IllegalStateException e) {
            LOG.error("Training read failed; inspect fixture and read permissions", e);
        }
    }
}
```

`readWithService()` crea y cierra su resolver. `readWith()` recibe uno prestado y no lo cierra: se puede invocar con el resolver de una petición cuando la operación debe respetar al solicitante. Ambos leen únicamente la carpeta fija; no reciben rutas arbitrarias de HTTP. Devuelven un String ya obtenido dentro del alcance válido.

La referencia obligatoria `ServiceUserMapped` retrasa la activación hasta que el mapping esté disponible. Si está ausente o inválido, el componente puede permanecer **unsatisfied** sin entrar en `activate()`: no esperes necesariamente una `LoginException` en el log. Si el login falla al ejecutar una llamada, el método público propaga la excepción; el disparador de demo la registra. Una carpeta inexistente o invisible causa otro mensaje y no se transforma en una lectura elevada. [Ejemplo de ServiceUserMapped — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/developing/advanced/service-users).

### D. Construir, instalar y observar

1. Ejecuta la construcción local de tu baseline desde la raíz del proyecto AEM. En WKND estándar suele ser `mvn clean install -PautoInstallSinglePackage`; conserva las versiones Java/SDK, perfiles y autenticación propios del proyecto.
2. En [Bundles local](http://localhost:4502/system/console/bundles), abre el bundle core y confirma su estado Active y `Bundle-SymbolicName`. Compáralo con `wknd.core` en el JSON.
3. En [Configuration Manager local](http://localhost:4502/system/console/configMgr), comprueba la instancia del mapping y la configuración de `TrainingGuideReader`. Inspecciona sin introducir cambios manuales que diverjan de los archivos.
4. En [Components local](http://localhost:4502/system/console/components), busca `com.adobe.aem.guides.wknd.core.training.TrainingGuideReader`. Si falta, revisa instalación y metadatos DS. Si está unsatisfied, revisa configuración requerida, `resolverFactory` y `serviceMapping`.
5. Busca `TrainingGuideReader` en `crx-quickstart/logs/error.log`. Si el logger permite INFO, el resultado esperado es `Training guide title: guides` o el título preparado. Si INFO está filtrado, usa un logger local para ese package siguiendo la [guía 23](session-23-study-guide.html#ejemplos-locales).
6. Para repetir la lectura, deshabilita y vuelve a habilitar **sólo este componente de demo** en Components local. Su activación lee una vez; no es un scheduler ni vuelve a ejecutarse automáticamente al editar la carpeta.

**Resultados esperados, no ejecución registrada en tu instancia.** Un componente Active no demuestra éxito de lectura: la demo captura y registra sus errores. Revisa el mensaje y el fixture. No hay despliegue Cloud ni edición de configuración en producción en estos pasos.

### E. Reconocer los fallos sin ampliar privilegios

| Síntoma | Comprobación concreta | Evita |
|---|---|---|
| Componente unsatisfied | Configuración requerida, mapping, nombre simbólico y principal existente. | Añadir acceso global para que arranque. |
| `LoginException` al obtener resolver | Mapping efectivo del bundle/subservice, identidad y disponibilidad del proveedor. | Fallback a admin o a otra cuenta. |
| `Folder missing or unreadable` | Administrador comprueba existencia; revisa ACL del principal técnico sobre la ruta exacta. | Interpretar `null` como prueba de inexistencia. |
| Error de persistencia en otra funcionalidad | Identidad, operación, privilegios, restricciones y causa de la excepción. | Conceder `jcr:all` sin identificar la operación. |
| HTTP 403 | Método, URL, identidad de la petición, log del filtro/handler y capa de respuesta. | Dar por hecho que siempre es ACL o siempre CSRF. |

Para una demostración negativa en un SDK desechable, cambia temporalmente en el mapping el principal a `training-guide-reader-missing`, instala y observa `serviceMapping` insatisfecha; después restaura el JSON original. Comprueba antes que ese principal no existe y que no hay mappings duplicados para la misma clave. No cambies permisos ni elimines identidades para provocar el fallo.

La [prueba de cierre incluida](examples/session-29/core/src/test/java/com/adobe/aem/guides/wknd/core/training/TrainingGuideReaderTest.java) usa dobles de las APIs; comprueba que el resolver creado se cierre y que el prestado permanezca abierto, pero no valida ACL reales:

```java
package com.adobe.aem.guides.wknd.core.training;

import org.apache.sling.api.resource.Resource;
import org.apache.sling.api.resource.ResourceResolver;
import org.apache.sling.api.resource.ResourceResolverFactory;
import org.apache.sling.api.resource.ValueMap;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.argThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class TrainingGuideReaderTest {
    @Test
    void closesOnlyTheResolverItCreates() throws Exception {
        ResourceResolverFactory factory = mock(ResourceResolverFactory.class);
        ResourceResolver resolver = mock(ResourceResolver.class);
        Resource resource = mock(Resource.class);
        ValueMap values = mock(ValueMap.class);
        when(factory.getServiceResourceResolver(argThat(this::usesExpectedSubservice))).thenReturn(resolver);
        when(resolver.getResource("/content/training-permissions/guides")).thenReturn(resource);
        when(resource.getValueMap()).thenReturn(values);
        when(values.get("jcr:title", "guides")).thenReturn("Training guides");
        when(resource.getName()).thenReturn("guides");

        TrainingGuideReader reader = new TrainingGuideReader();
        reader.resolverFactory = factory;

        assertEquals("Training guides", reader.readWithService());
        verify(resolver).close();
    }

    @Test
    void leavesBorrowedResolverOpen() {
        ResourceResolver resolver = mock(ResourceResolver.class);
        Resource resource = mock(Resource.class);
        ValueMap values = mock(ValueMap.class);
        when(resolver.getResource("/content/training-permissions/guides")).thenReturn(resource);
        when(resource.getValueMap()).thenReturn(values);
        when(resource.getName()).thenReturn("guides");
        when(values.get("jcr:title", "guides")).thenReturn("guides");

        assertEquals("guides", new TrainingGuideReader().readWith(resolver));
        verify(resolver, never()).close();
    }

    private boolean usesExpectedSubservice(Map<String, Object> authInfo) {
        return "training-guide-read".equals(authInfo.get(ResourceResolverFactory.SUBSERVICE));
    }
}
```

La ACL efectiva necesita comprobarse en el SDK. El método de lectura no escribe ni llama a `commit()`. En código que sí escribe, `close()` libera recursos pero **no sustituye a `commit()`**.

<a id="csrf"></a>
## 4. Un 403 no identifica por sí solo el problema

CSRF protege peticiones HTTP de escritura autenticadas bajo la configuración aplicable. Se obtiene un token de `/libs/granite/csrf/token.json` con la misma sesión y se envía recién obtenido mediante `CSRF-Token`. GET no necesita ese token. Una petición puede ser rechazada antes de que se ejecute el servlet; un token válido tampoco concede permisos de repositorio. [Protección CSRF y fetch — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/developing/advanced/csrf-protection).

Para explicarlo en clase, usa la pestaña Network del navegador con una acción normal de Author sobre contenido de demo. Inspecciona método, URL, identidad de sesión, obtención del token y status. Correlaciona con `error.log`: un mensaje de `com.adobe.granite.csrf.impl.CSRFFilter` que rechaza el token apunta a esa capa. No compartas el valor del token ni la cookie.

Si no aparece ese mensaje, revisa otras capas: Sling Referrer Filter, autorización del endpoint o, si existe un proxy, Dispatcher/CDN. El SDK directo en el puerto 4502 permite estudiar AEM sin ese proxy. Esta sesión no requiere implementar un POST ni desactivar filtros. El lector OSGi no pasa por HTTP, por lo que un problema de su mapping no se resuelve enviando un token CSRF.

<a id="repaso"></a>
## 5. Repaso con respuestas

**El request resolver no ve una página. ¿Reintentarías con el service user?** No por defecto: alteraría la identidad y podría exponer contenido. Primero determina si el usuario está autorizado y si la operación requiere realmente privilegios técnicos.

**El subservice coincide, pero el componente queda unsatisfied. ¿Qué falta revisar?** El nombre simbólico del bundle, el principal, las configuraciones efectivas y las referencias DS; el subservice es sólo una parte de la clave.

**¿Por qué no basta con añadir el service user a un grupo lector?** El login por principales del mapping con corchetes no expande esos grupos. Declara el permiso directamente para el principal utilizado.

**¿Quién cierra el resolver que recibe `readWith()`?** Su propietario. Si procede de la petición, lo administra Sling; si el caller lo creó, ese caller lo cierra.

**¿Un token CSRF válido elimina un error de escritura por ACL?** No. Son controles distintos y pueden fallar en momentos diferentes.

**¿Se puede devolver un Resource y cerrar antes de usarlo?** No es un contrato seguro. Copia los valores necesarios antes del cierre, como el String del ejemplo.

## Referencias oficiales

- [ResourceResolver: ciclo de vida y recursos — Sling](https://sling.apache.org/apidocs/sling12/org/apache/sling/api/resource/ResourceResolver.html).
- [ResourceResolverFactory — Sling](https://sling.apache.org/apidocs/sling12/org/apache/sling/api/resource/ResourceResolverFactory.html).
- [Service Authentication — Sling](https://sling.apache.org/documentation/the-sling-engine/service-authentication.html).
- [Service users — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/developing/advanced/service-users).
- [Mappings por principales — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/security/best-practices-for-sling-service-user-mapping-and-service-user-definition).
- [Protección CSRF — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/developing/advanced/csrf-protection).
