import pandas as pd
import os
import sys

def main():
    # Ruta del archivo (asumiendo que se ejecuta desde la raíz del proyecto)
    file_path = 'Data/Prueba_tecnica.xlsx'
    
    if not os.path.exists(file_path):
        print(f"Error: No se encuentra el archivo en {file_path}")
        sys.exit(1)
        
    print(f"--- INICIANDO DIAGNÓSTICO DE DATOS ---")
    print(f"Archivo: {file_path}")
    
    # Cargar datos
    try:
        df = pd.read_excel(file_path)
        print("\n[OK] Archivo Excel cargado exitosamente.")
    except Exception as e:
        print(f"\n[ERROR] Al cargar el Excel: {e}")
        sys.exit(1)
        
    # 1. Dimensiones básicas
    print("\n1. DIMENSIONES DEL DATASET")
    print(f"Total de filas: {df.shape[0]}")
    print(f"Total de columnas: {df.shape[1]}")
    
    # 2. Tipos de datos
    print("\n2. TIPOS DE DATOS POR COLUMNA")
    print(df.dtypes)
    
    # 3. Valores nulos
    print("\n3. VALORES NULOS POR COLUMNA")
    nulos = df.isnull().sum()
    print(nulos[nulos > 0])
    
    if nulos.sum() == 0:
        print("No se encontraron valores nulos en ninguna columna.")
    
    # 4. Registros duplicados
    print("\n4. REGISTROS DUPLICADOS")
    duplicados = df.duplicated().sum()
    print(f"Cantidad de filas exactamente duplicadas: {duplicados}")
    
    if 'id_transaccion' in df.columns:
        duplicados_id = df.duplicated(subset=['id_transaccion']).sum()
        print(f"Cantidad de 'id_transaccion' duplicados: {duplicados_id}")
        
    print("\n--- FIN DEL DIAGNÓSTICO ---")

if __name__ == "__main__":
    main()
