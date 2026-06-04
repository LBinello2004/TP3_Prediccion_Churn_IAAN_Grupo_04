# Reporte 03 - EDA guiado por hipotesis

## Objetivo

Este reporte resume la primera version del EDA generada con IA a partir de las hipotesis escritas por el equipo en `reports/01_hipotesis.md`.

El objetivo no es cerrar conclusiones definitivas, sino identificar que hipotesis parecen sostenerse, cuales son debiles y cuales requieren una revision manual mas profunda antes de pasar a modelado o reporte ejecutivo.

## Fuente y criterio de lectura

- Notebook principal: `notebooks/2. EDA guiado por hipotesis.ipynb`
- Dataset usado en el EDA: `data/processed/datos_limpios.csv`
- Target: `Churn`
- Churn rate general: 16.84%

El EDA usa graficos y tests estadisticos para contrastar las hipotesis. Los p-valores indican si hay evidencia estadistica de diferencia o asociacion, pero no alcanzan por si solos para afirmar importancia de negocio. Por eso tambien se considera direccion del efecto, tamano de efecto e interpretacion comercial.

## Resumen ejecutivo

Las señales mas fuertes aparecen en `Tenure` y `Complain`. Los clientes nuevos tienen una tasa de churn mucho mayor, y los clientes con reclamos presentan una tasa de churn claramente superior a quienes no reclamaron.

`CashbackAmount` tambien muestra una diferencia relevante: los clientes que churnearon tienen menor cashback mediano. Sin embargo, esta variable debe interpretarse con cautela porque puede estar relacionada con nivel de actividad o valor del cliente, no necesariamente con el beneficio como causa directa.

`OrderCount` muestra una asociacion estadistica, pero debil en terminos practicos. La diferencia entre clientes activos y churners no parece suficientemente grande como para explicar el abandono por si sola.

`SatisfactionScore` y `DaySinceLastOrder` generan resultados contraintuitivos: salen significativos, pero en direccion contraria a la hipotesis inicial. Estos casos requieren revision manual antes de usarlos como conclusiones.

## Resultados por hipotesis

### H1 - Tenure

**Hipotesis:** Los clientes con menor `Tenure` tienden a churnear mas.

**Resultado:** La hipotesis se sostiene con fuerza. Los clientes que churnearon tienen una antiguedad mediana de 1 mes, mientras que los clientes activos tienen una mediana de 10 meses.

**Lectura de negocio:** El churn parece concentrarse en etapas tempranas de la relacion con la empresa. Esto apunta a una oportunidad clara de onboarding, seguimiento temprano y acciones de retencion durante los primeros meses.

**Estado:** Hallazgo fuerte.

### H2 - Complain

**Hipotesis:** Los clientes con reclamos tienden a churnear mas.

**Resultado:** La hipotesis se sostiene. Los clientes con reclamos tienen una tasa de churn de 31.7%, frente a 10.9% en clientes sin reclamos.

**Lectura de negocio:** Los reclamos parecen estar asociados a una peor experiencia y mayor abandono. Es una variable accionable: mejorar resolucion de reclamos podria reducir churn o ayudar a priorizar contacto preventivo.

**Estado:** Hallazgo fuerte.

### H3 - SatisfactionScore

**Hipotesis:** Los clientes con menor `SatisfactionScore` tienden a churnear mas.

**Resultado:** La hipotesis no se confirma en la direccion esperada. En los datos observados, los niveles mas altos de `SatisfactionScore` presentan mayores tasas de churn que los niveles bajos.

**Lectura de negocio:** No conviene interpretar `SatisfactionScore` como una relacion lineal simple donde mayor satisfaccion implica menor churn. Puede haber problemas de definicion, momento de medicion, diferencias por segmento o interacciones con otras variables.

**Estado:** Hallazgo contraintuitivo; requiere revision manual.

### H4 - OrderCount

**Hipotesis:** Los clientes con menor `OrderCount` tienden a churnear mas.

**Resultado:** El test detecta diferencia estadistica, pero el efecto es bajo. La mediana de `OrderCount` es igual para churners y no churners.

**Lectura de negocio:** `OrderCount` puede aportar contexto, pero no parece una señal fuerte de churn por si sola. Conviene evaluarla junto con otras variables como `Tenure`, `CouponUsed` o `CashbackAmount`.

**Estado:** Hallazgo debil.

### H5 - CashbackAmount

**Hipotesis:** Los clientes con menor `CashbackAmount` tienden a churnear mas.

**Resultado:** La hipotesis se sostiene parcialmente. Los clientes que churnearon tienen menor cashback mediano que los clientes activos: 150 frente a 166.

**Lectura de negocio:** Menor cashback puede estar asociado con menor incentivo, menor volumen de compra o menor relacion previa con la plataforma. No debe interpretarse automaticamente como causalidad directa.

**Estado:** Hallazgo moderado.

### H6 - DaySinceLastOrder

**Hipotesis:** Los clientes con mas dias desde su ultima orden tienden a churnear mas.

**Resultado:** La hipotesis no se confirma. En los datos observados ocurre lo contrario: los clientes que churnearon tienen una mediana de 2 dias desde la ultima orden, frente a 4 dias en clientes activos.

**Lectura de negocio:** `DaySinceLastOrder` no debe interpretarse de forma directa como inactividad previa al abandono sin revisar como fue construida la variable. Puede estar medida de una manera que no captura el momento real de decision de churn.

**Estado:** Hallazgo contraintuitivo; requiere revision manual.

## Priorizacion de hallazgos

| Prioridad | Variable | Estado | Motivo |
|---|---|---|---|
| Alta | `Tenure` | Fuerte | Diferencia clara y accionable para onboarding. |
| Alta | `Complain` | Fuerte | Asociacion clara con mala experiencia y abandono. |
| Media | `CashbackAmount` | Moderado | Diferencia visible, pero posible relacion con actividad o valor del cliente. |
| Media | `DaySinceLastOrder` | Contraintuitivo | Resultado significativo pero opuesto a la hipotesis. |
| Media | `SatisfactionScore` | Contraintuitivo | Patron opuesto a la intuicion de negocio. |
| Baja | `OrderCount` | Debil | Asociacion estadistica con bajo tamano de efecto. |

## Puntos para revision manual

1. Revisar si el EDA debe mantenerse sobre `data/processed/datos_limpios.csv` o repetirse sobre `data/raw/datos.csv` para evitar que la imputacion influya en las hipotesis.
2. Profundizar `SatisfactionScore`: entender si mide satisfaccion general, experiencia puntual o si fue registrado en un momento posterior.
3. Profundizar `DaySinceLastOrder`: revisar definicion exacta de la variable y por que aparece en direccion contraria a la hipotesis.
4. Revisar si `CashbackAmount` representa incentivo, volumen de compra o valor historico del cliente.
5. No sobreinterpretar `OrderCount` como predictor fuerte sin combinarlo con otras variables.

## Implicancias para negocio

El principal foco comercial deberia estar en clientes nuevos y clientes con reclamos. Estos segmentos tienen una lectura clara y accionable: mejorar la experiencia inicial y resolver problemas de clientes antes de que se conviertan en abandono.

Las variables con resultados contraintuitivos no deben descartarse, pero tampoco usarse sin explicacion. Pueden revelar problemas de medicion, segmentos ocultos o relaciones no lineales que vale la pena investigar antes de modelar.

## Proximo paso

El equipo debe revisar manualmente este EDA y decidir:

1. Que hallazgos pasan al reporte ejecutivo.
2. Que hipotesis requieren graficos adicionales.
3. Que variables deben discutirse como limitacion o warning metodologico.
4. Que conclusiones todavia no estan listas para defender oralmente.
## Actualizacion: nuevas hipotesis H7-H8

Se agregaron dos hipotesis principales al notebook `notebooks/2. EDA guiado por hipotesis.ipynb`, manteniendo intacto el analisis previo de H1-H6. Estas hipotesis incorporan interacciones y segmentacion de valor para profundizar los hallazgos originales.

### H7 - Reclamos y satisfaccion

**Hipotesis:** Los clientes que realizaron reclamos (`Complain = 1`) y tienen baja satisfaccion presentan el mayor riesgo de churn.

**Resultado:** La combinacion de reclamos y satisfaccion muestra una asociacion estadisticamente significativa con churn. El test chi-cuadrado arroja p-valor < 0.001 y Cramer's V = 0.282. Sin embargo, el segmento con baja satisfaccion y reclamo no es el de mayor churn: presenta 22.1%, mientras que los clientes con reclamo y satisfaccion alta llegan a 37.3% y con satisfaccion media a 36.2%.

**Lectura de negocio:** La parte fuerte de la hipotesis es el efecto del reclamo: reclamar aumenta claramente el riesgo en todos los niveles de satisfaccion. La parte debil es asumir que la baja satisfaccion explica por si sola el mayor riesgo. El resultado refuerza que `SatisfactionScore` debe interpretarse con cautela, como ya habia ocurrido en H3.

**Estado:** Hallazgo fuerte para `Complain`; interaccion contraintuitiva con `SatisfactionScore`.

### H8 - Segmento VIP en riesgo

**Hipotesis:** Dentro de los clientes de mayor valor economico, aquellos que realizaron reclamos tienen una tasa de churn desproporcionadamente alta.

**Variable creada:** `ValorCliente = OrderCount * CashbackAmount`; segmento VIP = cuartil superior de `ValorCliente`.

**Resultado:** La hipotesis se sostiene con claridad. Dentro del segmento VIP, los clientes sin reclamo tienen churn de 8.3%, mientras que los VIP con reclamo llegan a 27.0%. El test chi-cuadrado arroja p-valor < 0.001 y Cramer's V = 0.243.

**Lectura de negocio:** Este es uno de los hallazgos mas accionables: combina riesgo de abandono con impacto economico. El segmento VIP con reclamo deberia ser candidato prioritario para acciones de retencion.

**Estado:** Hallazgo fuerte y accionable.

## Priorizacion adicional H7-H8

| Prioridad | Hipotesis | Estado | Motivo |
|---|---|---|---|
| Alta | H8 - VIP en riesgo | Fuerte | Segmento de alto valor con reclamo multiplica el churn y permite priorizar retencion. |
| Alta | H7 - Reclamos y satisfaccion | Fuerte / contraintuitiva | Confirma el peso de reclamos, pero satisfaction no ordena el riesgo como se esperaba. |

## Nuevos puntos para revision manual

1. No usar `SatisfactionScore` como variable lineal simple sin explicar sus patrones contraintuitivos.
2. Interpretar `ValorCliente` como proxy de intensidad comercial para segmentar clientes VIP, no como rentabilidad real.
3. Priorizar el segmento VIP con reclamos como hallazgo defendible para negocio.
