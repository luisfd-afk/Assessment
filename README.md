# Prueba Técnica: Analista de Gestión de Información Financiera

Este repositorio contiene la solución integral a la prueba técnica, enfocada en resolver problemas reales de negocio a través de **Data Engineering, ETL, Data Quality, Análisis Financiero y Visualización Interactiva**.

## 🛠️ Herramientas Utilizadas

**Parte 1: Análisis, Pipeline y Calidad de Datos**
*   **Python (Pandas & Numpy):** Utilizado para el análisis exploratorio (EDA) y la construcción del pipeline ETL. Permite manejar transformaciones lógicas complejas, aislar errores y hacer el proceso 100% reproducible en comparación con procesos manuales en Excel.
*   **SQLite:** Actúa como nuestro Data Warehouse local (`db_financiera.sqlite`). Elegido por ser una base de datos relacional ligera y sin configuración, perfecta para simular entornos productivos y ejecutar nuestras consultas de validación.
*   **SQL:** Utilizado para crear el portafolio de consultas analíticas (Cálculo de KPIs tributarios, agregaciones por canal/ciudad y auditoría de excepciones).
*   **Streamlit & Plotly:** Herramientas elegidas para el desarrollo del Dashboard interactivo. Permiten crear interfaces web profesionales y gráficos dinámicos (forecasting) directamente desde Python, sin depender de licencias externas de BI.

**Parte 2: Caso de Negocio (Gobierno de Datos Cloud)**
*   **Conceptos de Arquitectura Cloud (BigQuery/Snowflake, Data Catalog):** No se programaron, pero se utilizaron como base teórica arquitectónica para resolver el problema de los silos de datos, proponiendo un "Single Source of Truth" (SSOT) gobernable.

## Estructura del Proyecto

El proyecto está diseñado bajo estándares de la industria, garantizando modularidad, escalabilidad y un entorno listo para implementaciones Cloud.

```text
├── Data/                 # Archivos crudos originales Excel, PDF
├── data/
│   └── processed/        # Base de datos limpia 
├── dashboards/           # Aplicación web interactiva de Streamlit
│   ├── app.py            # Código fuente del dashboard de Data Quality
│   └── Logo_Sura.png
├── docs/                 # Documentación formal y hallazgos
│   ├── 1_Reporte_Calidad_Datos.md
│   ├── 2_Reporte_EDA.md
│   ├── 3_Pipeline_Data_Quality.md
│   └── 4_Conclusiones_Analisis.md
├── sql/                  # Portafolio de Consultas SQL analíticas
│   ├── 01_validacion_tributaria.sql
│   ├── 02_kpis_por_canal_ciudad.sql
│   └── 03_analisis_excepciones.sql
├── src/                  # Scripts principales de Python
│   ├── data_diagnostic.py
│   ├── data_cleaning.py          # ETL y Data Quality Pipeline
│   ├── eda_analysis.py
│   └── financial_risk_analysis.py # Modelo de cuantificación de riesgo
└── requirements.txt      # Dependencias para despliegue en la Nube
```

---

## ¿Cómo probar este proyecto localmente?

Si deseas ejecutar los scripts desde tu entorno local, asegúrate de tener Python instalado y sigue estos pasos:

**1. Instalar dependencias:**
```bash
pip install -r requirements.txt
```

**2. Ejecutar el Pipeline ETL y Data Quality:**
Este script ingesta los datos de Excel, aísla las excepciones de calidad y crea la base de datos oficial.
```bash
python src/data_cleaning.py
```

**3. Ejecutar el Modelo de Riesgo Financiero:**
```bash
python src/financial_risk_analysis.py
```

---

## Dashboard Interactivo Data Governance

Para visualizar la magnitud de los datos en riesgo, el Forecasting y la trazabilidad de los errores capturados por nuestro pipeline, he construido un **Data Quality Dashboard** en Streamlit.

### Ejecutarlo Localmente
Para correr el entorno visual interactivo en tu propia máquina, ejecuta el siguiente comando en tu terminal (asegúrate de haber instalado los requirements.txt):
```bash
python -m streamlit run dashboards/app.py
```
*(Esto abrirá automáticamente una pestaña en tu navegador web en `http://localhost:8501`)*.

En caso tal de que no puedas ver el Dashboard, Puedes acceder a la siguiente carpeta para ver los reportes estaticos:
(docs/)

---

## 📑 Reportes Destacados a Revisar

Te invito a navegar por la carpeta `docs/` donde encontrarás los análisis a profundidad:
- 💡 **[Reporte de Calidad y Riesgo](docs/1_Reporte_Calidad_Datos.md):** Donde se demuestra que el **7.78% del Capital Anual (Proyección de $10,149 millones)** estaba en riesgo por deficiencia en los datos.
- 🏗️ **[Arquitectura de Excepciones](docs/3_Pipeline_Data_Quality.md):** La lógica de por qué se creó un repositorio en cuarentena para no perder trazabilidad en las auditorías.
- 🎯 **[Conclusiones Finales](docs/4_Conclusiones_Analisis.md):** Síntesis gerencial del trabajo técnico de la Parte 1.
- ☁️ **[Resolución Caso de Negocio (Parte 2)](docs/5_Caso_Negocio_Cloud.md):** Propuesta de Arquitectura de Data Governance en la Nube (SSOT, Data Catalog, Data Stewards) para solucionar discrepancias entre áreas.
