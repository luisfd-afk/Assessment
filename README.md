# Sura Assessment - Analista de Gestión de Información Financiera

Este repositorio contiene la resolución técnica para el cargo de **Analista de Gestión de Información Financiera**. 

La prueba se divide en dos grandes frentes que se resuelven utilizando metodologías de Gobierno de Datos Cloud (Cloud Data Governance), automatización con Python y análisis estructurado.

## Estructura del Repositorio

- `data/`: Contiene los datos crudos (`raw/`) proporcionados para la prueba y los datos procesados/limpios (`processed/`). **Nota:** Algunos archivos de datos pueden estar ignorados en `.gitignore` por su tamaño, pero el script de transformación se provee completo.
- `src/`: Scripts de Python para realizar el proceso de ETL (Extracción, Transformación y Carga) y limpieza de datos.
- `sql/`: Consultas SQL para el análisis y diseño de modelos de información basados en los datos depurados.
- `notebooks/`: Cuadernos de Jupyter (Jupyter Notebooks) utilizados para Análisis Exploratorio de Datos (EDA) rápido.
- `dashboards/`: Contiene el tablero de control generado en Power BI (`.pbix`).
- `docs/`: Documentos en formato Markdown detallando los hallazgos (Parte 1) y la resolución metodológica orientada a la Nube para el Caso de Negocio (Parte 2).

## Instrucciones de Ejecución

### 1. Limpieza y ETL (Python)
Para reproducir la limpieza de datos:
1. Asegúrese de tener Python instalado y las dependencias de `requirements.txt`.
2. Ejecute el script principal de limpieza: `python src/data_cleaning.py`.

### 2. Análisis SQL
Las consultas analíticas se encuentran en la carpeta `sql/` y pueden ejecutarse sobre la base de datos resultante (`.sqlite` o directamente en un entorno Cloud).

### 3. Visualización (Power BI)
1. Descargue el archivo `dashboards/Reporte_Financiero.pbix`.
2. Ábralo con Power BI Desktop.
3. El dashboard está pre-conectado a la base de datos limpia local.
