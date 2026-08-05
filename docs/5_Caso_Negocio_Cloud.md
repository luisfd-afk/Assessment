# Resolución del Caso de Negocio: Discrepancia de Reportes (Data Governance Cloud)

## 1. Contexto del Problema
**Situación:** Al final del mes, el área de *Contabilidad* y el área de *Operaciones* presentan reportes de ingresos totales que no cuadran entre sí. Ambos equipos extraen la información del mismo ERP original, pero la procesan de manera distinta. 

Este es un problema clásico de **Silos de Datos** y falta de gobierno, el cual genera desconfianza en la información, retrasos en la toma de decisiones gerenciales y posibles riesgos de auditoría.

## 2. Diagnóstico: ¿Por qué ocurre la discrepancia?
Basado en las mejores prácticas de ingeniería de datos, las discrepancias suelen originarse por:
*   **Definiciones de Negocio Diferentes:** Operaciones puede estar midiendo el ingreso *Bruto* (apenas se hace la transacción), mientras que Contabilidad mide el ingreso *Neto* (después de impuestos y devoluciones).
*   **Cortes de Tiempo (Time-zones o Fechas):** Un equipo filtra por `fecha_transaccion` y el otro por `fecha_contabilizacion`.
*   **Manejo de Excepciones:** Un equipo elimina las transacciones con errores (nulos, duplicados) en su Excel manual, mientras que el otro las incluye asumiendo que se corregirán después.

## 3. Propuesta de Solución Arquitectónica (Cloud Data Governance)
Para resolver este problema de raíz y modernizar la infraestructura de SURA, propongo migrar hacia un ecosistema de **Gobierno de Datos en la Nube** (Ej. Google Cloud Platform, Azure o AWS) estructurado en 4 pilares:

### Pilar A: Fuente Única de Verdad (Single Source of Truth - SSOT)
Se prohíbe la extracción directa y manual de datos crudos desde el ERP hacia hojas de cálculo individuales.
*   **Solución:** Se construye un Data Lakehouse o Data Warehouse en la Nube (Ej. Google BigQuery o Snowflake). Todos los tableros de Power BI y reportes, tanto para Contabilidad como para Operaciones, **deben conectarse obligatoriamente a esta única base de datos certificada** (la tabla `transacciones` que limpiamos en la Parte 1).

### Pilar B: Catálogo de Datos (Data Catalog)
*   **Solución:** Implementar un diccionario de datos vivo (Ej. Google Cloud Data Catalog o Microsoft Purview). 
*   **Impacto:** Se estandariza el vocabulario a nivel corporativo. Si un KPI dice "Ingresos Totales", el catálogo define mediante una fórmula matemática aprobada qué columnas se suman y qué estados (`Pagado`) se incluyen, evitando que cada área invente su propio cálculo.

### Pilar C: Orquestación y Pipeline de Excepciones Automatizado
*   **Solución:** Desplegar un pipeline ETL en la nube (Ej. con Apache Airflow / Cloud Composer o dbt) idéntico a la lógica que construimos en el script de Python.
*   **Impacto:** Las transacciones con errores críticos (como colisiones de ID o sin fechas) son automáticamente desviadas a una **Bandeja de Excepciones** antes de entrar al Data Warehouse. Así, ningún reporte mostrará "basura", garantizando que los datos visibles sean exactos y auditables.

### Pilar D: Asignación de Data Stewards (Custodios del Dato)
*   **Solución:** La tecnología por sí sola no arregla el gobierno corporativo. Se debe nombrar a un *Data Steward* en Contabilidad y otro en Operaciones.
*   **Impacto:** Serán los responsables de revisar diariamente el **Dashboard de Calidad de Datos (Streamlit)** para corregir en el sistema origen las transacciones que el pipeline aisló en cuarentena.

## 4. Conclusión y Valor Gerencial
Adoptar esta estrategia Cloud elimina las "versiones de la verdad" competitivas. Cuando el Gerente Financiero pregunte *"¿Cuánto vendimos?"*, habrá un único número respaldado por reglas de calidad automatizadas, reduciendo el trabajo manual repetitivo y protegiendo el capital de la compañía contra errores humanos.
