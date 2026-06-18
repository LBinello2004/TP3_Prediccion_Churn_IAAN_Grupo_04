# Predicción de churn en e-commerce

Trabajo Práctico 3 de **Inteligencia Artificial Aplicada a los Negocios (81.91)** — ITBA, Grupo 04.

El proyecto desarrolla un sistema de predicción de churn para identificar clientes de un e-commerce con riesgo de abandono y convertir la estimación del modelo en una estrategia de retención accionable.

El resultado final combina:

- análisis de calidad y limpieza de datos;
- EDA guiado por hipótesis de negocio;
- feature engineering reproducible;
- entrenamiento y validación de un Random Forest;
- calibración de un umbral orientado a recall mediante F2;
- segmentación de clientes por nivel de riesgo;
- explicabilidad con SHAP;
- propuesta de acciones y estimación económica.

## Resumen ejecutivo

El dataset procesado contiene **5.074 clientes**, de los cuales **841 (16,57%)** presentan churn. El modelo final fue evaluado sobre un holdout de 1.015 clientes que permaneció separado durante la selección del modelo y la calibración del umbral.

Resultados finales sobre test:

| Métrica | Resultado |
|---|---:|
| ROC-AUC | 0,95 |
| PR-AUC | 0,84 |
| Recall | 96,4% |
| Precisión | 50,6% |
| F2 | 0,82 |
| Umbral operativo | 0,291 |

Con ese umbral, el modelo detecta **162 de los 168 churners** del conjunto de evaluación. La estrategia interviene al **31,5%** de los clientes evaluados y cubre el **96,4%** de los churners reales.

## Objetivo de negocio

El objetivo no es solamente clasificar clientes, sino responder tres preguntas:

1. ¿Qué clientes tienen mayor probabilidad de abandonar?
2. ¿Qué señales utiliza el modelo para estimar ese riesgo?
3. ¿Qué acción de retención conviene aplicar según la probabilidad estimada?

El costo de un falso negativo —no detectar a un cliente que finalmente abandona— se considera superior al costo de realizar una intervención preventiva adicional. Por eso se priorizan recall y F2 por encima de accuracy.

## Dataset

- **Fuente raw:** `data/raw/datos.csv`
- **Registros originales:** 5.630
- **Registros procesados:** 5.074
- **Perfiles duplicados eliminados:** 556
- **Columnas originales:** 20
- **Target:** `Churn`
- **Clase positiva:** `Churn = 1`
- **Tasa final de churn:** 16,57%

Los duplicados se identificaron comparando todas las variables excepto `CustomerID`. Eran perfiles iguales en atributos y target, pero con identificadores diferentes. Se conservó la primera aparición para evitar sobreponderarlos durante el EDA y el entrenamiento.

### Variables principales

El dataset incluye información sobre:

- antigüedad del cliente (`Tenure`);
- dispositivos y medios de acceso;
- ciudad y distancia al depósito;
- forma de pago;
- género y estado civil;
- satisfacción y reclamos;
- categoría de compra preferida;
- uso de cupones;
- cantidad de órdenes;
- cashback;
- cantidad de direcciones y dispositivos registrados.

`CustomerID` se excluye por ser un identificador. `DaySinceLastOrder` se analiza en el EDA, pero se excluye del modelo porque su comportamiento es temporalmente ambiguo y no resulta confiable como señal de alerta temprana.

## Hallazgos principales del EDA

| Hallazgo | Evidencia | Lectura de negocio |
|---|---|---|
| El riesgo se concentra al inicio | Los clientes de 0–1 meses tienen 51,3% de churn | La etapa de onboarding es una ventana crítica |
| Los reclamos son una señal fuerte | 31,3% de churn con reclamo frente a 10,8% sin reclamo | Un reclamo debe activar seguimiento comercial además de resolución operativa |
| Existen segmentos con mayor exposición | Solteros: 26,7%; categoría Mobile Phone: 26,3% | Sirven para monitoreo y segmentación, sin interpretar causalidad |
| El cashback aporta información | Los churners presentan menor cashback mediano | Puede representar diferencias de actividad o valor, no necesariamente un efecto causal |
| La satisfacción es contraintuitiva | Los scores altos no presentan necesariamente menor churn | Debe interpretarse junto con reclamos y otras variables |
| `OrderCount` aislada es débil | Sin diferencia práctica suficiente luego de deduplicar | No se utiliza como conclusión principal por sí sola |
| `DaySinceLastOrder` es ambigua | La relación observada es inversa a la hipótesis inicial | Se excluye como predictor de alerta temprana |

Los hallazgos describen asociaciones observadas. No demuestran que una variable cause el churn.

## Metodología

### 1. Limpieza y calidad de datos

El notebook de limpieza:

- inspecciona estructura, tipos y cardinalidad;
- cuantifica valores faltantes;
- detecta perfiles duplicados;
- normaliza categorías equivalentes;
- imputa faltantes numéricos con mediana para el dataset de EDA;
- redondea variables que representan conteos;
- guarda `data/processed/datos_limpios.csv`.

Categorías normalizadas:

- `COD` → `Cash on Delivery`;
- `CC` → `Credit Card`;
- `Phone` y `Mobile` → `Mobile Phone`.

La imputación del dataset limpio permite realizar el EDA sin eliminar registros. Para modelado, la imputación se repite dentro del pipeline y se ajusta exclusivamente sobre train.

### 2. EDA guiado por hipótesis

Las hipótesis fueron definidas antes de analizar los resultados. El notebook contrasta:

- antigüedad;
- reclamos;
- satisfacción;
- cantidad de órdenes;
- cashback;
- días desde la última orden;
- interacción entre reclamos y satisfacción;
- segmento de clientes de alto valor con reclamos.

Se utilizan visualizaciones, Mann-Whitney U para variables numéricas y chi-cuadrado para variables categóricas. Los p-valores se interpretan junto con dirección, tamaño de efecto y utilidad de negocio.

### 3. Split y prevención de leakage

El modelado parte nuevamente desde el dataset raw y realiza un split estratificado antes de aprender transformaciones:

| Split | Clientes | Churners | Tasa de churn |
|---|---:|---:|---:|
| Train | 4.059 | 673 | 16,58% |
| Test | 1.015 | 168 | 16,55% |

Configuración:

- split 80/20;
- estratificación por `Churn`;
- `random_state=42`;
- test reservado para la evaluación final;
- `StratifiedKFold` de 5 folds sobre train.

La imputación, el escalado, los umbrales estadísticos de features y la selección del modelo se aprenden sin utilizar test.

### 4. Feature engineering

El pipeline definido en `src/features/pipeline.py` genera:

#### Features derivadas de negocio

| Feature | Definición |
|---|---|
| `valor_cliente_proxy` | `OrderCount × CashbackAmount` |
| `coupon_per_order` | `CouponUsed / max(OrderCount, 1)` |
| `cashback_per_order` | `CashbackAmount / max(OrderCount, 1)` |
| `complain_x_satisfaction` | `Complain × SatisfactionScore` |

#### Flags de segmentación

| Feature | Criterio |
|---|---|
| `is_new_customer` | `Tenure <= 3` |
| `is_loyal_customer` | `Tenure >= 18` |
| `is_low_freq_user` | `OrderCount <= Q25` de train |
| `is_high_freq_user` | `OrderCount >= Q75` de train |
| `is_high_value` | `CashbackAmount >= mediana` de train |

Los umbrales basados en cuantiles y medianas se ajustan únicamente sobre train.

#### Preprocesamiento

- numéricas: `SimpleImputer(strategy="median")` + `RobustScaler`;
- categóricas: imputación por moda + `OneHotEncoder(handle_unknown="ignore")`;
- columnas excluidas: `CustomerID`, `Churn` y `DaySinceLastOrder`.

El pipeline produce 38 features. En el notebook de modelado se agrega `kmeans_cluster`, calculado sólo a partir de train, para obtener un total de 39 features.

### 5. Modelado

Se comparan:

- `DummyClassifier(strategy="most_frequent")` como baseline;
- `RandomForestClassifier` como modelo principal.

El DummyClassifier demuestra por qué accuracy no es suficiente: puede alcanzar aproximadamente 83% prediciendo siempre “No churn”, pero obtiene recall y F2 iguales a cero.

El Random Forest se selecciona mediante `GridSearchCV` maximizando **PR-AUC**, métrica adecuada para evaluar el ranking de la clase minoritaria.

Configuración final:

| Hiperparámetro | Valor |
|---|---:|
| `n_estimators` | 200 |
| `max_depth` | 12 |
| `min_samples_leaf` | 5 |
| `min_samples_split` | 10 |
| `max_features` | `sqrt` |
| `class_weight` | `balanced_subsample` |
| `max_samples` | 0,85 |
| `bootstrap` | `True` |

### 6. Calibración del umbral

El umbral no se optimiza sobre test. Se calcula utilizando probabilidades out-of-fold generadas sobre train mediante validación cruzada estratificada.

Se maximiza F2 porque esta métrica asigna más peso al recall:

- umbral seleccionado: **0,291**;
- F2 out-of-fold: 0,806;
- recall out-of-fold: 94,35%;
- precisión out-of-fold: 50,92%.

Luego el umbral se aplica una única vez sobre test para obtener la evaluación final.

### 7. Explicabilidad

SHAP se utiliza para analizar cómo las features influyen en las predicciones del Random Forest.

Las señales con mayor impacto incluyen:

- antigüedad;
- flag de cliente nuevo;
- interacción entre reclamo y satisfacción;
- reclamos;
- cantidad de direcciones;
- cashback;
- componentes del perfil comercial.

La importancia SHAP describe el comportamiento del modelo; no prueba relaciones causales.

## Estrategia de intervención

Se utilizan dos umbrales para separar el costo de la acción del nivel de riesgo:

| Segmento | Criterio | Clientes en test | Churners alcanzados | Acción propuesta |
|---|---|---:|---:|---|
| Alta prioridad | `P >= 0,50` | 203 | 134 | Contacto personal dentro de 24 horas |
| Prioridad media | `0,291 <= P < 0,50` | 117 | 28 | Campaña automática dentro de 48 horas |
| Sin acción | `P < 0,291` | 695 | 6 | Sin contacto; recalcular riesgo semanalmente |

La cobertura de los churners reales se distribuye así:

- alta prioridad: 79,8%;
- prioridad media: 16,7%;
- sin acción: 3,6%.

Alta y media prioridad cubren juntas **162 de 168 churners (96,4%)**.

## Proyección económica

La proyección traslada las proporciones observadas en test a los 5.074 clientes procesados:

| Concepto | Estimación |
|---|---:|
| Clientes intervenidos | ≈1.600 |
| Alta prioridad | ≈1.015 |
| Prioridad media | ≈585 |
| Churners alcanzados | ≈810 |
| Recuperación supuesta | 20% |
| Clientes potencialmente recuperados | ≈162 |
| Ingreso anual por cliente recuperado | USD 150 |
| Ingreso preservado | USD 24.300 |
| Costo de alta prioridad | USD 5 por cliente |
| Costo de prioridad media | USD 0,50 por cliente |
| Costo total estimado | USD 5.367,50 |
| Beneficio neto anual estimado | USD 18.932,50 |

Estas cifras son una **proyección basada en supuestos**, no un impacto causal observado. La recuperación del 20%, el ingreso por cliente y los costos de campaña deben validarse mediante una campaña piloto o prueba A/B.

## Estructura del repositorio

```text
.
├── data/
│   ├── raw/
│   │   └── datos.csv
│   └── processed/
│       ├── datos_limpios.csv
│       ├── features_train.parquet
│       ├── features_test.parquet
│       ├── target_train.csv
│       ├── target_test.csv
│       └── split/
├── notebooks/
│   ├── 1. Limpieza de datos.ipynb
│   ├── 2. EDA guiado por hipotesis.ipynb
│   ├── 3. Training.ipynb
│   ├── 4. Modeler.ipynb
│   └── 5. Gráficos de negocio.ipynb
├── outputs/
│   ├── business/
│   │   └── clientes_priorizados_retencion.csv
│   ├── eda/
│   └── models/
│       ├── best_rf.pkl
│       ├── confusion_matrix.png
│       ├── precision_recall_curve.png
│       ├── roc_curve.png
│       ├── shap_bar.png
│       ├── shap_summary.png
│       ├── shap_waterfall_example.png
│       └── threshold_f2_cv.json
├── plans/
├── reports/
├── src/
│   └── features/
│       └── pipeline.py
├── decisions.md
├── requirements.txt
└── README.md
```

## Notebooks

Los notebooks deben ejecutarse en este orden:

1. **`1. Limpieza de datos.ipynb`**
   Diagnóstico, faltantes, duplicados, normalización y generación del dataset para EDA.

2. **`2. EDA guiado por hipotesis.ipynb`**
   Contraste de hipótesis, tests estadísticos y hallazgos de negocio.

3. **`3. Training.ipynb`**
   Split estratificado, ajuste del pipeline y generación de features transformadas.

4. **`4. Modeler.ipynb`**
   Clustering auxiliar, baseline, GridSearchCV, Random Forest, SHAP, calibración del umbral y evaluación final.

5. **`5. Gráficos de negocio.ipynb`**
   Segmentos de intervención, cobertura, perfiles y lista priorizada para CRM.

Cada notebook consume artefactos generados por los anteriores. Para reproducir el proyecto completo deben ejecutarse secuencialmente desde un kernel limpio.

## Instalación

Se recomienda Python 3.10 o superior.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
jupyter notebook
```

### Linux o macOS

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
jupyter notebook
```

Abrir los notebooks y ejecutarlos en el orden indicado.

## Dependencias principales

- pandas y NumPy;
- scikit-learn;
- SciPy;
- Matplotlib y Seaborn;
- PyArrow;
- SHAP;
- Jupyter.

Las versiones no están fijadas en `requirements.txt`. Para una reproducción estricta conviene registrar posteriormente las versiones exactas del entorno utilizado.

## Artefactos finales

### Modelo

- `outputs/models/best_rf.pkl`: Random Forest final.
- `outputs/models/threshold_f2_cv.json`: umbral F2 y métricas out-of-fold.
- `outputs/models/confusion_matrix.png`: matriz de confusión final.
- `outputs/models/roc_curve.png`: curva ROC.
- `outputs/models/precision_recall_curve.png`: curva precision-recall.
- `outputs/models/shap_summary.png`: impacto global y dirección de las features.
- `outputs/models/shap_bar.png`: importancia SHAP media absoluta.
- `outputs/models/shap_waterfall_example.png`: explicación de un cliente individual.

### Negocio

- `outputs/business/clientes_priorizados_retencion.csv`: clientes del holdout ordenados por probabilidad y segmento de intervención.
- `outputs/business/segmentos_intervencion.png`: tamaño y composición de los segmentos.
- `outputs/business/cobertura_churners.png`: cobertura acumulada.
- `outputs/business/precision_recall_umbral_f2.png`: trade-off del umbral.
- `outputs/business/perfil_segmentos.png`: perfil relativo de los segmentos.

## Trazabilidad de decisiones

`decisions.md` registra las decisiones metodológicas, alternativas descartadas y consecuencias. Entre las más importantes:

- conservar el raw sin modificaciones;
- imputar con mediana;
- eliminar perfiles duplicados;
- realizar el split antes de transformar;
- seleccionar por PR-AUC;
- excluir `DaySinceLastOrder`;
- calibrar el umbral mediante F2 out-of-fold;
- usar dos niveles de intervención;
- separar resultados observados de proyecciones económicas.

## Limitaciones

- El modelo aprende de información histórica y puede degradarse ante cambios de comportamiento o mercado.
- `Complain` sólo puede utilizarse en producción si está disponible antes del momento de predicción.
- No se incluyen variables de competencia, estacionalidad ni contexto macroeconómico.
- Algunas variables presentan asociaciones contraintuitivas y requieren interpretación cautelosa.
- SHAP explica predicciones, no causalidad.
- La estrategia económica todavía no fue validada mediante una intervención real.
- Las proporciones del holdout se extrapolan a la base completa como aproximación.

## Próximos pasos

1. Integrar el scoring en el proceso comercial o CRM.
2. Definir la frecuencia de recalibración de probabilidades.
3. Ejecutar una prueba A/B para medir uplift real de las acciones.
4. Estimar costos, margen y customer lifetime value con datos del negocio.
5. Monitorear drift, recall, precisión y cobertura por segmento.
6. Reentrenar el modelo periódicamente.
7. Versionar datos, modelos y dependencias para fortalecer la reproducibilidad.

## Documentación adicional

- `reports/00_contexto_negocio.md`: definición del problema.
- `reports/01_hipotesis.md`: hipótesis previas al EDA.
- `reports/02_data_quality.md`: diagnóstico de calidad.
- `reports/03_eda.md`: interpretación de hallazgos.
- `reports/feature_report.md`: detalle de feature engineering.
- `reports/handoff_to_modeler.md`: contrato entre preparación y modelado.
- `decisions.md`: registro completo de decisiones.

Última actualización del README: 2026-06-18
