# Feature Engineering Report
**Fecha**: 2026-06-05
**Input**: `data/processed/datos_limpios.csv`
**Modo**: ML
**Output**: `data/processed/features_train.parquet`, `data/processed/features_test.parquet`
**Split**: 4059 train / 1015 test - stratify=True - random_state=42

---

## Objetivo

Preparar datos listos para modelado de churn sin entrenar modelos ni hacer feature selection. El input ya viene de la limpieza con categorias equivalentes estandarizadas.

---

## Columnas Dropeadas

| Columna | Razon |
|---|---|
| `CustomerID` | Identificador, no predictor. |
| `Churn` | Target, se guarda separado. |
| `DaySinceLastOrder` | Warning metodologico: descriptor retroactivo documentado en `decisions.md`; no se usa como predictor confiable para produccion. |

---

## Transformaciones Aplicadas

| Variable original | Transformacion | Tecnica BA (#) | Parametros | Justificacion |
|---|---|---:|---|---|
| Numericas base | `SimpleImputer` + `RobustScaler` | - | mediana; IQR | Hay nulos en variables numericas y posibles outliers; se fitea solo en train. |
| Categoricas nominales | `SimpleImputer` + `OneHotEncoder` | 9 | moda; `handle_unknown='ignore'` | Baja cardinalidad, sin orden natural. |
| `OrderCount`, `CashbackAmount` | `valor_cliente_proxy` | 1 | `OrderCount * CashbackAmount` | Proxy de valor/intensidad comercial respaldado por H8. |
| `CouponUsed`, `OrderCount` | `coupon_per_order` | 1 | `CouponUsed / max(OrderCount, 1)` | Normaliza uso de cupones por actividad. |
| `CashbackAmount`, `OrderCount` | `cashback_per_order` | 1 | `CashbackAmount / max(OrderCount, 1)` | Normaliza incentivo por actividad. |
| `Complain`, `SatisfactionScore` | `complain_x_satisfaction` | 1 | producto | Captura interaccion explorada en H7. |

---

## Imputacion

| Variable | % Null aprox. | Estrategia | Flag creado |
|---|---:|---|---|
| `Tenure` | 4.69% | mediana dentro del pipeline | No |
| `WarehouseToHome` | 4.46% | mediana dentro del pipeline | No |
| `HourSpendOnApp` | 4.53% | mediana dentro del pipeline | No |
| `OrderAmountHikeFromlastYear` | 4.71% | mediana dentro del pipeline | No |
| `CouponUsed` | 4.55% | mediana dentro del pipeline | No |
| `OrderCount` | 4.58% | mediana dentro del pipeline | No |

---

## Artefactos Generados

| Archivo | Contenido |
|---|---|
| `src/features/pipeline.py` | Pipeline reproducible con `build_pipeline()`. |
| `data/processed/split/train.csv` | Filas raw asignadas a train. |
| `data/processed/split/test.csv` | Filas raw asignadas a test. |
| `data/processed/split/X_train.csv` | Features raw de train luego de drops. |
| `data/processed/split/X_test.csv` | Features raw de test luego de drops. |
| `data/processed/split/y_train.csv` | Target de train. |
| `data/processed/split/y_test.csv` | Target de test. |
| `data/processed/features_train.parquet` | Features transformadas de train, 4059 x 38. |
| `data/processed/features_test.parquet` | Features transformadas de test, 1015 x 38. |

---

## Validaciones

- Split antes de cualquier transformacion: OK.
- Categorias equivalentes estandarizadas en `data/processed/datos_limpios.csv`: OK.
- Fit de imputers/encoders/scalers solo sobre train: OK.
- Test transformado solo con `.transform()`: OK.
- Train/test sin nulos post-transformacion: OK.
- Mismas 38 columnas transformadas en train y test: OK.

---

## Warnings para el Modeler

- `Complain` queda incluida, pero debe justificarse temporalmente: si el reclamo ocurre despues del churn o como parte del cierre de cuenta, seria leakage.
- El target esta desbalanceado: churn positivo = 16.84%. Evaluar `class_weight`, PR-AUC, recall y tuning de umbral.
- No se hizo feature selection en esta etapa; corresponde al Modeler.
