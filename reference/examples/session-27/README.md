# Sesión 27 · Diagnóstico local

Sigue el [ejemplo completo de la guía](../../session-27-study-guide.html#ejemplos-locales). Incluye preparación desde cero con cinco páginas y tags; no depende de prácticas anteriores.

- `querybuilder.properties`: consulta acotada, dos hits por ventana; pegar en QueryBuilder Debugger.
- `guides.sql2`: selección y orden equivalentes; límite/offset se aplican en la herramienta o API JCR.
- `explain-broad.sql2`: plan de la raíz demasiado amplia; pegar en consola SQL2, sin ejecutar el SELECT por separado.
- `explain-bounded.sql2`: plan de la raíz correcta; misma consola.
- `measure-bounded.sql2`: ejecuta la consulta sobre el conjunto pequeño y devuelve contadores por selector. No incluye un límite de ejecución; usar sólo el fixture descrito.
- `properties-review.json`: fragmento ilustrativo de `indexRules/cq:Page/properties`; para lectura, no es un índice completo ni un paquete instalable.

En Query Performance → Explain Query se pega `guides.sql2` sin el prefijo EXPLAIN, con las opciones de ejecución desmarcadas. En CRXDE → Query se usan directamente los archivos `explain-*.sql2`.

Adapta `/content/wknd/us/en` si tu sitio usa otra raíz. No cambies índices, permisos globales ni opciones de reindexación. Los planes y contadores dependen del SDK; no se incluyen mediciones reales ni promesas de mejora.
