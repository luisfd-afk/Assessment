# Reporte de Calidad de Datos (Parte 1)

Este documento detalla los hallazgos encontrados durante el análisis exploratorio inicial de la base de datos `Prueba_tecnica.xlsx`, correspondientes a la Parte 1 de la prueba técnica para **Analista de Gestión de Información Financiera**.

## 1. Resumen General del Dataset

- **Fuente de datos:** `Prueba_tecnica.xlsx`
- **Total de registros (filas):** 5,080
- **Total de variables (columnas):** 21

> [!NOTE]
> Las dimensiones del archivo indican un volumen de datos manejable localmente pero suficiente para demostrar técnicas de limpieza a escala.

## 2. Hallazgos Principales (Data Profiling)

A partir de la ejecución del script exploratorio `src/data_diagnostic.py`, se identificaron los siguientes problemas de calidad de datos, clasificados por dimensión de calidad:

### A. Completitud (Valores Nulos)
Se identificó la ausencia de información en campos clave para el negocio:

| Campo | Cantidad de Nulos | Impacto |
| :--- | :--- | :--- |
| `fecha_contabilizacion` | 151 | Alto. Impide el cuadre contable y cierre de mes. |
| `centro_costo` | 103 | Medio-Alto. Afecta la asignación presupuestal y análisis de rentabilidad por área. |
| `usuario_creacion` | 103 | Bajo. Afecta auditoría pero no cálculos financieros directos. |
| `ciudad` | 101 | Bajo. Limita la segmentación geográfica. |
| `cliente` | 100 | Alto. Transacciones huérfanas sin titularidad clara (se debe cruzar con NIT si está disponible). |

> [!IMPORTANT]
> **Acción recomendada:** Para los nulos, deberemos aplicar reglas de imputación (ej. inferir el `cliente` a partir del `nit` si este no es nulo) o, en última instancia, marcar el registro para revisión manual.

### B. Unicidad (Registros Duplicados)
- **Duplicados exactos (toda la fila):** 72 registros.
- **Identificadores de transacción (`id_transaccion`) duplicados:** 80 registros.

> [!WARNING]
> La diferencia entre los 80 `id_transaccion` duplicados y los 72 duplicados exactos indica que **existen 8 transacciones con el mismo ID pero con diferentes valores** en otras columnas. Esto es un riesgo severo de integridad que podría estar duplicando ingresos/gastos en los reportes o sobreescribiendo información errónea.

## 3. Siguientes Pasos (Plan de Depuración)

Para entregar la base de datos depurada, ejecutaremos las siguientes acciones de mejora (ETL):

1. **Eliminar duplicados exactos** manteniendo solo una ocurrencia.
2. **Resolver colisiones de ID** (los 8 registros con mismo `id_transaccion` pero distintos datos), priorizando el registro con la `fecha_carga` más reciente, asumiendo que es una corrección.
3. **Imputar nulos** donde sea lógicamente posible (ej. recuperar `cliente` mapeando desde un maestro de `nit`).
4. **Exportar** la base consolidada a una tabla en SQLite (preparándonos para la visualización en Power BI).
