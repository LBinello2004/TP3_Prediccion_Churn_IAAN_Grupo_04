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

**Consecuencias:** no se eliminan filas por valores faltantes; se conservan todos los perfiles no duplicados y los faltantes se tratan con imputacion.

## Decision 3 - Imputar faltantes numericos con mediana

**Fecha:** 2026-05-30

**Que decidimos:** imputar las variables numericas con faltantes usando mediana.

**Por que:** todos los faltantes detectados estan en variables numericas (`Tenure`, `WarehouseToHome`, `HourSpendOnApp`, `OrderAmountHikeFromlastYear`, `CouponUsed`, `OrderCount`, `DaySinceLastOrder`) y cada columna tiene solo 4-5% de nulos. La mediana es robusta a outliers, simple de explicar y consistente con el pipeline de modelado.

**Alternativas descartadas:** `KNNImputer` (mas complejo, requiere escalado y genera una politica distinta entre limpieza y modelado); imputar con media; eliminar filas con nulos.

**Consecuencias:** se conservan todos los perfiles no duplicados y se usa la misma politica conceptual de imputacion en limpieza exploratoria y modelado.

## Decision 4 - Redondear variables de conteo despues de imputar

**Fecha:** 2026-05-30

**Que decidimos:** redondear variables que representan conteos o cantidades enteras despues de imputar.

**Por que:** la mediana puede devolver decimales cuando la cantidad de observaciones es par, pero variables como `OrderCount`, `CouponUsed`, `Tenure` o `DaySinceLastOrder` deben seguir siendo interpretables como cantidades enteras.

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

**Por que:** el dataset procesado conserva 5.074 perfiles luego de eliminar duplicados y resuelve los faltantes numericos mediante la limpieza definida previamente. Esto permite graficar y testear hipotesis sin perder registros adicionales por nulos.

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

**Por que:** con 5.074 registros, diferencias chicas pueden resultar estadisticamente significativas. Un p-valor bajo no implica automaticamente que la variable sea importante para negocio o para un futuro modelo.

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

## Decision 23 - Usar PR-AUC como metrica principal de seleccion

**Fecha:** 2026-06-08

**Que decidimos:** seleccionar los hiperparametros del Random Forest maximizando PR-AUC (`average_precision`) en validacion cruzada, y reportar ademas ROC-AUC, F1, recall, precision y F2.

**Por que:** el dataset tiene desbalance de clases (~17% churn). Accuracy es misleading: un modelo que predice "nadie churna" alcanza 83% sin aprender nada. PR-AUC se concentra en la calidad del ranking de la clase positiva y penaliza el deterioro de precision al buscar mayor recall, por lo que esta mejor alineada con la deteccion de churners. ROC-AUC se mantiene como metrica complementaria de separabilidad global. Recall es critico para el negocio porque los falsos negativos tienen mayor costo que los falsos positivos.

**Alternativas descartadas:** usar accuracy como metrica principal; seleccionar por ROC-AUC, que pondera ambas clases y puede resultar optimista con desbalance; seleccionar directamente por F2, que requiere fijar un umbral durante el ajuste de hiperparametros.

**Consecuencias:** el GridSearchCV usa `scoring='average_precision'`. PR-AUC selecciona la configuracion del modelo; F2 sigue calibrando el umbral operativo mediante predicciones out-of-fold. La evaluacion final reporta PR-AUC y ROC-AUC y genera ambas curvas.

## Decision 24 - Agregar 4 features derivadas de negocio al pipeline

**Fecha:** 2026-06-08

**Que decidimos:** incorporar en `src/features/pipeline.py` cuatro features construidas a partir de los hallazgos del EDA: `valor_cliente_proxy`, `coupon_per_order`, `cashback_per_order` y `complain_x_satisfaction`.

**Por que:** el EDA mostro que el churn esta asociado a combinaciones de variables, no solo a variables individuales. `valor_cliente_proxy` (OrderCount * CashbackAmount) captura el valor economico del cliente. `coupon_per_order` y `cashback_per_order` normalizan beneficios por nivel de actividad. `complain_x_satisfaction` captura la interaccion de H7: un reclamo en presencia de alta satisfaccion tiene distinto significado que en baja satisfaccion.

**Alternativas descartadas:** usar solo las variables originales sin derivar; incluir mas interacciones combinatorias entre todas las variables del EDA.

**Consecuencias:** el pipeline pasa de 29 a 33 columnas. El analisis SHAP permite verificar si las features derivadas aportan informacion adicional frente a las originales.

## Decision 25 - Elegir Random Forest como modelo principal

**Fecha:** 2026-06-08

**Que decidimos:** usar `DummyClassifier(strategy="most_frequent")` como baseline ingenuo y Random Forest como modelo principal para la evaluacion final y el analisis SHAP.

**Por que:** el DummyClassifier establece un piso reproducible que no aprende relaciones entre las variables y el target: siempre predice la clase mayoritaria (`Churn=0`). Esto deja en evidencia que una accuracy cercana al 83% no implica capacidad para detectar churn. En validacion cruzada, el dummy obtiene ROC-AUC 0.5000, PR-AUC 0.1658 y F1, recall, precision y F2 iguales a 0, mientras que el RF regularizado alcanza ROC-AUC 0.9485, PR-AUC 0.8122, F1 0.7282, recall 0.7741, precision 0.6882 y F2 0.7549. En test, el RF con umbral optimizado logra ROC-AUC 0.9515, PR-AUC 0.8362, recall 0.9643, precision 0.5062 y F2 0.8165, frente a ROC-AUC 0.5000, PR-AUC 0.1655 y metricas de clase positiva iguales a 0 para el dummy.

**Alternativas descartadas:** usar un unico modelo sin baseline; usar un baseline aleatorio con `strategy="stratified"`, que hace menos estable la comparacion; omitir Random Forest y sus relaciones no lineales.

**Consecuencias:** el notebook compara `DummyClassifier (most_frequent)` y Random Forest. El reporte usa el baseline para mostrar el valor predictivo agregado y se apoya en Random Forest para las metricas finales, la priorizacion de clientes y la explicabilidad con SHAP.

## Decision 26 - Configuracion final del Random Forest

**Fecha:** 2026-06-08

**Que decidimos:** usar `n_estimators=200`, `max_depth=12`, `min_samples_leaf=5`, `min_samples_split=10`, `max_features='sqrt'`, `class_weight='balanced_subsample'`, `max_samples=0.85` y `bootstrap=True` como configuracion final del Random Forest.

**Por que:** estos parametros surgieron de GridSearchCV optimizado por PR-AUC con validacion cruzada estratificada de 5 folds. La profundidad y el tamano minimo de hoja limitan la complejidad; `max_features='sqrt'`, `max_samples=0.85` y `class_weight='balanced_subsample'` aumentan la diversidad y ajustan el peso de clases dentro de cada muestra bootstrap. La corrida registrada obtuvo PR-AUC train 0.9467, PR-AUC CV 0.8122 y una brecha de 0.1345.

**Alternativas descartadas:** permitir arboles sin limite de profundidad y hojas de una observacion; usar `class_weight='balanced'`, que obtuvo una PR-AUC CV ligeramente inferior; eliminar el muestreo parcial de observaciones por arbol.

**Consecuencias:** el modelo final queda guardado en `outputs/models/best_rf.pkl`. Si se corre el notebook en otro ambiente, el GridSearch puede devolver parametros ligeramente distintos dependiendo de la version de scikit-learn.

## Decision 27 - Calibrar el umbral sin utilizar el test set

**Fecha:** 2026-06-08

**Que decidimos:** calibrar el umbral de clasificacion usando probabilidades out-of-fold generadas exclusivamente sobre train con validacion cruzada estratificada de 5 folds.

**Por que:** elegir el umbral directamente sobre test contaminaria la evaluacion final. Las predicciones out-of-fold permiten seleccionar el punto de corte con observaciones que no fueron vistas por el modelo que las predijo, manteniendo el test reservado para la medicion final.

**Alternativas descartadas:** optimizar el umbral sobre test; usar 0.50 por defecto sin analizar el costo asimetrico de falsos negativos y falsos positivos; seleccionar hiperparametros y umbral en una unica evaluacion sobre test.

**Consecuencias:** el umbral queda almacenado en `outputs/models/threshold_f2_cv.json` y luego se aplica una sola vez sobre test para calcular las metricas finales y construir la estrategia de intervencion.


## Decision 28 - Mantener SimpleImputer con mediana en el pipeline de modelado

**Fecha:** 2026-06-08

**Que decidimos:** usar `SimpleImputer(strategy="median")` para la imputacion de faltantes dentro del pipeline de modelado.

**Por que:** alinea modelado con la limpieza definida en Decision 3 y evita usar criterios distintos entre EDA y entrenamiento. La mediana es suficiente porque solo el 4-5% de los registros tienen faltantes en cada columna y el modelo final (Random Forest) es robusto a pequenas diferencias en la imputacion.

**Alternativas descartadas:** `KNNImputer` con pipeline separado para numericas y categoricas (mas complejo, mas lento y sin ganancia defendible en este dataset).

**Consecuencias:** limpieza exploratoria y modelado quedan alineados: mediana en `notebooks/1. Limpieza de datos.ipynb` y mediana dentro del pipeline de entrenamiento/CV.

## Decision 29 - Agregar features binarias de segmentacion de clientes

**Fecha:** 2026-06-12

**Que decidimos:** incorporar en `src/features/pipeline.py` cinco flags binarias de segmentacion via `SegmentFeatureBuilder`: `is_new_customer` (Tenure <= 3 meses), `is_loyal_customer` (Tenure >= 18 meses), `is_low_freq_user` (OrderCount <= Q25 train), `is_high_freq_user` (OrderCount >= Q75 train), `is_high_value` (CashbackAmount >= mediana train).

**Por que:** las variables originales ya estan en el modelo, pero sus valores continuos pueden capturar mal los umbrales de negocio mas relevantes. Un cliente con Tenure=4 y otro con Tenure=20 son cualitativamente distintos aunque la variable continua los trate como proximos. Las flags permiten al modelo aprender directamente sobre estos segmentos sin depender de que el arbol encuentre el corte exacto.

**Alternativas descartadas:** usar solo las variables continuas originales; codificar segmentos como variables ordinales (bajo/medio/alto con 3 niveles); usar Q33/Q67 como umbrales de frecuencia (descartado porque `OrderCount` se concentra fuertemente en 1-2-3, lo que hace que Q33 = Q67 = 2.0 y genera solapamiento: el 68% de los clientes quedaria marcado como low freq Y high freq al mismo tiempo). Q25=1.0 y Q75=3.0 separan tres segmentos limpios sin solapamiento: bajo (<=1, 31%), medio (2, 37%), alto (>=3, 31%).

**Consecuencias:** `NUMERIC_FEATURES` pasa de 16 a 21 columnas y el output del pipeline de 33 a 38 columnas. Los umbrales fijos (Tenure) son reglas de negocio interpretables en la defensa oral. Los umbrales estadisticos (OrderCount, CashbackAmount) se fitean solo en train para evitar leakage. Hay que re-correr el notebook 3 (Training) para regenerar los parquets y el notebook 4 (Modeler) para reentrenar con las nuevas features.

## Decision 30 - Regularizar el Random Forest final del Modeler

**Fecha:** 2026-06-12

**Que decidimos:** buscar el Random Forest final dentro de una grilla regularizada en `notebooks/4. Modeler.ipynb`: `n_estimators=200`, `max_depth=[6, 8, 10, 12]`, `min_samples_leaf=[5, 10, 20]`, `min_samples_split=[10, 20, 40]`, `max_features='sqrt'`, `class_weight=['balanced', 'balanced_subsample']` y `max_samples=[0.70, 0.85]`, con `bootstrap=True` y `return_train_score=True`.

**Por que:** la grilla fuerza regularizacion estructural, mantiene diversidad entre arboles y permite medir explicitamente el gap train-CV. Al seleccionar por PR-AUC, el mejor RF fue `class_weight='balanced_subsample'`, `max_depth=12`, `max_samples=0.85`, `min_samples_leaf=5` y `min_samples_split=10`, con PR-AUC train 0.9467, PR-AUC CV 0.8122 y gap 0.1345. Como referencia complementaria, obtuvo ROC-AUC CV 0.9485.

**Alternativas descartadas:** permitir `max_depth=None` y hojas puras; usar solamente el DummyClassifier; usar un Random Forest sin medir el gap entre train y validacion.

**Consecuencias:** el notebook reporta la comparacion CV entre `DummyClassifier (most_frequent)` y `RF regularizado`, incluye el chequeo de overfitting train vs CV, genera explicaciones SHAP y evalua el Random Forest final sobre test.

## Decision 31 - Agregar feature de clusterizacion K-Means al pipeline de modelado

**Fecha:** 2026-06-12

**Que decidimos:** agregar la pertenencia al cluster K-Means como feature numerica entera (`kmeans_cluster`) en el notebook de modelado. El K-Means se ajusta solo sobre `X_train` usando las 16 features continuas escaladas (`BASE_NUMERIC_FEATURES + DERIVED_NUMERIC_FEATURES`). El numero de clusters se determina por coeficiente de silueta evaluado en k=2 a k=5; el resultado actualizado fue k=2 con silueta=0.4293.

**Por que:** la separacion en 2 clusters (3.426 y 633 observaciones en train) captura estructura latente en el espacio de features continuas y puede aportar una sintesis adicional al modelo supervisado.

**Alternativas descartadas:** usar K-Means sobre todas las 39 features incluyendo OHE (las flags binarias tienen IQR nulo y distorsionan la metrica euclidiana; las columnas OHE aportan informacion categorica ya presente de otro modo); aplicar K-Means dentro del pipeline sklearn (habria requerido un transformer custom para no romper la secuencia de pasos existente).

**Consecuencias:** `X_train` y `X_test` pasan de 38 a 39 columnas. El modelo RF regularizado se re-entrena con la nueva feature. El K-Means con k=2 descubrio dos segmentos interpretativamente coherentes: un segmento de clientes de alto valor/baja rotacion (mayoria) y uno de clientes en riesgo con perfil de churn (minoria). Esto es util para la defensa oral: el modelo no solo clasifica, sino que identifica el segmento de riesgo de forma no supervisada.

## Decision 32 - Usar F2 (beta=2) como criterio de threshold tuning

**Fecha:** 2026-06-12

**Que decidimos:** usar F2 (beta=2) para determinar el umbral de clasificacion optimo. El umbral calibrado con predicciones out-of-fold es 0.291.

**Por que:** para la estrategia de intervencion final se prioriza recall sobre precision: perder un cliente churner sin intervenir es mas grave que contactar de mas con una accion de bajo costo. Con beta=2, el F-score pondera recall mas que precision. En CV out-of-fold, el umbral 0.291 logra F2=0.8060, recall=0.9435 y precision=0.5092. Aplicado sobre test, logra F2=0.8165, recall=0.9643 y precision=0.5062.

**Alternativas descartadas:** usar un criterio orientado a precision (deja demasiados churners sin cubrir); fijar umbral 0.50 por defecto como unico criterio (mejora precision, pero pierde cobertura); usar un umbral muy bajo orientado a recall puro (vuelve la campana poco eficiente operativamente).

**Consecuencias:** con el umbral F2-optimo (0.291), el sistema detecta 162 de los 168 churners del test y deja 6 sin intervencion. La estrategia segmentada reserva la accion costosa para `proba >= 0.50` y usa acciones baratas para el rango 0.291-0.50.

## Decision 33 - Estrategia de intervencion segmentada con dos umbrales

**Fecha:** 2026-06-12

**Que decidimos:** en lugar de elegir un umbral unico, usar dos umbrales para asignar acciones proporcionales al nivel de riesgo de cada cliente: `threshold_high=0.50` para accion costosa y `threshold_low=0.291` (F2-optimo) para accion barata.

**Por que:** el enfoque de umbral unico fuerza una eleccion entre cobertura y costo operativo. La segmentacion en dos niveles los desacopla. Los 203 clientes con proba >= 0.50 incluyen 134 churners reales y justifican llamadas o descuentos significativos. Los 117 clientes adicionales en el rango 0.291-0.50 incluyen 28 churners reales, por lo que conviene tratarlos con una accion automatizable de bajo costo. Los 695 clientes con proba < 0.291 no reciben intervencion.

**Alternativas descartadas:** umbral unico en 0.50 (deja 28 churners adicionales sin alcanzar); umbral unico en 0.291 (obliga a realizar la accion costosa sobre todos los casos positivos, incluyendo 158 falsos positivos).

**Consecuencias:** el sistema cubre el 96.4% de los churners del test set (162/168). El presupuesto de retencion se divide en 203 intervenciones de alto costo y 117 de bajo costo. Esta propuesta es accionable en cualquier CRM que soporte segmentacion por probabilidad de churn.

## Decision 34 - Crear notebook de graficos de negocio

**Fecha:** 2026-06-13

**Que decidimos:** crear `notebooks/5. Gráficos de negocio.ipynb` como notebook independiente para traducir el modelo de churn a visualizaciones accionables para negocio. El notebook carga el modelo final `outputs/models/best_rf.pkl`, reconstruye la feature `kmeans_cluster`, carga el umbral F2 calibrado mediante CV y arma los segmentos de intervencion.

**Por que:** el notebook de modelado contiene la evaluacion tecnica, pero para presentar el caso de negocio conviene separar graficos de decision: tamanio de segmentos, churners capturados, trade-off precision/recall, perfil promedio de clientes por segmento y lista priorizada para CRM.

**Alternativas descartadas:** agregar mas graficos al notebook 4 (mezcla modelado con storytelling de negocio); crear solo imagenes estaticas sin notebook reproducible (pierde trazabilidad); usar el umbral 0.50 como unico criterio (no refleja la decision de priorizar recall con F2).

**Consecuencias:** el proyecto gana un artefacto especifico para comunicacion ejecutiva. Al ejecutar el notebook se generan graficos en `outputs/business` y un CSV `clientes_priorizados_retencion.csv` con clientes ordenados por probabilidad de churn y segmento de intervencion.

## Decision 35 - Agregar graficos de variables binarias del pipeline

**Fecha:** 2026-06-13

**Que decidimos:** extender `notebooks/5. Graficos de negocio.ipynb` con una seccion especifica para las flags binarias generadas en `src/features/pipeline.py`: `is_new_customer`, `is_loyal_customer`, `is_low_freq_user`, `is_high_freq_user` e `is_high_value`.

**Por que:** estas variables son interpretables para negocio y ayudan a defender que el modelo no es solo una caja negra: captura segmentos accionables como clientes nuevos, clientes leales, baja/alta frecuencia y alto valor. Visualizarlas permite mostrar tasa de churn, probabilidad promedio e intensidad de intervencion por segmento binario.

**Alternativas descartadas:** dejar las flags solo como features internas del modelo (pierde valor explicativo); graficar solo variables continuas originales (menos accionable para CRM); mezclar estas flags dentro del perfil promedio general (oculta el contraste flag activa vs no activa).

**Consecuencias:** el notebook 5 ahora genera dos graficos adicionales en `outputs/business`: `flags_binarias_tasa_churn.png` y `flags_binarias_segmentos_intervencion.png`. La seccion tambien muestra una tabla resumen con clientes, churners, tasa de churn, probabilidad media y porcentaje intervenido para cada flag activa/inactiva.

## Decision 36 - Agregar grafico porcentual de prioridades de intervencion

**Fecha:** 2026-06-13

**Que decidimos:** agregar debajo del grafico de segmentos de intervencion un grafico de barra horizontal apilada al 100% con la proporcion de clientes en `Alta prioridad`, `Media prioridad` y `Sin accion`.

**Por que:** el grafico de cantidades absolutas muestra volumen y churners reales, pero para una presentacion ejecutiva tambien conviene mostrar rapidamente que porcentaje de la base cae en cada nivel de accion. Esto ayuda a dimensionar capacidad operativa y presupuesto.

**Alternativas descartadas:** usar otro grafico vertical de barras (duplica el anterior); mostrar solo una tabla porcentual (menos visual); mezclar porcentajes dentro del grafico de cantidades absolutas (sobrecarga la lectura).

**Consecuencias:** `notebooks/5. Graficos de negocio.ipynb` ahora genera `outputs/business/proporcion_prioridades_intervencion.png`, con porcentajes y cantidades por nivel de intervencion.

## Decision 37 - Reemplazar perfil promedio por heatmap relativo de segmentos

**Fecha:** 2026-06-13

**Que decidimos:** reemplazar el grafico de barras facetadas de perfil promedio por segmento por un heatmap relativo. El nuevo grafico muestra, para cada segmento de intervencion, la diferencia porcentual de cada variable respecto del promedio general, y entre parentesis conserva el valor promedio real.

**Por que:** el grafico anterior mostraba seis barras separadas y obligaba a comparar a ojo, sin dejar claro que caracterizaba a cada segmento. El heatmap permite ver rapidamente que la alta prioridad concentra clientes con menor antiguedad, mas reclamos y menos pedidos/dias desde ultimo pedido, mientras que el segmento sin accion tiene mayor antiguedad y menos reclamos.

**Alternativas descartadas:** mantener small multiples de barras (poca sintesis ejecutiva); usar solo una tabla de promedios (menos visual); normalizar sin mostrar valores reales (pierde interpretabilidad de negocio).

**Consecuencias:** `outputs/business/perfil_segmentos.png` ahora comunica el perfil relativo de cada segmento de forma mas accionable para la presentacion.

## Decision 38 - Unificar imputacion en mediana y descartar KNN

**Fecha:** 2026-06-13

**Que decidimos:** no usar KNN para imputacion en ninguna etapa del proyecto. La limpieza exploratoria y el pipeline de modelado usan imputacion por mediana.

**Por que:** no tiene sentido defender dos criterios distintos para resolver el mismo problema de faltantes. Con 4-5% de nulos por columna, la mediana es suficiente, robusta, reproducible y mucho mas facil de explicar en una presentacion de negocio.

**Alternativas descartadas:** mantener KNN en el notebook de limpieza y mediana en modelado; usar media; eliminar filas con nulos.

**Consecuencias:** `notebooks/1. Limpieza de datos.ipynb`, `data/processed/datos_limpios.csv`, `reports/02_data_quality.md` y la narrativa de la presentacion quedan consistentes: no se usa KNN para imputar.

## Decision 39 - Eliminar perfiles exactamente duplicados

**Fecha:** 2026-06-18

**Que decidimos:** eliminar perfiles exactamente duplicados considerando todas las columnas excepto `CustomerID`, conservando la primera aparicion de cada perfil.

**Por que:** se detectaron 556 filas adicionales cuyo target y atributos eran identicos a los de otro registro; la unica diferencia era el identificador. Mantener ambas observaciones sobreponderaria esos perfiles en el EDA y el modelado.

**Alternativas descartadas:** mantener los registros por tener IDs diferentes; eliminar automaticamente todos los pares sinteticamente relacionados aunque presenten diferencias en sus variables.

**Consecuencias:** `data/processed/datos_limpios.csv` pasa de 5.630 a 5.074 filas y conserva 841 churners, con una tasa de churn de 16,57%. Se regeneran los artefactos de EDA, split, entrenamiento, modelado y negocio sobre esta version deduplicada.
