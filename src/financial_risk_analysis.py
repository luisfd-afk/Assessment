import pandas as pd

def main():
    input_file = 'Data/Prueba_tecnica.xlsx'
    
    print("--- INICIANDO ANÁLISIS DE RIESGO FINANCIERO ---")
    df = pd.read_excel(input_file)
    
    total_bruto = df['valor_bruto'].sum()
    print(f"Valor bruto total de la base original: ${total_bruto:,.2f}")
    
    # Riesgo por Nulos Críticos
    df_nulos_fecha = df[df['fecha_contabilizacion'].isnull()]
    riesgo_fecha = df_nulos_fecha['valor_bruto'].sum()
    print(f"\nRiesgo por transacciones sin fecha de contabilización:")
    print(f"Cantidad: {len(df_nulos_fecha)} transacciones")
    print(f"Valor bruto en riesgo: ${riesgo_fecha:,.2f}")
    
    # Riesgo por Duplicados Exactos
    riesgo_duplicados = df[df.duplicated(keep='first')]['valor_bruto'].sum()
    print(f"\nRiesgo por sobreestimación debido a duplicados exactos:")
    print(f"Valor bruto inflado artificialmente: ${riesgo_duplicados:,.2f}")
    
    # Riesgo por Colisiones de ID
    ids_repetidos = df[df.duplicated(subset=['id_transaccion'], keep=False)]['id_transaccion'].unique()
    df_colisiones = df[df['id_transaccion'].isin(ids_repetidos)]
    riesgo_colisiones = df_colisiones['valor_bruto'].sum()
    print(f"\nRiesgo por inconsistencia (IDs colisionados):")
    print(f"Cantidad de IDs afectados: {len(ids_repetidos)}")
    print(f"Valor bruto asociado a estas colisiones: ${riesgo_colisiones:,.2f}")
    
    # Total en riesgo 
    condicion_defecto = (
        df['fecha_contabilizacion'].isnull() | 
        df['centro_costo'].isnull() |
        df['cliente'].isnull() |
        df.duplicated(subset=['id_transaccion'], keep=False)
    )
    df_riesgo_total = df[condicion_defecto]
    riesgo_total = df_riesgo_total['valor_bruto'].sum()
    
    print(f"\n=======================================================")
    print(f"IMPACTO FINANCIERO GLOBAL (Capital comprometido)")
    print(f"=======================================================")
    print(f"Transacciones con defectos críticos: {len(df_riesgo_total)}")
    print(f"Valor bruto expuesto a riesgo: ${riesgo_total:,.2f}")
    print(f"Porcentaje del total de la base: {(riesgo_total/total_bruto)*100:.2f}%")
    print(f"=======================================================")

    # Proyección a futuro
    df['fecha_transaccion'] = pd.to_datetime(df['fecha_transaccion'], errors='coerce')
    min_date = df['fecha_transaccion'].min()
    max_date = df['fecha_transaccion'].max()
    
    if pd.notnull(min_date) and pd.notnull(max_date):
        dias_dataset = (max_date - min_date).days
        meses_dataset = max(1, dias_dataset / 30.44) # Promedio de días por mes
        
        riesgo_mensual_promedio = riesgo_total / meses_dataset
        riesgo_proyectado_anual = riesgo_mensual_promedio * 12
        
        print(f"\n=======================================================")
        print(f"FORECASTING (Proyección de Riesgo)")
        print(f"=======================================================")
        print(f"Período del dataset: {min_date.strftime('%Y-%m-%d')} a {max_date.strftime('%Y-%m-%d')} ({meses_dataset:.1f} meses)")
        print(f"Riesgo financiero promedio mensual: ${riesgo_mensual_promedio:,.2f}")
        print(f"Riesgo proyectado a 12 meses (Anualizado): ${riesgo_proyectado_anual:,.2f}")
        print(f"=======================================================")

if __name__ == "__main__":
    main()
