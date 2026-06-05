# Handoff to Modeler
**Fecha**: 2026-06-05
**Origen**: `notebooks/3. Training.ipynb`

## Feature Engineering - Resultado Final

**Features disponibles**: 33 columnas transformadas  
**Train shape**: 4504 x 33  
**Test shape**: 1126 x 33  
**Pipeline**: `src/features/pipeline.py` - funcion `build_pipeline()`

## Archivos

| Archivo | Uso |
|---|---|
| `data/processed/features_train.parquet` | X train transformado. |
| `data/processed/features_test.parquet` | X test transformado. |
| `data/processed/target_train.csv` | y train con `CustomerID`. |
| `data/processed/target_test.csv` | y test con `CustomerID`. |
| `data/processed/split/split_summary.csv` | Distribucion del target por split. |
| `data/processed/split/split_indices.csv` | Indices y IDs para reconstruir el holdout. |

## Split

| Split | Churn=0 | Churn=1 | Churn positivo |
|---|---:|---:|---:|
| Train | 3746 | 758 | 16.83% |
| Test | 936 | 190 | 16.87% |

## Features a evaluar para selection

La seleccion final de variables queda para el Modeler. La lista disponible incluye:

- Numericas originales transformadas: `Tenure`, `CityTier`, `WarehouseToHome`, `HourSpendOnApp`, `NumberOfDeviceRegistered`, `SatisfactionScore`, `NumberOfAddress`, `Complain`, `OrderAmountHikeFromlastYear`, `CouponUsed`, `OrderCount`, `CashbackAmount`.
- Features derivadas: `valor_cliente_proxy`, `coupon_per_order`, `cashback_per_order`, `complain_x_satisfaction`.
- Dummies OHE de: `PreferredLoginDevice`, `PreferredPaymentMode`, `Gender`, `PreferedOrderCat`, `MaritalStatus`.
- Categorias estandarizadas en limpieza antes del OHE: `COD -> Cash on Delivery`, `CC -> Credit Card`, `Phone -> Mobile Phone`, `Mobile -> Mobile Phone`.

## Columnas excluidas antes de modelar

| Columna | Razon |
|---|---|
| `CustomerID` | Identificador. |
| `Churn` | Target. |
| `DaySinceLastOrder` | Descriptor retroactivo no confiable como predictor de alerta temprana. |

## Recomendaciones para el Modeler

- Empezar con `DummyClassifier(strategy='most_frequent')` como baseline obligatorio.
- Comparar modelos con CV estratificada usando train; mantener test cerrado hasta la evaluacion final.
- Reportar F1, recall, precision y PR-AUC; no usar accuracy como metrica principal.
- Evaluar `class_weight='balanced'` o estrategia equivalente por el desbalance.
- Tratar `Complain` como warning de posible leakage hasta justificar disponibilidad temporal.
