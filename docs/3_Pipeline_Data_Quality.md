# Pipeline de Calidad de Datos (Gestión de Excepciones)

## 1. Contexto del Negocio
Basado en el Análisis de Riesgo Financiero previo (donde identificamos que un alto porcentaje de capital está expuesto por errores transaccionales), se determinó que **eliminar o ignorar silenciosamente los registros defectuosos representa un riesgo de auditoría y pérdida de trazabilidad**. 

Para solucionar esto de forma robusta, se implementó un **Data Quality Pipeline (Pipeline de Calidad de Datos)** dentro de nuestro script principal de ETL (`src/data_cleaning.py`).

## 2. Arquitectura del Pipeline

El proceso de ingesta ahora se divide en dos flujos paralelos:

1.  **Bandeja de Excepciones (`transacciones_excepciones`):** Antes de realizar cualquier limpieza forzada, el sistema evalúa las reglas de calidad y separa todas las transacciones que las incumplen.
2.  **Base Oficial (`transacciones`):** Los datos que pasan las reglas (o que pueden ser imputados y salvados mediante lógica de negocio) conforman la base oficial, también conocida como la **Fuente Única de Verdad (Single Source of Truth)**.

> [!TIP]
> **Valor para el Negocio:** Al no eliminar los errores, la empresa puede analizar *por qué* ocurren y corregirlos desde el origen (ej. solicitando a TI que mejore un formulario web para que el centro de costo sea obligatorio).

## 3. Reglas de Calidad Implementadas

Las transacciones son desviadas a la bandeja de excepciones si incumplen alguna de las siguientes reglas críticas:

-   **Nulos Críticos:** Ausencia de campos financieros obligatorios como `fecha_contabilizacion` o `centro_costo`.
-   **Duplicidad Exacta:** El registro es una copia idéntica de otro. Se envían todas las ocurrencias a revisión para auditar el sistema origen.
-   **Colisión de Identificadores:** Transacciones que comparten el mismo `id_transaccion` pero tienen información divergente en otros campos.

## 4. Resultados de la Ejecución

Al ejecutar el pipeline sobre el conjunto de datos `Prueba_tecnica.xlsx`, el sistema arrojó el siguiente balance:

-   **Registros originales:** 5,080
-   **Enviados a la bandeja de excepciones:** **398 registros**. Quedan almacenados en la tabla `transacciones_excepciones` con una etiqueta de advertencia.
-   **Registros limpios (Base Oficial):** **5,000 registros**. Listos para ser consumidos por Power BI.

> [!IMPORTANT]
> **Integración con Gobierno de Datos (Rol del Data Steward):**
> La tabla de excepciones debe ser consumida periódicamente por un **Data Steward (Custodio del Dato)**. Su responsabilidad será investigar estos 398 registros anómalos, corregirlos en el ERP/sistema origen y permitir que vuelvan a fluir correctamente hacia la base oficial en la siguiente ejecución del ETL.
