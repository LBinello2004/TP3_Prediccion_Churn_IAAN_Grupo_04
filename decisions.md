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
