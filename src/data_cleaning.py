import pandas as pd
import sqlite3
import os

def main():
    input_file = 'Data/Prueba_tecnica.xlsx'
    output_db = 'data/processed/db_financiera.sqlite'
    
    print("--- INICIANDO PROCESO ETL ---")
    
    # 1. Extracción
    print(f"Cargando datos desde: {input_file}")
    df = pd.read_excel(input_file)
    print(f"Filas originales: {df.shape[0]}")
    
    # 2. Transformación y Limpieza
    
    # 2.1 Eliminar duplicados exactos
    df_clean = df.drop_duplicates()
    print(f"Filas tras eliminar duplicados exactos: {df_clean.shape[0]}")
    
    # 2.2 Resolver colisiones de ID
    # Ordenamos por fecha de carga de la más nueva a la más vieja y nos quedamos con el primer registro 
    # (asumiendo que si hay un ID duplicado, el registro con la carga más reciente es la versión corregida).
    if 'fecha_carga' in df_clean.columns and 'id_transaccion' in df_clean.columns:
        df_clean = df_clean.sort_values('fecha_carga', ascending=False)
        df_clean = df_clean.drop_duplicates(subset=['id_transaccion'], keep='first')
        print(f"Filas tras resolver colisiones de ID: {df_clean.shape[0]}")
        
    # 2.3 Imputación de valores nulos
    
    # - Recuperar el nombre del 'cliente' basándonos en el 'nit'. Si otro registro tiene el mismo NIT, copiamos el nombre.
    if 'nit' in df_clean.columns and 'cliente' in df_clean.columns:
        df_valid_clientes = df_clean.dropna(subset=['cliente'])
        nit_to_cliente = dict(zip(df_valid_clientes['nit'], df_valid_clientes['cliente']))
        df_clean['cliente'] = df_clean.apply(
            lambda row: nit_to_cliente.get(row['nit']) if pd.isna(row['cliente']) else row['cliente'],
            axis=1
        )
    
    # - Los valores que sigan nulos en columnas categóricas los marcamos como 'No Identificado' 
    # para no perder la integridad del cálculo financiero de esas transacciones.
    cols_to_fill_str = ['ciudad', 'centro_costo', 'usuario_creacion', 'cliente']
    for col in cols_to_fill_str:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna('No Identificado')
            
    # 2.4 Estandarización de texto
    # Basado en los hallazgos del EDA, estandarizamos la columna 'estado'
    if 'estado' in df_clean.columns:
        df_clean['estado'] = df_clean['estado'].str.strip().str.capitalize()
            
    # 3. Carga (Exportar a SQLite)
    os.makedirs(os.path.dirname(output_db), exist_ok=True)
    conn = sqlite3.connect(output_db)
    
    table_name = 'transacciones'
    df_clean.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"\n[OK] Datos limpios exportados exitosamente a la base de datos local:")
    print(f"Ruta: {output_db}")
    print(f"Tabla: {table_name}")
    print("--- FIN DEL PROCESO ETL ---")

if __name__ == "__main__":
    main()
