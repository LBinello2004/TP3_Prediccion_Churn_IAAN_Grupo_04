# Data quality

## Dataset auditado

- Fuente usada para el proyecto: `data/raw/datos.csv`
- Filas: 5630
- Columnas: 20
- Target: `Churn`
- Tasa de churn: 16.84%

## Hallazgos estructurales

- No se detectan faltantes en el target `Churn`.
- No se detectan faltantes en variables categoricas.
- Los faltantes estan concentrados en 7 variables numericas.
- Cada columna con faltantes tiene entre 4.46% y 5.45% de valores ausentes.
- Si se usa `dropna()` se eliminan 1856 filas, equivalente al 32.97% del dataset.

## Columnas con valores faltantes

| Columna | Faltantes | Porcentaje |
|---|---:|---:|
| `DaySinceLastOrder` | 307 | 5.45% |
| `OrderAmountHikeFromlastYear` | 265 | 4.71% |
| `Tenure` | 264 | 4.69% |
| `OrderCount` | 258 | 4.58% |
| `CouponUsed` | 256 | 4.55% |
| `HourSpendOnApp` | 255 | 4.53% |
| `WarehouseToHome` | 251 | 4.46% |

## Decision de limpieza

No se usa `dropna()` como limpieza principal porque descarta casi un tercio de la base. Para una base de churn, esa perdida es demasiado alta: reduce informacion de clientes y puede debilitar el analisis de segmentos.

La limpieza exploratoria usa imputacion KNN para variables numericas, con escalado previo. No se crean columnas adicionales de indicador de faltante para mantener el dataset procesado con la misma estructura conceptual que el raw.

Tambien se estandarizan categorias equivalentes antes de guardar `data/processed/datos_limpios.csv`: `COD` se unifica como `Cash on Delivery`, `CC` como `Credit Card`, `Phone` como `Mobile Phone`, y `Mobile` como `Mobile Phone` en `PreferedOrderCat`.

## Red flags para etapas siguientes

- `Complain` debe tratarse como posible leakage hasta justificar temporalmente si la queja estaba disponible antes de la prediccion.
- `CustomerID` es identificador y no debe usarse como predictor.
- La imputacion para modelado no debe hacerse antes del split train/test. Debe ir dentro de un `Pipeline` para evitar leakage desde test hacia train.
- `CouponUsed`, `OrderCount`, `Tenure`, `WarehouseToHome`, `HourSpendOnApp`, `OrderAmountHikeFromlastYear` y `DaySinceLastOrder` son numericas, pero varias representan conteos o cantidades enteras; despues de KNN se redondean y se acotan a valores no negativos.
- Las categorias equivalentes de medio de pago, dispositivo de login y categoria de orden ya quedan normalizadas en `datos_limpios.csv`, por lo que el EDA no debe contar `COD`/`Cash on Delivery`, `CC`/`Credit Card`, `Phone`/`Mobile Phone` o `Mobile`/`Mobile Phone` como categorias separadas.

## Cierre ds-dq

- Caracterizacion antes de intervenir: realizada.
- Nulos antes y despues: documentados en notebook.
- Duplicados y tipos: incluidos como chequeos en notebook.
- Supuestos de imputacion: documentados.
- Limpieza reproducible: `notebooks/1. Limpieza de datos.ipynb`.
