# Diagnóstico inicial — AEM

Duración: 35 minutos asíncronos antes del Día 1. No tiene calificación y no se permite consultar documentación. Su propósito es ajustar la profundidad del curso sin consumir una sesión.

## 1. Contexto personal — 5 minutos

Cada participante anota:

- principal experiencia: frontend, Java/backend, QA/DevOps u otra;
- años aproximados trabajando con web y con AEM;
- una tarea de AEM que puede realizar sin ayuda;
- una tarea de AEM que todavía no puede realizar;
- acceso disponible: Java, Maven, Git, Node, SDK de AEM y repositorio; Cloud Manager no es requisito.

## 2. Recuperación conceptual — 10 minutos

Responder en una o dos frases, sin buscar definiciones:

1. ¿Qué diferencia práctica existe entre Author y Publish?
2. ¿Qué ocurre desde que el navegador solicita una URL hasta que AEM devuelve HTML?
3. ¿Para qué sirven JCR, Sling y OSGi?
4. ¿Qué responsabilidades tienen HTL, un Sling Model y una client library?
5. ¿Por qué se prefiere extender un Core Component mediante un proxy en vez de copiarlo?
6. ¿Qué debería cachear Dispatcher y qué no debería cachear?

## 3. Lectura de proyecto — 10 minutos

Usar el repositorio real si está disponible; de lo contrario, usar un proyecto de ejemplo. Localizar y explicar brevemente:

- dónde vive un componente;
- dónde está su diálogo;
- cómo encuentra su Sling Model;
- dónde se incluye CSS o JavaScript;
- dónde hay configuración dependiente del ambiente;
- cómo se construye y despliega el proyecto.

No importa completar todos los puntos. Registrar en cuáles necesitó ayuda.

## 4. Cambio práctico — 10 minutos

Elegir una sola opción según el perfil:

- Frontend: describir los archivos y cambios necesarios para agregar una variante visual authorable a un componente existente.
- Backend: escribir o bosquejar la lógica mínima de un Sling Model que expone un título con valor alternativo.
- QA/DevOps: proponer la comprobación mínima para impedir que ese cambio roto llegue a producción.

La respuesta debe incluir cómo comprobarían que funciona y un riesgo que revisarían.

## Lectura del resultado por el instructor

Clasificar cada dimensión por separado, no asignar un nivel único a la persona:

| Dimensión | Necesita apoyo | Puede trabajar acompañado | Puede guiar a otra persona |
|---|---|---|---|
| Web/Git | No puede explicar o localizar lo básico | Resuelve con alguna orientación | Resuelve y justifica decisiones |
| AEM conceptual | Confunde responsabilidades centrales | Traza el flujo con vacíos menores | Traza el flujo y anticipa efectos |
| Especialidad | No completa el cambio | Propone una solución viable | Propone, comprueba y detecta riesgos |
| Entorno | Accesos o herramientas bloqueados | Entorno parcial | Entorno listo para desarrollar |

Usar las dimensiones para adaptar ejemplos, asignar revisores asíncronos y detectar quién necesita acompañamiento. No crear salas o reuniones adicionales.

## Evidencia a conservar

Guardar únicamente la matriz por dimensión, bloqueos de acceso y temas que requieren refuerzo. Transferir ese punto de partida a `reference/seguimiento-evidencias.html`. No conservar una puntuación total: no aporta información útil para adaptar las lecciones.
