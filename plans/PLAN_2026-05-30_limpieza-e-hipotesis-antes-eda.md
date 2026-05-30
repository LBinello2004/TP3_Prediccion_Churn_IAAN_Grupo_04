# Plan: limpieza de datos e hipotesis antes del EDA

**Fecha**: 2026-05-30
**Alternativa elegida**: Limpieza primero, hipotesis humanas despues, EDA recien al final
**Alternativas descartadas**:
- EDA inmediato: descartado porque queremos que las hipotesis las escriba el equipo antes de mirar graficos y tests.
- Hipotesis genericas generadas por IA: descartado porque debilita la defensa oral y no refleja el razonamiento propio del grupo.
- Modelado temprano: descartado porque la consigna prioriza entendimiento, limpieza e hipotesis antes de entrenar modelos.
**STATUS**: LISTO_PARA_EJECUCION

---

## Fase 0: Validacion de estado del proyecto

- **Objetivo**: Confirmar que el proyecto tiene estructura minima, entorno virtual, dataset raw y notebook de limpieza.
- **Entregable concreto**: repo con `.venv`, `requirements.txt`, `data/raw/datos.csv` y `notebooks/1. Limpieza de datos.ipynb`.
- **Criterio de aceptacion**: El notebook de limpieza corre usando el kernel `.venv` y carga `data/raw/datos.csv`.
- **Esfuerzo estimado**: 30 minutos.
- **Dependencias**: ninguna.
- **Agente ejecutor**: humano / ds-dq.

### Tareas

1. Verificar que VS Code/Cursor usa el kernel `.venv`.
2. Confirmar que el CSV raw existe en `data/raw/datos.csv`.
3. Ejecutar `notebooks/1. Limpieza de datos.ipynb`.
4. Confirmar que se genera `data/processed/datos_limpios.csv`.
5. Registrar decisiones efectivas en `decisions.md`.

## Fase 1: Limpieza de datos defendible

- **Objetivo**: Documentar una limpieza reproducible sin perder informacion innecesariamente.
- **Entregable concreto**: `notebooks/1. Limpieza de datos.ipynb` y `reports/02_data_quality.md`.
- **Criterio de aceptacion**: El reporte explica nulos, duplicados, tipos, cardinalidad y por que se imputa en vez de dropear.
- **Esfuerzo estimado**: 1-2 horas.
- **Dependencias**: Fase 0.
- **Agente ejecutor**: ds-dq.

### Tareas

1. Auditar dimensiones, tipos y memoria.
2. Auditar nulos por columna y porcentaje.
3. Auditar duplicados exactos y por `CustomerID`.
4. Auditar cardinalidad de variables categoricas.
5. Aplicar imputacion KNN sobre variables numericas con faltantes.
6. Guardar dataset procesado para uso exploratorio.
7. Documentar limitaciones de esta limpieza.

## Fase 2: Hipotesis escritas por el equipo

- **Objetivo**: Formular hipotesis de negocio propias antes del EDA.
- **Entregable concreto**: `reports/01_hipotesis.md`.
- **Criterio de aceptacion**: El archivo contiene al menos 5 hipotesis redactadas por el equipo, cada una con motivacion de negocio y variable(s) asociadas.
- **Esfuerzo estimado**: 1-2 horas.
- **Dependencias**: Fase 1.
- **Agente ejecutor**: humano.

### Tareas

1. Leer `reports/00_contexto_negocio.md`.
2. Revisar el diccionario de variables del dataset.
3. Escribir hipotesis sin mirar resultados de EDA.
4. Para cada hipotesis, indicar que variable(s) la validarian.
5. Marcar si alguna hipotesis puede tener riesgo de leakage.

## Checkpoint antes del EDA

- **Objetivo**: Evitar que el EDA sea una coleccion de graficos sin pregunta.
- **Entregable concreto**: revision de `reports/01_hipotesis.md`.
- **Criterio de aceptacion**: El equipo confirma que las hipotesis estan listas para testear.
- **Esfuerzo estimado**: 30 minutos.
- **Dependencias**: Fase 2.
- **Agente ejecutor**: humano / grill-me.

### Tareas

1. Revisar si cada hipotesis responde una pregunta de retencion.
2. Eliminar hipotesis tautologicas o demasiado obvias.
3. Separar hipotesis descriptivas de hipotesis predictivas.
4. Elegir prioridad de validacion.

## Fase 3: EDA guiado por hipotesis

- **Objetivo**: Validar las hipotesis escritas por el equipo con graficos, tests e interpretacion de negocio.
- **Entregable concreto**: notebook EDA y reporte de resultados, a crear despues de que `reports/01_hipotesis.md` este listo.
- **Criterio de aceptacion**: Cada hipotesis tiene grafico, test estadistico, p-valor, tamano de efecto e interpretacion.
- **Esfuerzo estimado**: 3-5 horas.
- **Dependencias**: Checkpoint antes del EDA.
- **Agente ejecutor**: ds-explorer / ds-stats.

### Tareas

1. Leer hipotesis finales del equipo.
2. Elegir test estadistico por tipo de variable.
3. Generar graficos solo para responder esas hipotesis.
4. Documentar hallazgos y limitaciones.
5. Actualizar `decisions.md` con decisiones metodologicas nuevas.

---

## Reglas de trabajo

- No generar hipotesis automaticas antes de que el equipo escriba las suyas.
- No avanzar al EDA sin `reports/01_hipotesis.md` revisado.
- Mantener `decisions.md` como memoria viva del proyecto.
- Registrar solo decisiones reales: metodos, supuestos, descartes y riesgos aceptados.

## Handoff

- **Proxima fase**: Fase 2, hipotesis escritas por el equipo.
- **Agente sugerido ahora**: humano.
- **Agente sugerido despues**: ds-explorer + ds-stats, una vez completo `reports/01_hipotesis.md`.
