# TP3 - Prediccion de Churn | Grupo 04

Trabajo Practico 3 de Inteligencia Artificial Aplicada a los Negocios (81.91) - ITBA.

El objetivo es predecir que clientes de un e-commerce tienen mayor probabilidad de abandonar la plataforma, y traducir esos resultados en acciones de retencion accionables para el negocio.

## Dataset

- **Fuente:** `data/raw/datos.csv`
- **Registros:** 5630 clientes
- **Variables:** 20 columnas (1 ID + 1 target `Churn` + 18 features)
- **Desbalance:** ~17% clase positiva (churn = 1)

## Estructura del repositorio

```
data/
  raw/           # Dataset original sin modificar
  processed/     # Dataset limpio con imputacion KNN
    split/       # CSVs de train/test, X/y, indices y resumen del holdout
    features_train.parquet  # Features transformadas para modelado
    features_test.parquet   # Features transformadas para modelado
notebooks/
  1. Limpieza de datos.ipynb          # Auditoria de calidad e imputacion
  2. EDA guiado por hipotesis.ipynb   # Validacion de 6 hipotesis de negocio
  3. Training.ipynb                   # Split train/test y preparacion para modelado
src/
  features/
    pipeline.py  # Pipeline reproducible de feature engineering
outputs/
  eda/           # Graficos generados por el EDA
reports/
  00_contexto_negocio.md  # Pregunta de negocio y criterio de exito
  01_hipotesis.md         # Hipotesis escritas por el equipo antes del EDA
  02_data_quality.md      # Auditoria de calidad del dataset
  03_eda.md               # Resumen de hallazgos: fuertes, moderados, contraintuitivos
  feature_report.md       # Transformaciones aplicadas para modelado
  handoff_to_modeler.md   # Contrato para la etapa de modelos
decisions.md     # Log de decisiones tecnicas y metodologicas
requirements.txt
```

## Como ejecutar

```bash
pip install -r requirements.txt
jupyter notebook
```

Ejecutar los notebooks en orden: primero `1. Limpieza de datos.ipynb`, luego `2. EDA guiado por hipotesis.ipynb` y despues `3. Training.ipynb`.

## Hallazgos principales del EDA

| Variable | Resultado |
|---|---|
| `Tenure` | Fuerte: mediana de 1 mes en churners vs 10 meses en activos |
| `Complain` | Fuerte: tasa de churn 31.7% con reclamos vs 10.9% sin reclamos |
| `CashbackAmount` | Moderado: cashback menor en clientes que churnearon |
| `OrderCount` | Debil: diferencia estadistica con bajo efecto practico |
| `SatisfactionScore` | Contraintuitivo: se esperaba mayor churn en scores bajos, pero los scores altos muestran mayor tasa de abandono |
| `DaySinceLastOrder` | Contraintuitivo: se esperaba mayor churn con mas dias de inactividad, pero los churners tienen mediana de 2 dias vs 4 dias en activos |

## Entregas

| Fecha | Contenido |
|---|---|
| 05/06 | EDA + repo GitHub |
| 12/06 | Notebook de modelado + `decisions.md` |
| 19/06 | Reporte ejecutivo PDF + defensa oral |
