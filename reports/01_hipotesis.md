# Hipotesis de negocio

Este archivo queda reservado para las hipotesis escritas por el equipo antes del EDA.

## Instrucciones

Completar al menos 5 hipotesis. Para cada una, escribir:

- **Enunciado:** que creemos que pasa.
- **Motivacion de negocio:** por que esa hipotesis tiene sentido para retencion.
- **Variables involucradas:** columnas que permitirian validarla.
- **Resultado esperado:** que patron esperariamos encontrar.

## H1

**Enunciado:** Los clientes con menor tenure tienden a churnear más.

**Motivacion de negocio:** Los clientes nuevos todavía no desarrollaron hábito de compra ni vínculo fuerte con la empresa. Si la experiencia inicial no es buena, es más probable que abandonen antes de consolidarse como clientes recurrentes.

**Variables involucradas:** `Tenure`, `Churn`

**Resultado esperado:** Esperamos que los clientes con `Churn = 1` tengan menor tenure promedio o mediano que los clientes con `Churn = 0`.

## H2

**Enunciado:** Los clientes con reclamos tienden a churnear más

**Motivacion de negocio:** Un reclamo puede reflejar una mala experiencia con la compra, entrega, producto o atención. Si la empresa no resuelve bien ese problema, el cliente puede perder confianza y dejar de comprar.

**Variables involucradas:** `Complain`, `Churn`

**Resultado esperado:** Esperamos que la tasa de churn sea significativamente mayor entre clientes con `Complain = 1` que entre clientes con `Complain = 0`.

## H3

**Enunciado:** Los clientes con menor `SatisfactionScore` tienden a churnear más.

**Motivacion de negocio:** La satisfacción resume parte de la experiencia del cliente. Si un cliente está poco satisfecho, es razonable esperar menor lealtad y mayor probabilidad de abandono.

**Variables involucradas:** `SatisfactionScore`, `Churn`.

**Resultado esperado:** Esperamos que la tasa de churn sea mayor en clientes con scores bajos de satisfacción que en clientes con scores altos.

## H4

**Enunciado:** Los clientes con menor `OrderCount` tienden a churnear más.

**Motivacion de negocio:** Un cliente que realizó pocas órdenes tiene menor vínculo transaccional con la empresa. Menor frecuencia de compra puede indicar baja adopción, poco hábito o preferencia por otros canales.

**Variables involucradas:** `OrderCount`, `Churn`.

**Resultado esperado:** Esperamos que los clientes con `Churn = 1` tengan menor cantidad de órdenes que los clientes con `Churn = 0`.

## H5

**Enunciado:** Los clientes con menor `CashbackAmount` tienden a churnear más.

**Motivacion de negocio:** El cashback puede funcionar como incentivo de recompra. Clientes que reciben menos beneficios podrían tener menor motivación económica para seguir comprando en la plataforma.

**Variables involucradas:** `CashbackAmount`, `Churn`.

**Resultado esperado:** Esperamos que los clientes con `Churn = 1` tengan menor cashback promedio o mediano que los clientes con `Churn = 0`.

## H6

**Enunciado:** Los clientes con más días desde su última orden tienden a churnear más.

**Motivacion de negocio:** La falta de compras recientes puede ser una señal temprana de pérdida de interés o de migración hacia otra plataforma. Si un cliente pasa mucho tiempo sin volver a comprar, la empresa podría intervenir con campañas de reactivación antes de que el abandono se consolide.

**Variables involucradas:** `DaySinceLastOrder`, `Churn`.

**Resultado esperado:** Esperamos que los clientes con `Churn = 1` tengan mayor cantidad de días desde su última orden que los clientes con `Churn = 0`.