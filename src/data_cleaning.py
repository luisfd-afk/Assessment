import pandas as pd
import sqlite3
import os

def main():
    input_file = 'Data/Prueba_tecnica.xlsx'
    output_db = 'data/processed/db_financiera.sqlite'
    
    print("--- INICIANDO PROCESO ETL Y DATA QUALITY PIPELINE ---")
    
    # 1. Extracción
    print(f"Cargando datos desde: {input_file}")
    df = pd.read_excel(input_file)
    print(f"Filas originales: {df.shape[0]}")
    
    # -------------------------------------------------------------
    # FASE 2.A: PIPELINE DE CALIDAD (Reporte de Excepciones)
    # -------------------------------------------------------------
    print("\nAplicando reglas de calidad y aislando excepciones...")
    
    # Regla 1: Valores nulos críticos (fecha o centro de costo)
    mask_nulos = df['fecha_contabilizacion'].isnull() | df['centro_costo'].isnull()
    
    # Regla 2: Duplicados exactos (marcamos todos los registros involucrados)
    mask_duplicados = df.duplicated(keep=False)
    
    # Regla 3: Colisiones de ID (Mismo ID_transaccion, diferentes datos)
    mask_colisiones_id = df.duplicated(subset=['id_transaccion'], keep=False) & ~mask_duplicados
    
    # Consolidar todos los registros problemáticos
    mask_excepciones = mask_nulos | mask_duplicados | mask_colisiones_id
    df_excepciones = df[mask_excepciones].copy()
    
    # Agregar una marca a los registros para la auditoría (Data Steward)
    df_excepciones['etiqueta_dq'] = "Requiere Revisión (Data Steward)"
    
    print(f"Total de registros aislados en la bandeja de excepciones: {df_excepciones.shape[0]}")
    
    # -------------------------------------------------------------
    # FASE 2.B: TRANSFORMACIÓN Y LIMPIEZA (Base Oficial Consolidada)
    # -------------------------------------------------------------
    print("\nIniciando limpieza para la tabla oficial...")
    
    # Eliminar duplicados exactos
    df_clean = df.drop_duplicates()
    
    # Resolver colisiones de ID (dejar el más reciente)
    if 'fecha_carga' in df_clean.columns and 'id_transaccion' in df_clean.columns:
        df_clean = df_clean.sort_values('fecha_carga', ascending=False)
        df_clean = df_clean.drop_duplicates(subset=['id_transaccion'], keep='first')
        
    # Imputación de valores nulos (Cliente vía NIT)
    if 'nit' in df_clean.columns and 'cliente' in df_clean.columns:
        df_valid_clientes = df_clean.dropna(subset=['cliente'])
        nit_to_cliente = dict(zip(df_valid_clientes['nit'], df_valid_clientes['cliente']))
        df_clean['cliente'] = df_clean.apply(
            lambda row: nit_to_cliente.get(row['nit']) if pd.isna(row['cliente']) else row['cliente'],
            axis=1
        )
    
    # Rellenar restantes con 'No Identificado'
    cols_to_fill_str = ['ciudad', 'centro_costo', 'usuario_creacion', 'cliente']
    for col in cols_to_fill_str:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna('No Identificado')
            
    # Estandarización de texto (Hallazgo del EDA)
    if 'estado' in df_clean.columns:
        df_clean['estado'] = df_clean['estado'].str.strip().str.capitalize()
            
    # -------------------------------------------------------------
    # FASE 3: CARGA (Exportar a SQLite)
    # -------------------------------------------------------------
    os.makedirs(os.path.dirname(output_db), exist_ok=True)
    conn = sqlite3.connect(output_db)
    
    # Guardar base oficial (Single Source of Truth)
    df_clean.to_sql('transacciones', conn, if_exists='replace', index=False)
    
    # Guardar bandeja de excepciones
    df_excepciones.to_sql('transacciones_excepciones', conn, if_exists='replace', index=False)
    
    conn.close()
    
    print(f"\n[OK] Datos exportados exitosamente a la base de datos local:")
    print(f"- {df_clean.shape[0]} registros limpios guardados en tabla 'transacciones'")
    print(f"- {df_excepciones.shape[0]} registros aislados guardados en tabla 'transacciones_excepciones'")
    print("--- FIN DEL PROCESO ETL ---")

if __name__ == "__main__":
    main()
