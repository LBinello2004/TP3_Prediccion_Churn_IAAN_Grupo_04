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
