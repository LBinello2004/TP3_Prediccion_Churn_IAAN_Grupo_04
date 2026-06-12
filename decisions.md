# Decisions log

Este archivo registra decisiones efectivas del proyecto: elecciones metodologicas, supuestos, alternativas descartadas y consecuencias. No registra obviedades de la consigna.

## Decision 1 - Mantener el dataset raw intacto

**Fecha:** 2026-05-30

**Que decidimos:** trabajar siempre desde `data/raw/datos.csv` como fuente cruda y no editar ese archivo manualmente.

**Por que:** necesitamos trazabilidad y reproducibilidad. Si se modifica el raw, despues no queda claro que parte del resultado viene del dato original y que parte viene de una intervencion nuestra.

**Alternativas descartadas:** limpiar o corregir directamente el CSV raw.

**Consecuencias:** cualquier limpieza se hace en notebooks o se guarda en `data/processed/`.

## Decision 2 - No usar dropna como limpieza principal

**Fecha:** 2026-05-30

**Que decidimos:** no eliminar todas las filas con algun valor faltante usando `dropna()`.

**Por que:** aunque cada columna con nulos tiene alrededor de 4.46% a 5.45% de faltantes, al aplicar `dropna()` se eliminan 1856 filas, equivalente al 32.97% del dataset. Para un problema de churn, perder un tercio de los clientes es demasiado costoso y dificil de defender.

**Alternativas descartadas:** borrar todas las filas incompletas.

**Consecuencias:** conservamos la base completa de 5630 clientes y tratamos los faltantes con imputacion.

## Decision 3 - Imputar faltantes numericos con KNN

**Fecha:** 2026-05-30

**Que decidimos:** imputar las variables numericas con faltantes usando `KNNImputer`.

**Por que:** todos los faltantes detectados estan en variables numericas (`Tenure`, `WarehouseToHome`, `HourSpendOnApp`, `OrderAmountHikeFromlastYear`, `CouponUsed`, `OrderCount`, `DaySinceLastOrder`). KNN permite completar valores usando clientes similares en lugar de una regla unica como media o mediana.

**Alternativas descartadas:** imputar todo con mediana o media; eliminar filas con nulos.

**Consecuencias:** antes de KNN escalamos variables numericas con `StandardScaler`, porque KNN depende de distancias. Luego revertimos el escalado.

## Decision 4 - Redondear variables de conteo despues de KNN

**Fecha:** 2026-05-30

**Que decidimos:** redondear variables que representan conteos o cantidades enteras despues de imputar.

**Por que:** KNN puede devolver decimales, pero variables como `OrderCount`, `CouponUsed`, `Tenure` o `DaySinceLastOrder` deben seguir siendo interpretables como cantidades enteras.

**Alternativas descartadas:** dejar decimales generados por la imputacion en variables de conteo.

**Consecuencias:** despues de imputar, redondeamos y acotamos variables naturalmente no negativas a minimo 0.

## Decision 5 - Separar limpieza exploratoria de modelado

**Fecha:** 2026-05-30

**Que decidimos:** el CSV procesado por limpieza puede usarse para exploracion y documentacion, pero en modelado la imputacion debe ir dentro de un `Pipeline` despues del split train/test.

**Por que:** si imputamos antes de separar train/test, el imputador aprende de todo el dataset e introduce leakage desde test hacia train.

**Alternativas descartadas:** entrenar modelos directamente sobre un dataset ya imputado usando toda la base antes del split.

**Consecuencias:** cuando llegue el modelado, hay que repetir la imputacion dentro del flujo de entrenamiento.

## Decision 6 - No generar hipotesis automaticamente antes del EDA

**Fecha:** 2026-05-30

**Que decidimos:** las hipotesis de negocio iniciales las escribe el equipo en `reports/01_hipotesis.md` antes de que la IA construya el EDA.

**Por que:** la consigna evalua entendimiento de negocio y defensa de decisiones. Si las hipotesis salen genericas de la IA, el analisis pierde valor pedagogico y es mas dificil defenderlo oralmente.

**Alternativas descartadas:** generar hipotesis genericas automaticamente y construir el EDA sobre ellas.

**Consecuencias:** no se avanza al EDA hasta que `reports/01_hipotesis.md` este escrito y revisado.

## Decision 7 - Usar IA para generar un EDA inicial revisable

**Fecha:** 2026-05-30

**Que decidimos:** usar IA para construir un notebook EDA inicial, guiado por las hipotesis escritas por el equipo y con una exploracion complementaria para detectar posibles patrones.

**Por que:** queremos acelerar la generacion de graficos, tablas y tests, pero mantener el criterio de negocio en manos del equipo. El EDA generado por IA no se toma como conclusion final: se revisa manualmente para decidir que hallazgos son defendibles.

**Alternativas descartadas:** hacer todo el EDA manualmente desde cero; aceptar automaticamente cualquier hallazgo generado por IA sin revision.

**Consecuencias:** el notebook EDA sirve como borrador tecnico y fuente de evidencia. Las conclusiones finales se escriben despues de revisar si los resultados tienen sentido de negocio.

## Decision 8 - Cerrar el set inicial de hipotesis en 6

**Fecha:** 2026-05-30

**Que decidimos:** no agregar mas hipotesis por ahora y trabajar con las 6 hipotesis ya escritas en `reports/01_hipotesis.md`. Teniendo en consideración la opción de agregar nuevas hipótesis en un futuro.

**Por que:** agregar hipotesis nuevas en este momento puede dispersar el analisis. Preferimos revisar criticamente el EDA actual, entender que hipotesis se sostienen y recien despues decidir si hace falta abrir nuevas lineas.

**Alternativas descartadas:** seguir sumando hipotesis combinadas o mas especificas antes de terminar la revision del EDA inicial.

**Consecuencias:** el proximo foco es evaluar la calidad del EDA y separar hallazgos fuertes, debiles y contraintuitivos.

## Decision 9 - Documentar el EDA como reporte revisable

**Fecha:** 2026-05-30

**Que decidimos:** crear `reports/03_eda.md` como sintesis del EDA inicial, separando hallazgos fuertes, moderados, debiles y contraintuitivos.

**Por que:** el notebook contiene evidencia tecnica, pero el equipo necesita una version legible para revisar manualmente que conclusiones son defendibles y cuales requieren profundizacion.

**Alternativas descartadas:** dejar los resultados solo dentro del notebook; escribir conclusiones finales sin revision manual.

**Consecuencias:** `reports/03_eda.md` funciona como puente entre notebook tecnico y futuro reporte ejecutivo.

## Decision 10 - Usar el dataset procesado para el EDA inicial

**Fecha:** 2026-05-30

**Que decidimos:** ejecutar el EDA inicial sobre `data/processed/datos_limpios.csv`.

**Por que:** el dataset procesado conserva las 5630 filas y resuelve los faltantes numericos mediante la limpieza definida previamente. Esto permite graficar y testear hipotesis sin perder registros por nulos.

**Alternativas descartadas:** hacer el EDA directamente sobre `data/raw/datos.csv` y dropear nulos variable por variable en cada analisis.

**Consecuencias:** las conclusiones del EDA deben leerse como resultados sobre datos imputados. Para hallazgos sensibles, conviene revisar si se mantienen sobre el dataset raw.

## Decision 11 - Elegir tests estadisticos segun tipo de variable

**Fecha:** 2026-05-30

**Que decidimos:** usar Mann-Whitney U para variables numericas contra `Churn` y chi-cuadrado para variables categoricas u ordinales contra `Churn`.

**Por que:** `Churn` es binaria y varias variables numericas no parecen normales ni necesariamente comparables por media. Mann-Whitney permite comparar distribuciones sin asumir normalidad. Chi-cuadrado permite evaluar asociacion entre variables categoricas y el target.

**Alternativas descartadas:** usar solo comparaciones visuales; usar t-test para todas las variables numericas; interpretar diferencias sin test.

**Consecuencias:** cada hipotesis tiene respaldo estadistico, pero el p-valor no se toma como conclusion final sin mirar tamano de efecto y sentido de negocio.

## Decision 12 - No interpretar p-value como importancia de negocio

**Fecha:** 2026-05-30

**Que decidimos:** evaluar cada hipotesis mirando p-valor, tamano de efecto, direccion del resultado y lectura comercial.

**Por que:** con 5630 registros, diferencias chicas pueden resultar estadisticamente significativas. Un p-valor bajo no implica automaticamente que la variable sea importante para negocio o para un futuro modelo.

**Alternativas descartadas:** clasificar hipotesis como confirmadas solo porque `p < 0.05`.

**Consecuencias:** `OrderCount` queda tratado como hallazgo debil: tiene diferencia estadistica, pero bajo tamano de efecto y poca separacion practica.

## Decision 13 - Tratar resultados contraintuitivos como hallazgos a revisar

**Fecha:** 2026-05-30

**Que decidimos:** no forzar las hipotesis que salieron en direccion contraria a lo esperado.

**Por que:** `SatisfactionScore` y `DaySinceLastOrder` muestran patrones contrarios a la intuicion inicial. En vez de descartarlos o maquillarlos, se documentan como hallazgos contraintuitivos que requieren revision manual.

**Alternativas descartadas:** reescribir la conclusion para que parezca que las hipotesis se confirmaron; eliminar estos resultados por incomodos.

**Consecuencias:** el reporte 03 marca estas variables como puntos de revision antes de usarlas en conclusiones ejecutivas o modelado.

## Decision 14 - Priorizar claridad visual sobre graficos tecnicamente completos

**Fecha:** 2026-05-30

**Que decidimos:** reemplazar o evitar graficos dificiles de leer cuando no ayudan a comunicar el hallazgo principal.

**Por que:** la entrega tiene foco de negocio. Un grafico tecnicamente correcto puede no servir si el lector no entiende rapido que decision o patron muestra.

**Alternativas descartadas:** usar boxplots o distribuciones densas para todas las variables por defecto.

**Consecuencias:** se prefieren graficos simples y defendibles: tasas por segmento, lineas para variables ordinales, y visualizaciones que conecten directamente con la hipotesis.

## Decision 15 - Interpretar DaySinceLastOrder como descriptor retroactivo, no predictor

**Fecha:** 2026-06-04

**Que decidimos:** no usar `DaySinceLastOrder` como predictor confiable en produccion y documentarlo como limitacion metodologica en el reporte ejecutivo.

**Por que:** los datos muestran que los clientes con 0 dias desde su ultima orden tienen la tasa de churn mas alta (34.3%), lo que es opuesto a la intuicion. La explicacion es que la variable no captura inactividad previa al churn: el cliente hace una compra, nunca vuelve, y cuando el sistema registra el churn mide los dias desde esa ultima compra. La variable describe el evento retroactivamente. En produccion, al momento de querer actuar, no es posible saber si la ultima compra de un cliente va a ser su ultima compra.

**Alternativas descartadas:** incluir la variable sin advertencia; excluirla completamente del modelo.

**Consecuencias:** si se incluye en el modelo, hay que advertir en el reporte que su interpretacion no es causal. No debe usarse como señal de alerta temprana en un sistema de retencion real.

## Decision 16 - Ampliar el EDA con hipotesis principales H7-H8

**Fecha:** 2026-06-04

**Que decidimos:** agregar al EDA guiado por hipotesis solo dos hipotesis principales: reclamos y satisfaccion, y segmento VIP en riesgo.

**Por que:** estas hipotesis agregan interaccion y priorizacion comercial con lectura de negocio, sin dispersar el analisis con demasiadas variantes opcionales.

**Alternativas descartadas:** mantener las hipotesis de beneficios inefectivos, frecuencia ajustada y valor del cliente como hipotesis principales.

**Consecuencias:** el notebook `notebooks/2. EDA guiado por hipotesis.ipynb` mantiene H1-H6 intactas y suma H7-H8 como extension del EDA.

## Decision 17 - Usar heatmap para H7

**Fecha:** 2026-06-04

**Que decidimos:** representar H7 con un heatmap de `Complain` por `SatisfactionScore`, usando color para la tasa de churn y anotaciones con porcentaje y tamano de muestra.

**Por que:** H7 es una hipotesis de interaccion. Un heatmap permite ver rapidamente como cambia el churn al combinar reclamos y satisfaccion, y evita ocultar patrones raros al resumir satisfaction en pocos grupos.

**Alternativas descartadas:** usar un grafico de barras por segmentos combinados.

**Consecuencias:** el EDA comunica mejor que `Complain` eleva el churn en todos los niveles de satisfaccion, mientras que `SatisfactionScore` no se comporta de forma lineal simple.

## Decision 18 - Agregar clustering exploratorio al EDA

**Fecha:** 2026-06-04

**Que decidimos:** agregar al final del notebook EDA una seccion exploratoria de clustering con K-Means, metodo del codo e indice de silueta.

**Por que:** queremos evaluar si existen segmentos naturales de clientes que puedan servir como base para futuras hipotesis de negocio, sin forzar todavia una conclusion.

**Alternativas descartadas:** convertir los clusters directamente en hipotesis confirmadas; incluir `Churn` o `CustomerID` como variables de entrada del clustering.

**Consecuencias:** los clusters se interpretan como segmentacion candidata. Si se usan mas adelante, hay que validar si aportan informacion adicional frente a variables ya fuertes como `Tenure`, `OrderCount` y `CashbackAmount`.

## Decision 19 - Descartar clusters del EDA final

**Fecha:** 2026-06-04

**Que decidimos:** sacar la seccion de clustering del notebook EDA y del reporte `reports/03_eda.md`.

**Por que:** el metodo del codo no mostro una separacion clara y la mejor silueta fue baja (`k = 2`, silhouette = 0.143). Aunque los clusters mostraban cierta diferencia de churn, no identificaban segmentos suficientemente solidos como para sostener nuevas hipotesis.

**Alternativas descartadas:** mantener los clusters como bloque exploratorio; convertirlos en hipotesis nuevas; usar clusters con mas valores de `k` pese a menor silueta.

**Consecuencias:** el EDA queda enfocado en hipotesis defendibles. Si mas adelante se quiere segmentar clientes, conviene probar otra estrategia de segmentacion o partir de reglas de negocio mas interpretables.


## Decision 20 - Descartar PCA del EDA final

**Fecha:** 2026-06-04

**Que decidimos:** sacar por completo el analisis PCA del notebook EDA, del reporte `reports/03_eda.md` y de los outputs.

**Por que:** aunque se probo como analisis factorial exploratorio, las visualizaciones no aportaron una lectura suficientemente clara o accionable para el EDA de churn. Mantenerlo podia distraer de las hipotesis principales y generar una interpretacion mas compleja de lo necesario.

**Alternativas descartadas:** convertir PC1 en una hipotesis de actividad transaccional; mantener PCA solo como apendice exploratorio; usar criterio eigenvalue > 1 para justificar componentes retenidos.

**Consecuencias:** el EDA queda enfocado en hipotesis de negocio mas directas y defendibles. Si en el futuro se necesita reduccion dimensional, se deberia evaluar en una etapa metodologica separada y no como parte central del EDA guiado por hipotesis.

## Decision 21 - Crear el split train/test antes de cualquier transformacion de modelado

**Fecha:** 2026-06-05

**Que decidimos:** iniciar el notebook de training desde `data/raw/datos.csv` y crear un split train/test estratificado 80/20 con `random_state=42`.

**Por que:** el target `Churn` esta desbalanceado (~16.8% clase positiva), por lo que el split debe preservar la proporcion de churners. Ademas, para evitar leakage, la imputacion, el escalado, el encoding y la seleccion de variables deben aprenderse solo dentro de train/CV, no sobre toda la base antes del split.

**Alternativas descartadas:** entrenar usando directamente `data/processed/datos_limpios.csv`; hacer un split no estratificado; guardar datasets train/test duplicados con transformaciones ya aplicadas.

**Consecuencias:** el notebook `notebooks/3. Training.ipynb` guarda los CSVs del holdout en `data/processed/split/` (`train.csv`, `test.csv`, `X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv`, indices y resumen). El test set queda reservado para la evaluacion final.

## Decision 22 - Estandarizar categorias equivalentes antes del encoding

**Fecha:** 2026-06-05

**Que decidimos:** normalizar categorias repetidas en el notebook de limpieza antes de guardar `data/processed/datos_limpios.csv`: `COD` se unifica como `Cash on Delivery`, `CC` como `Credit Card`, `Phone` como `Mobile Phone`, y `Mobile` como `Mobile Phone` en `PreferedOrderCat`.

**Por que:** las categorias representan el mismo concepto de negocio pero estaban escritas con etiquetas distintas. Si se codifican sin estandarizar, el modelo recibe columnas dummy duplicadas artificialmente y reparte la misma senal entre categorias equivalentes.

**Alternativas descartadas:** dejar las categorias tal como vienen en el raw; corregirlas solamente en el pipeline de modelado; corregirlas manualmente solo en los CSVs de split.

**Consecuencias:** el EDA queda alimentado por `datos_limpios.csv` con categorias consolidadas, y el pipeline de modelado ya no necesita hacer esta limpieza. Las features transformadas quedan en 33 columnas.

## Decision 23 - Usar ROC-AUC como metrica principal de modelado

**Fecha:** 2026-06-08

**Que decidimos:** evaluar y comparar todos los modelos usando ROC-AUC como metrica principal, y reportar ademas F1, recall y precision.

**Por que:** el dataset tiene desbalance de clases (~17% churn). Accuracy es misleading: un modelo que predice "nadie churna" alcanza 83% sin aprender nada. ROC-AUC mide separabilidad independientemente del umbral y es robusta al desbalance. Recall es critico para el negocio porque falsos negativos (churners no detectados) tienen mayor costo que falsos positivos.

**Alternativas descartadas:** usar accuracy como metrica principal; usar solo F1 sin ROC-AUC.

**Consecuencias:** el GridSearchCV usa `scoring='roc_auc'` para seleccionar el mejor modelo. El reporte final incluye la curva ROC, matriz de confusion y el reporte de clasificacion completo por clase.

## Decision 24 - Agregar 4 features derivadas de negocio al pipeline

**Fecha:** 2026-06-08

**Que decidimos:** incorporar en `src/features/pipeline.py` cuatro features construidas a partir de los hallazgos del EDA: `valor_cliente_proxy`, `coupon_per_order`, `cashback_per_order` y `complain_x_satisfaction`.

**Por que:** el EDA mostro que el churn esta asociado a combinaciones de variables, no solo a variables individuales. `valor_cliente_proxy` (OrderCount * CashbackAmount) captura el valor economico del cliente. `coupon_per_order` y `cashback_per_order` normalizan beneficios por nivel de actividad. `complain_x_satisfaction` captura la interaccion de H7: un reclamo en presencia de alta satisfaccion tiene distinto significado que en baja satisfaccion.

**Alternativas descartadas:** usar solo las variables originales sin derivar; incluir mas interacciones combinatorias entre todas las variables del EDA.

**Consecuencias:** el pipeline pasa de 29 a 33 columnas. El analisis SHAP permite verificar si las features derivadas aportan informacion adicional frente a las originales.

## Decision 25 - Elegir Random Forest como modelo principal

**Fecha:** 2026-06-08

**Que decidimos:** usar Random Forest como modelo principal para la evaluacion en test set y para el analisis SHAP. El Decision Tree optimizado se mantiene como comparacion baseline interpretable.

**Por que:** los resultados de CV son concluyentes: RF logro ROC-AUC 0.9791 frente a 0.9115 del DT optimizado y 0.8715 del baseline. En test set: RF ROC-AUC 0.9976, recall 96.3%, F1 93.4% frente a DT ROC-AUC 0.9415, F1 77.9%. La diferencia es suficientemente grande como para justificar el modelo mas complejo.

**Alternativas descartadas:** usar el DT optimizado como modelo principal por mayor interpretabilidad; reportar solo el baseline como pide la consigna y omitir RF.

**Consecuencias:** el reporte ejecutivo y la defensa oral se apoyan en Random Forest para metricas finales y en SHAP para explicabilidad. El DT se menciona como baseline y para mostrar la regla de decision mas simple.

## Decision 26 - Mejores hiperparametros del Random Forest (run 2026-06-08)

**Fecha:** 2026-06-08

**Que decidimos:** usar `n_estimators=200`, `max_depth=None`, `min_samples_leaf=1`, `max_features='sqrt'`, `class_weight='balanced'` como configuracion final del Random Forest.

**Por que:** estos parametros surgieron del GridSearchCV con 48 combinaciones y CV estratificada de 5 folds. `max_depth=None` indica que los arboles crecen hasta hojas puras, lo que con `min_samples_leaf=1` puede implicar cierto overfitting en train, pero el ROC-AUC de test (0.9976) supera al CV (0.9791), lo que confirma que el modelo generaliza bien.

**Alternativas descartadas:** limitar `max_depth` para reducir complejidad; usar `class_weight='balanced_subsample'` que no fue el mejor en CV.

**Consecuencias:** el modelo final queda guardado en `outputs/models/best_rf.pkl`. Si se corre el notebook en otro ambiente, el GridSearch puede devolver parametros ligeramente distintos dependiendo de la version de scikit-learn.

## Decision 27 - Presentar dos umbrales de clasificacion segun costo de negocio

**Fecha:** 2026-06-08

**Que decidimos:** no fijar un umbral unico de produccion. Presentar dos opciones con sus tradeoffs cuantificados para que el negocio elija segun el costo real de sus acciones de retencion.

**Por que:** perder un cliente churner tiene costo permanente (revenue perdido, boca a boca negativo). Contactar a un no-churner con una accion de retencion tiene costo bajo y reversible. El umbral optimo depende de esa asimetria, que el equipo de negocio conoce mejor que el modelo. Umbral 0.35: recall 100% (190/190 churners detectados), precision 78%, 53 falsos positivos. Umbral 0.465 (F2-optimo, recall pesa el doble que precision): recall 98.4% (187/190), 3 churners perdidos, 21 falsos positivos.

**Alternativas descartadas:** fijar el umbral en 0.5 default (deja 7 churners sin detectar); optimizar scoring='recall' en GridSearchCV (innecesario con ROC-AUC 0.9976: la separabilidad ya es excelente, el ajuste fino es de umbral, no de hiperparametros).

**Consecuencias:** el reporte ejecutivo y la defensa oral presentan ambas opciones. Si el costo de una accion de retencion es bajo, se recomienda 0.35 (cobertura total). Si hay restriccion presupuestaria o de capacidad operativa, se recomienda 0.465 (F2-optimo). La tabla completa de tradeoffs queda en el notebook (seccion 8).


## Decision 28 - Reemplazar KNNImputer por SimpleImputer con mediana en el pipeline de modelado

**Fecha:** 2026-06-08

**Que decidimos:** usar `SimpleImputer(strategy="median")` en lugar del `KNNImputer` planteado en Decision 3 para la imputacion de faltantes dentro del pipeline de modelado.

**Por que:** Decision 3 propuso KNN porque permite imputar usando clientes similares. Al implementar el pipeline en `src/features/pipeline.py`, KNN presento dos problemas: (1) es significativamente mas lento en CV con grillas de hiperparametros de 160 y 48 combinaciones porque recalcula distancias en cada fold; (2) el `KNNImputer` de scikit-learn no admite columnas categoricas directamente, lo que complica el `ColumnTransformer`. La mediana es suficiente porque solo el 4-5% de los registros tienen faltantes en cada columna y el modelo final (Random Forest) es robusto a pequenas diferencias en la imputacion. El impacto en ROC-AUC de usar mediana vs KNN es negligible con este nivel de missingness.

**Alternativas descartadas:** KNNImputer con pipeline separado para numericas y categoricas (mas complejo, mas lento, sin ganancia medible en este dataset).

**Consecuencias:** Decision 3 queda superada por esta decision para la etapa de modelado. La imputacion KNN del notebook de limpieza (`notebooks/1. Limpieza de datos.ipynb`) se mantiene para el EDA, ya que ahi no hay restriccion de velocidad ni riesgo de leakage.

## Decision 29 - Agregar features binarias de segmentacion de clientes

**Fecha:** 2026-06-12

**Que decidimos:** incorporar en `src/features/pipeline.py` cinco flags binarias de segmentacion via `SegmentFeatureBuilder`: `is_new_customer` (Tenure <= 3 meses), `is_loyal_customer` (Tenure >= 18 meses), `is_low_freq_user` (OrderCount <= Q25 train), `is_high_freq_user` (OrderCount >= Q75 train), `is_high_value` (CashbackAmount >= mediana train).

**Por que:** las variables originales ya estan en el modelo, pero sus valores continuos pueden capturar mal los umbrales de negocio mas relevantes. Un cliente con Tenure=4 y otro con Tenure=20 son cualitativamente distintos aunque la variable continua los trate como proximos. Las flags permiten al modelo aprender directamente sobre estos segmentos sin depender de que el arbol encuentre el corte exacto.

**Alternativas descartadas:** usar solo las variables continuas originales; codificar segmentos como variables ordinales (bajo/medio/alto con 3 niveles); usar Q33/Q67 como umbrales de frecuencia (descartado porque `OrderCount` se concentra fuertemente en 1-2-3, lo que hace que Q33 = Q67 = 2.0 y genera solapamiento: el 68% de los clientes quedaria marcado como low freq Y high freq al mismo tiempo). Q25=1.0 y Q75=3.0 separan tres segmentos limpios sin solapamiento: bajo (<=1, 31%), medio (2, 37%), alto (>=3, 31%).

**Consecuencias:** `NUMERIC_FEATURES` pasa de 16 a 21 columnas y el output del pipeline de 33 a 38 columnas. Los umbrales fijos (Tenure) son reglas de negocio interpretables en la defensa oral. Los umbrales estadisticos (OrderCount, CashbackAmount) se fitean solo en train para evitar leakage. Hay que re-correr el notebook 3 (Training) para regenerar los parquets y el notebook 4 (Modeler) para reentrenar con las nuevas features.

## Decision 30 - Regularizar el Random Forest final del Modeler

**Fecha:** 2026-06-12

**Que decidimos:** reemplazar el Random Forest optimizado con arboles libres por un Random Forest regularizado en `notebooks/4. Modeler.ipynb`. La nueva grilla usa `n_estimators=200`, `max_depth=[6, 8, 10, 12]`, `min_samples_leaf=[5, 10, 20]`, `min_samples_split=[10, 20, 40]`, `max_features='sqrt'`, `class_weight=['balanced', 'balanced_subsample']` y `max_samples=[0.70, 0.85]` con `bootstrap=True` y `return_train_score=True`.

**Por que:** la configuracion anterior permitia `max_depth=None` y `min_samples_leaf=1`, una combinacion demasiado flexible para un modelo de arboles y con riesgo de memorizar train. La nueva grilla fuerza regularizacion estructural, mantiene diversidad entre arboles y permite medir explicitamente el gap train-CV. En la corrida registrada, el mejor RF regularizado fue `class_weight='balanced'`, `max_depth=12`, `max_samples=0.85`, `min_samples_leaf=5`, `min_samples_split=10`, con ROC-AUC train CV interno 0.9922, ROC-AUC validacion CV 0.9524 y gap ROC-AUC 0.0398.

**Alternativas descartadas:** mantener el RF anterior con `max_depth=None` y hojas puras; elegir el Decision Tree optimizado como modelo final solo por interpretabilidad; eliminar RF para evitar complejidad. El DT optimizado queda como comparador interpretable, pero el RF regularizado sigue superandolo en test segun la corrida registrada: ROC-AUC 0.9690 y recall 0.8368 frente a ROC-AUC 0.9415 y recall 0.7789 del DT.

**Consecuencias:** el notebook ahora reporta comparacion CV entre `DT baseline`, `DT optimizado` y `RF regularizado`, agrega chequeo de overfitting train vs CV para RF, actualiza la narrativa de SHAP y evalua en test set el RF regularizado. Hay que re-ejecutar `notebooks/4. Modeler.ipynb` para regenerar los outputs y graficos de `outputs/models`.
