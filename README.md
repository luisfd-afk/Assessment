# SURA - Prueba Técnica: Analista de Gestión de Información Financiera 🚀

Este repositorio contiene la solución integral a la prueba técnica, enfocada en resolver problemas reales de negocio a través de **Data Engineering (ETL), Data Quality, Análisis Financiero y Visualización Interactiva**.

## 📁 Estructura del Proyecto

El proyecto está diseñado bajo estándares de la industria, garantizando modularidad, escalabilidad y un entorno listo para implementaciones Cloud.

```text
├── Data/                 # Archivos crudos originales (Excel, PDFs)
├── data/
│   └── processed/        # Base de datos limpia (db_financiera.sqlite)
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

## 🛠️ ¿Cómo probar este proyecto localmente?

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

## 📊 Dashboard Interactivo (Data Governance)

Para visualizar la magnitud de los datos en riesgo, el Forecasting y la trazabilidad de los errores capturados por nuestro pipeline, he construido un **Data Quality Dashboard** en Streamlit.

### Opción A: Verlo Online (Recomendado)
Puedes acceder directamente a la versión desplegada en la nube sin instalar nada en tu equipo a través del siguiente enlace:
👉 **[INSERTAR_URL_DE_STREAMLIT_AQUI]** *(Se actualizará una vez desplegado).*

### Opción B: Ejecutarlo Localmente
Si deseas correr el entorno visual interactivo en tu propia máquina, ejecuta el siguiente comando en tu terminal:
```bash
streamlit run dashboards/app.py
```
*(Esto abrirá automáticamente una pestaña en tu navegador en `http://localhost:8501`)*.

---

## 📑 Reportes Destacados a Revisar

Te invito a navegar por la carpeta `docs/` donde encontrarás los análisis a profundidad:
- 💡 **[Reporte de Calidad y Riesgo](docs/1_Reporte_Calidad_Datos.md):** Donde se demuestra que el **7.78% del Capital Anual (Proyección de $10,149 millones)** estaba en riesgo por deficiencia en los datos.
- 🏗️ **[Arquitectura de Excepciones](docs/3_Pipeline_Data_Quality.md):** La lógica de por qué se creó un repositorio en cuarentena para no perder trazabilidad en las auditorías.
- 🎯 **[Conclusiones Finales](docs/4_Conclusiones_Analisis.md):** Síntesis gerencial del trabajo técnico.
