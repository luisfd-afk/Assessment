import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    db_path = 'data/processed/db_financiera.sqlite'
    output_dir = 'docs/eda_graphs'
    
    # Crear directorio para las gráficas si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    print("--- INICIANDO ANÁLISIS EXPLORATORIO DE DATOS (EDA) ---")
    
    # Conectar a la BD y extraer datos
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM transacciones", conn)
    conn.close()
    
    # Asegurar que las fechas son tipo datetime
    if 'fecha_transaccion' in df.columns:
        df['fecha_transaccion'] = pd.to_datetime(df['fecha_transaccion'])
    
    # ---------------------------------------------------------
    # ANÁLISIS BIVARIANTE NUMÉRICA VS NUMÉRICA 
    # ---------------------------------------------------------
    print("Generando matriz de correlación...")
    numeric_cols = ['valor_bruto', 'porcentaje_impuesto', 'valor_impuesto', 'valor_neto']
    
    # Verificar que las columnas existan
    valid_cols = [c for c in numeric_cols if c in df.columns]
    
    if valid_cols:
        corr_matrix = df[valid_cols].corr()
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
        plt.title('Matriz de Correlación - Variables Numéricas')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, '1_correlacion.png'))
        plt.close()
    
    # ---------------------------------------------------------
    # ANÁLISIS CATEGÓRICA VS NUMÉRICA 
    # ---------------------------------------------------------
    print("Generando gráficos de caja...")
    
    # Valor Neto vs Estado de la transacción
    if 'estado' in df.columns and 'valor_neto' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='estado', y='valor_neto', data=df, palette='Set2')
        plt.title('Distribución del Valor Neto por Estado')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, '2_boxplot_estado_valor.png'))
        plt.close()
    
    # Valor Neto vs Tipo de Cliente
    if 'tipo_cliente' in df.columns and 'valor_neto' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='tipo_cliente', y='valor_neto', data=df, palette='Set3')
        plt.title('Distribución del Valor Neto por Tipo de Cliente')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, '3_boxplot_cliente_valor.png'))
        plt.close()

    # ---------------------------------------------------------
    # ANÁLISIS CATEGÓRICA VS CATEGÓRICA
    # ---------------------------------------------------------
    print("Generando tablas de contingencia y gráficos de barras apiladas...")
    
    if 'canal_pago' in df.columns and 'estado' in df.columns:
        # Tabla de contingencia
        contingency_table = pd.crosstab(df['canal_pago'], df['estado'])
        
        # Guardar la tabla en un archivo de texto para el reporte
        with open(os.path.join(output_dir, 'contingency_tables.txt'), 'w', encoding='utf-8') as f:
            f.write("Tabla de Contingencia: Canal de Pago vs Estado\n")
            f.write("-" * 50 + "\n")
            f.write(contingency_table.to_string())
            f.write("\n\n")
        
        # Gráfico de barras apiladas
        contingency_table.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')
        plt.title('Estado de las Transacciones por Canal de Pago')
        plt.ylabel('Cantidad de Transacciones')
        plt.xlabel('Canal de Pago')
        plt.legend(title='Estado')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, '4_barras_apiladas_canal_estado.png'))
        plt.close()
    
    print(f"\n[OK] EDA finalizado. Gráficas guardadas en: {output_dir}")

if __name__ == "__main__":
    main()
