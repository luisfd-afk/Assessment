-- ==========================================================================================
-- SCRIPT 02: KPIs ESTRATÉGICOS DE RENTABILIDAD POR CANAL Y CIUDAD
-- Objetivo: Obtener indicadores de negocio limpios para toma de decisiones.
-- Lógica: Agrupa solo transacciones efectivamente pagadas, calculando volumen y ticket promedio.
-- ==========================================================================================

SELECT 
    canal_pago,
    ciudad,
    COUNT(id_transaccion) AS total_transacciones_exitosas,
    SUM(valor_neto) AS ingresos_netos_totales,
    AVG(valor_neto) AS ticket_promedio
FROM transacciones
WHERE estado = 'Pagado' -- Solo contamos el dinero real ingresado
GROUP BY canal_pago, ciudad
ORDER BY ingresos_netos_totales DESC;
