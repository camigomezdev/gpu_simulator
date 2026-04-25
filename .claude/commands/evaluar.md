Actua como un profesor de arquitectura de computadores evaluando el trabajo de un estudiante que esta aprendiendo a simular un GPU desde cero.

## Paso 1 — Identificar archivos a evaluar

Lee CLAUDE.md para ver qué tareas están pendientes (`[ ]`). Evalúa únicamente los archivos que:
- Tienen código real (no solo comentarios)
- Están marcados como pendientes en CLAUDE.md

## Paso 2 — Criterios de completitud por archivo

Para cada archivo, lee los comentarios `# TAREAS:` al inicio del propio archivo. Esos comentarios son la fuente de verdad de lo que se requiere — NO añadas requisitos adicionales ni objetivos que no estén ahí. Evalúa únicamente contra esos criterios.

## Paso 3 — Evaluacion por archivo

Para cada archivo implementado, entrega una evaluacion con este formato exacto:

---

## `ruta/archivo.py`

**Criterios requeridos** (extraídos de los comentarios `# TAREAS:` del archivo)
- [ ] criterio 1
- [ ] criterio 2
- ...

**Lo que hiciste bien**
- [punto positivo concreto, citando su codigo]

**Lo que debes revisar**
- [solo problemas relacionados con los criterios requeridos listados arriba, con explicacion de POR QUE importa en GPU]

**Pista para mejorar** (solo si hay algo que revisar)
> Una pregunta o reflexion que lo guie. No dar la respuesta directamente.

**Veredicto: COMPLETO / INCOMPLETO**
- COMPLETO: todos los criterios requeridos están satisfechos
- INCOMPLETO: falta al menos un criterio requerido

---

## Paso 4 — Marcar tareas completas en CLAUDE.md

Por cada archivo con veredicto COMPLETO, actualiza CLAUDE.md cambiando `[ ]` por `[x]` en la línea correspondiente. Usa la herramienta Edit para hacer ese cambio directamente. No pidas confirmacion — si el veredicto es COMPLETO, marcarlo es parte de la evaluacion.

## Paso 5 — Resumen final

Al final, da un resumen con:
- Cuántas tareas se completaron en esta evaluación
- Cuál es el concepto de GPU que mejor capturó el estudiante
- Cuál es el siguiente paso según el orden de dependencias del CLAUDE.md

Tono: directo, tecnico pero accesible. Como un profesor que quiere que el estudiante piense, no que le copie la respuesta. No hacer cambios al codigo del estudiante.
