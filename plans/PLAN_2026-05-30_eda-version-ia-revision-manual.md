# Plan: EDA version IA con revision manual

**Fecha**: 2026-05-30
**Alternativa elegida**: IA genera una primera version del EDA y el equipo la revisa manualmente
**Alternativas descartadas**:
- EDA 100% manual desde cero: descartado porque consume mas tiempo en graficos y tests repetitivos.
- EDA aceptado automaticamente: descartado porque la IA puede sobredimensionar patrones, pasar por alto variables interesantes o proponer conclusiones poco defendibles.
- EDA solo guiado por hipotesis: descartado como unico enfoque porque queremos tambien una exploracion complementaria para detectar cosas que no anticipamos.
**STATUS**: LISTO_PARA_EJECUCION

---

## Fase 0: Insumos validados

- **Objetivo**: Confirmar que el EDA parte de hipotesis humanas y datos preparados.
- **Entregable concreto**: `reports/01_hipotesis.md`, `data/raw/datos.csv`, `notebooks/1. Limpieza de datos.ipynb`.
- **Criterio de aceptacion**: Existen al menos 5 hipotesis escritas por el equipo y el notebook de limpieza corre sin errores.
- **Esfuerzo estimado**: 30 minutos.
- **Dependencias**: limpieza de datos.
- **Agente ejecutor**: humano / ds-dq.

### Tareas

1. Verificar que `reports/01_hipotesis.md` contiene las hipotesis del equipo.
2. Confirmar que las variables mencionadas existen en el dataset.
3. Confirmar que el entorno `.venv` esta seleccionado como kernel.
4. Confirmar que `data/raw/datos.csv` es la fuente usada por el EDA.

## Fase 1: EDA version IA

- **Objetivo**: Generar una primera version tecnica del EDA con graficos, comparaciones y tests.
- **Entregable concreto**: `notebooks/2. EDA guiado por hipotesis.ipynb`.
- **Criterio de aceptacion**: El notebook corre de punta a punta y contiene analisis para cada hipotesis.
- **Esfuerzo estimado**: 1-2 horas.
- **Dependencias**: Fase 0.
- **Agente ejecutor**: ds-explorer / ds-stats.

### Tareas

1. Cargar el dataset raw.
2. Mostrar `df.head()` para verificar lectura.
3. Resumir la distribucion de `Churn`.
4. Para cada hipotesis, generar un grafico adecuado.
5. Para cada hipotesis, aplicar un test estadistico defendible.
6. Reportar p-valor y tamano de efecto.
7. Agregar una exploracion complementaria corta para detectar variables potencialmente interesantes.

## Fase 2: Revision manual del EDA

- **Objetivo**: Revisar criticamente lo generado por IA y separar hallazgos utiles de ruido.
- **Entregable concreto**: anotaciones del equipo sobre que hallazgos conservar, descartar o profundizar.
- **Criterio de aceptacion**: Cada hipotesis queda marcada como confirmada, no confirmada, contraintuitiva o requiere revision.
- **Esfuerzo estimado**: 1-2 horas.
- **Dependencias**: Fase 1.
- **Agente ejecutor**: humano / grill-me.

### Tareas

1. Revisar si cada resultado va en la direccion esperada.
2. Distinguir significancia estadistica de importancia de negocio.
3. Identificar graficos que no aportan o son confusos.
4. Detectar hallazgos contraintuitivos que merecen discusion.
5. Marcar variables que la IA no priorizo pero el equipo considera relevantes.

## Fase 3: Profundizacion selectiva

- **Objetivo**: Mejorar solo los hallazgos que sobreviven a la revision manual.
- **Entregable concreto**: version refinada del EDA o reporte de resultados posterior.
- **Criterio de aceptacion**: Cada conclusion final tiene evidencia, interpretacion de negocio y limitacion.
- **Esfuerzo estimado**: 2-4 horas.
- **Dependencias**: Fase 2.
- **Agente ejecutor**: ds-explorer / ds-stats / humano.

### Tareas

1. Rehacer graficos poco claros.
2. Agregar segmentaciones si una hipotesis lo necesita.
3. Revisar outliers o distribuciones raras donde afecten la interpretacion.
4. Escribir conclusiones en lenguaje de negocio.
5. Actualizar `decisions.md` con decisiones metodologicas nuevas.

---

## Reglas de trabajo

- La IA puede proponer evidencia, pero no decide las conclusiones finales.
- La exploracion complementaria sirve para encontrar pistas, no para inventar hipotesis post hoc sin aclararlo.
- Si un resultado contradice la hipotesis, se conserva como hallazgo posible; no se fuerza la historia original.
- Todo hallazgo que llegue al reporte final debe poder defenderse frente al gerente comercial.

## Handoff

- **Proxima fase**: Fase 2, revision manual del notebook generado.
- **Archivo principal**: `notebooks/2. EDA guiado por hipotesis.ipynb`.
- **Criterio para avanzar**: el equipo decide que hallazgos se profundizan y cuales se descartan.
