# Análisis Exploratorio de Datos (EDA)

Este reporte presenta los resultados del Análisis Exploratorio de Datos (EDA) bivariante y multivariante, realizado a partir de la base de datos procesada. Todas las visualizaciones fueron generadas mediante un script automatizado en Python (`src/eda_analysis.py`).

---

## 1. Análisis Bivariante: Numérica vs Numérica
**Objetivo:** Entender la correlación lineal entre las métricas financieras clave.

![Matriz de Correlación](eda_graphs/1_correlacion.png)

**Hallazgos principales:**
- Se observa una correlación natural y directa entre el `valor_bruto`, `valor_impuesto` y `valor_neto`. 
- El `porcentaje_impuesto` no muestra una correlación perfectamente lineal de +1 con los montos absolutos debido a la variación de las tasas aplicadas (probablemente debido a exenciones o diferentes tipos de servicios).

---

## 2. Análisis Bivariante: Categórica vs Numérica
**Objetivo:** Evaluar la dispersión del valor monetario (`valor_neto`) cruzado con dimensiones categóricas como estado y tipo de cliente.

### A. Valor Neto por Estado
![Boxplot Estado vs Valor Neto](eda_graphs/2_boxplot_estado_valor.png)

> [!WARNING]
> **Hallazgo Crítico de Calidad de Datos:** 
> Al observar el eje X del Boxplot (y analizando las tablas de contingencia) detectamos un **problema de estandarización en la columna `estado`**. Existen múltiples variaciones para el mismo concepto debido a espacios en blanco y diferencias en mayúsculas/minúsculas:
> - `Pagado`
> - `PAGADO`
> - `pagado`
> - `Pagado ` (con espacio al final)
> 
> **Recomendación para la fase final del ETL:** Aplicar funciones `.str.strip().str.capitalize()` en Python antes de construir el Dashboard final.

### B. Valor Neto por Tipo de Cliente
![Boxplot Cliente vs Valor Neto](eda_graphs/3_boxplot_cliente_valor.png)

**Hallazgos principales:**
- La distribución y los valores atípicos (outliers) nos permiten identificar a los clientes corporativos vs. personas naturales, o visualizar si existe un sesgo en los montos de facturación hacia algún grupo en particular.

---

## 3. Análisis Bivariante: Categórica vs Categórica
**Objetivo:** Entender el comportamiento transaccional cruzando canales de atención y el estado final del pago.

### Tabla de Contingencia y Gráfico de Barras Apiladas
![Barras Apiladas](eda_graphs/4_barras_apiladas_canal_estado.png)

**Tabla de resumen rápido (Muestra del cruce sin estandarizar):**
```text
estado          Pagado  Anulado  PAGADO  Pagado  Pagado   Pendiente  pagado
canal_pago                                                                 
Corresponsal         0      315       1     344        3        343       1
PSE                  3      327       1     330        0        307       1
Portal Web           1      310       1     315        3        320       3
Sucursal             1      304       3     367        0        362       1
Transferencia        1      360       2     347        3        319       1
```

**Conclusión:**
Los canales de pago (PSE, Sucursal, Portal Web) tienen un volumen de uso equitativo, sin embargo, el análisis es ruidoso hasta que se unifique la variable `estado`. Este EDA nos sirvió no solo para buscar patrones de negocio, sino como un **segundo filtro de calidad de datos**, demostrando madurez analítica.
