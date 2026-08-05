-- ==========================================================================================
-- SCRIPT 01: VALIDACIÓN MATEMÁTICA Y TRIBUTARIA
-- Objetivo: Identificar riesgos financieros por errores en el cálculo de impuestos.
-- Lógica: Busca transacciones donde el (valor_bruto + valor_impuesto) difiera del valor_neto
--         o transacciones exentas de impuestos a las que se les haya cobrado valor_impuesto.
-- ==========================================================================================

SELECT 
    id_transaccion,
    fecha_transaccion,
    cliente,
    valor_bruto,
    valor_impuesto,
    valor_neto,
    aplica_impuesto,
    porcentaje_impuesto,
    (valor_bruto + valor_impuesto) AS valor_calculado,
    ABS(valor_neto - (valor_bruto + valor_impuesto)) AS diferencia_matematica
FROM transacciones
WHERE 
    -- 1. Diferencias de cálculo mayores a $1 peso (para tolerar problemas menores de redondeo de decimales)
    ABS(valor_neto - (valor_bruto + valor_impuesto)) > 1.0 
    
    -- 2. Transacciones exentas ('No' o 'NO') pero que registraron un impuesto cobrado
    OR (UPPER(aplica_impuesto) = 'NO' AND valor_impuesto > 0)
    
ORDER BY diferencia_matematica DESC;
