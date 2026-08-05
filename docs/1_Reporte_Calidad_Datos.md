# Reporte de Calidad de Datos

Este documento detalla los hallazgos encontrados durante el análisis exploratorio inicial de la base de datos `Prueba_tecnica.xlsx`, correspondientes a la Parte 1 de la prueba técnica para **Analista de Gestión de Información Financiera**.

## 1. Resumen General del Dataset

- **Fuente de datos:** `Prueba_tecnica.xlsx`
- **Total de registros filas:** 5,080
- **Total de variables columnas:** 21

> [!NOTE]
> Las dimensiones del archivo indican un volumen de datos manejable localmente pero suficiente para demostrar técnicas de limpieza a escala.

## 2. Hallazgos Principales

A partir de la ejecución del script exploratorio `src/data_diagnostic.py`, se identificaron los siguientes problemas de calidad de datos, clasificados por dimensión de calidad:

### A. Completitud 
Se identificó la ausencia de información en campos clave para el negocio:

| Campo | Cantidad de Nulos | Impacto |
| :--- | :--- | :--- |
| `fecha_contabilizacion` | 151 | Alto. Impide el cuadre contable y cierre de mes. |
| `centro_costo` | 103 | Medio-Alto. Afecta la asignación presupuestal y análisis de rentabilidad por área. |
| `usuario_creacion` | 103 | Bajo. Afecta auditoría pero no cálculos financieros directos. |
| `ciudad` | 101 | Bajo. Limita la segmentación geográfica. |
| `cliente` | 100 | Alto. Transacciones huérfanas sin titularidad clara (se debe cruzar con NIT si está disponible). |

> [!IMPORTANT]
> **Acción recomendada:** Para los nulos, deberemos aplicar reglas de imputación ej. inferir el `cliente` a partir del `nit` si este no es nulo o, en última instancia, marcar el registro para revisión manual.

### B. Unicidad 
- **Duplicados exactos toda la fila:** 72 registros.
- **Identificadores de transacción (`id_transaccion`) duplicados:** 80 registros.

> [!WARNING]
> La diferencia entre los 80 `id_transaccion` duplicados y los 72 duplicados exactos indica que **existen 8 transacciones con el mismo ID pero con diferentes valores** en otras columnas. Esto es un riesgo severo de integridad que podría estar duplicando ingresos/gastos en los reportes o sobreescribiendo información errónea.

## 3. Cuantificación del Riesgo Financiero

Más allá de identificar los errores técnicos, se ejecutó un script de análisis (`src/financial_risk_analysis.py`) para cuantificar el impacto monetario de esta mala calidad de datos. Sobre un valor bruto total original de **$576,457 millones**, encontramos lo siguiente:

- **Riesgo por Nulos Críticos:** 151 transacciones sin fecha de contabilización ponen en riesgo de retraso contable o descuadre un valor de **$18,501 millones**.
- **Sobreestimación por Duplicidad:** Los duplicados exactos inflan artificialmente la base en **$186 millones**.
- **Inconsistencia por Colisión de IDs:** Los 80 IDs colisionados comprometen la trazabilidad de **$754 millones**.

> [!CAUTION]
> **Impacto Global:** Existen 496 transacciones con defectos críticos (fechas nulas, sin centro de costo, IDs duplicados o clientes nulos). Esto significa que **$44,871 millones el 7.78% del total transado** está expuesto a riesgo operativo, tributario o contable por falta de gobierno de datos.

### Forecasting 

Tomando como base el rango de tiempo de las transacciones aproximadamente 53.1 meses de datos observados, calculamos la tasa de defectos y proyectamos el riesgo monetario en caso de no aplicar medidas de calidad de datos preventivas:

*   **Riesgo financiero promedio mensual:** $845.7 millones expuestos mensualmente a fallas de consistencia y completitud.
*   **Proyección de pérdida/riesgo anualizado:** **$10,149 millones**.

Este es el capital proyectado que entrará al sistema con defectos críticos durante el próximo año si no se implementa el proceso ETL depurativo de inmediato.

## 4. Acciones de Mejora para Mitigar Riesgos

Para salvaguardar la confiabilidad de la información y mitigar los riesgos monetarios identificados, se han diseñado e implementado las siguientes acciones de mejora específicas para cada problema de calidad:

### A. Riesgo por Valores Nulos Críticos
- **El Problema:** Ausencia de `fecha_contabilizacion`, `centro_costo` y `cliente`.
- **Acción de Mitigación a Corto Plazo:** Implementar lógica de imputación en el ETL. Por ejemplo, cruzar el campo `nit` con una tabla maestra o los mismos registros históricos para deducir el `cliente` faltante. Para los nulos financieros como la fecha, los registros se envían a una tabla de excepciones (`transacciones_excepciones`) evitando que contaminen los cálculos de ingresos del mes actual.
- **Acción de Mitigación a Largo Plazo:** Configurar estos campos como **obligatorios** desde la interfaz de usuario o el formulario web donde se originan las transacciones.

### B. Riesgo por Duplicidad Exacta
- **El Problema:** 72 registros idénticos inflando el valor bruto.
- **Acción de Mitigación:** Modificar el pipeline de ingesta para incluir un nodo de deduplicación Ej. `df.drop_duplicates()` antes de cualquier consolidación. Hacia atrás, auditar el sistema transaccional origen para descubrir si existe un error de doble clic al guardar la información.

### C. Riesgo por Inconsistencia
- **El Problema:** 80 IDs compartidos con datos diferentes.
- **Acción de Mitigación:** Aplicar una regla de resolución de conflictos (Tie-breaker). El ETL ordena los registros colisionados por la columna `fecha_carga` de forma descendente, asumiendo que el registro más reciente es una corrección o actualización legítima, y descarta los anteriores.

### D. Riesgo por Estandarización Textual
- **El Problema:** Múltiples formatos para el estado ("PAGADO", "pagado", "Pagado ").
- **Acción de Mitigación:** Agregar una capa de limpieza de strings (`.str.strip().str.capitalize()`) en el flujo de transformación de datos para unificar categóricamente los estados antes de que los consuma Power BI, asegurando agrupaciones correctas en los reportes financieros.
