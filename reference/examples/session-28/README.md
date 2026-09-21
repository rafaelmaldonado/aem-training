# Sesión 28 · Permisos como código

[Guía completa y pasos en Author local](../../session-28-study-guide.html#ejemplos-locales).

- `permissions.repoinit`: versión legible del script; no se instala por sí sola.
- `ui.config/.../org.apache.sling.jcr.repoinit.RepositoryInitializer~training-permissions.cfg.json`: configuración instalable desde tu proyecto WKND. Su único elemento `scripts` contiene el script completo, incluidos los bloques ACL.
- Para Archetype, cambia sólo `/apps/wknd` por la raíz real del proyecto. El fixture `/content/training-permissions` es independiente del sitio.
- No instala usuarios humanos ni contraseñas. Crea el usuario de demostración manualmente en el SDK.
- La configuración añade permisos; no revoca concesiones previas. Comprueba membresías, ACL heredadas y operaciones dentro/fuera de `guides`.
- `create path` conserva compatibilidad con parsers antiguos; Sling actual recomienda `ensure nodes`. No cambia el tipo de nodos existentes.

El JSON y la sintaxis Repo Init se comprobaron localmente. Las comprobaciones de permisos efectivos y operaciones necesitan ejecutarse en un SDK; no se presentan como resultados medidos.

No es un proyecto Maven completo. Instala el archivo usando el perfil local de tu baseline; no copies estos usuarios de demostración a Cloud.
