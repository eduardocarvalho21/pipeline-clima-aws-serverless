SELECT 
    cidade, 
    AVG(temp) as media_temperatura, 
    MAX(temp) as temp_maxima, 
    MIN(temp) as temp_minima
FROM db_clima.tb_clima_silver
GROUP BY cidade;
