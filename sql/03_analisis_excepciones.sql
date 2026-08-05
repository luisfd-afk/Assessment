-- ==========================================================================================
-- SCRIPT 03: TABLERO DE CONTROL DEL DATA STEWARD (EXCEPCIONES)
-- Objetivo: Monitorear el volumen y el impacto económico de los errores de calidad de datos.
-- Lógica: Consulta a la tabla aislada de excepciones generada por el pipeline de Python.
-- ==========================================================================================

SELECT 
    etiqueta_dq AS motivo_rechazo_pipeline,
    COUNT(id_transaccion) AS cantidad_transacciones_rechazadas,
    SUM(valor_bruto) AS capital_inmovilizado_por_riesgo
FROM transacciones_excepciones
GROUP BY etiqueta_dq
ORDER BY capital_inmovilizado_por_riesgo DESC;
