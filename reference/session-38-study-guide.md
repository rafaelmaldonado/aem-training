# Sesión 38 · Explicar la configuración efectiva

**Miércoles 7 de octubre de 2026 · Semana 8 · 30 minutos**

[Versión HTML](session-38-study-guide.html) · [Slides en inglés](../lessons/0038-effective-configuration.html#slide-deck)

## Objetivo observable

Ante un valor distinto entre SDK local y AEM Cloud, identificar el **PID**, el archivo `.cfg.json` aplicable por run modes, el origen de cada valor y la propiedad efectiva del servicio. Los PIDs, URLs y secretos de las slides son ejemplos inventados. No se necesita acceso a Cloud Manager ni se asigna una práctica.

## Recorrido de 30 minutos

| Minutos | Slides | Acción |
| --- | --- | --- |
| 0–6 | 1–2 | Distinguir PID y nombre de instancia factory. |
| 6–12 | 3 | Elegir un archivo completo por run modes. |
| 12–19 | 4–6 | Separar inline, variable no secreta y secreto; explicar la prueba local. |
| 19–25 | 7–8 | Comparar Preview, Publish, local y Cloud. |
| 25–30 | 9 | Formular diagnóstico y preguntas. |

## 1. Del PID al archivo ganador

Una configuración OSGi en el proyecto usa el nombre `<PID>.cfg.json`; el PID suele ser el nombre completo de la clase del componente. Para una factory configuration, el nombre agrega un identificador de instancia. La carpeta `config`, `config.author`, `config.author.dev` o su equivalente admitido delimita el servicio y ambiente. En Author con `dev`, si el mismo PID aparece en `config.author` y `config.author.dev`, gana el archivo con más run modes coincidentes **para el PID completo**. No se mezclan sus propiedades: si `timeout` sólo está en el archivo menos específico, el ganador no lo hereda. El valor sin definir depende del componente. [Configuración OSGi — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi).

## 2. De los placeholders al valor

| Forma | Uso | Ubicación del valor |
| --- | --- | --- |
| Valor inline | Opción normal para un valor no secreto estable | `.cfg.json` versionado en Git. |
| `$[env:CATALOG_URL]` | Valor no secreto que debe variar entre ambientes de desarrollo o entre Publish y Preview | Variable definida para el ambiente y servicio correspondientes. |
| `$[secret:CATALOG_KEY]` | Clave o contraseña | Secreto fuera de Git. |

En el SDK local, un valor `env` puede venir de una variable del proceso iniciada antes de Java. Un secreto local se puede leer desde un archivo de nombre exacto en el directorio indicado por `org.apache.felix.configadmin.plugin.interpolation.secretsdir` en `sling.properties`. No copies secretos reales a capturas, logs o repositorios. El mecanismo local ayuda a comprender la sustitución; no prueba que la variable esté configurada en Cloud Manager. [Valores OSGi y entorno local — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi) · [Variables de Cloud Manager — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/environment-variables).

Preview hereda la configuración OSGi de Publish; no se crea `config.preview`. El mismo placeholder puede recibir un valor diferente si la variable se define para Preview y Publish por separado. La carpeta responde **qué archivo se seleccionó**; la variable responde **qué valor sustituyó al placeholder**. [Configuración OSGi — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi).

## 3. Caso guiado: local resuelve y Cloud no

**Ficha didáctica inventada:** el SDK con `author,dev` resuelve `CATALOG_URL`, pero en el ambiente Cloud de Author el valor observado difiere o queda sin resolver. El orden de comprobación es:

1. Confirmar el PID exacto y el servicio afectado.
2. Elegir el `.cfg.json` ganador por run modes y comprobar que contiene el placeholder esperado.
3. Consultar la configuración efectiva en AEM Developer Console para el ambiente y tier correctos.
4. Verificar en Cloud Manager que la variable exista para ese ambiente y servicio.
5. Sólo entonces concluir si la diferencia se debe a selección de archivo, variable ausente u otra configuración.

El ejemplo de la slide 08 sugiere una variable faltante, pero esa causa requiere verificar Cloud Manager; valores distintos pueden tener otras causas. Developer Console es de sólo lectura en Cloud. El Web Console del SDK local no es su equivalente editable en producción. [Developer Console — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/aem-developer-console).

## Repaso con respuestas

1. **¿Qué identifica el nombre del archivo?** El PID y, en una factory configuration, su instancia.
2. **¿Se hereda `timeout` desde `config.author` si gana `config.author.dev`?** No; la selección es por archivo completo del mismo PID.
3. **¿Cuándo usar un valor inline?** Para un valor no secreto estable; es la opción normal.
4. **¿Dónde va una API key?** En un secreto referenciado por `$[secret:...]`, fuera de Git.
5. **¿Qué archivo lee Preview?** La configuración de Publish; el valor de la variable puede diferir por servicio.

## Fuentes oficiales

- [Configuring OSGi for AEM as a Cloud Service — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi)
- [Environment Variables in Cloud Manager — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/environment-variables)
- [AEM Developer Console — Adobe](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/aem-developer-console)
