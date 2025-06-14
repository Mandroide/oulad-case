-- Full Domain son todos los valores distintos de una columna.
-- FULLDOMAIN: Tabla `assessments`

-- Tipos de evaluación y cuántas hay de cada tipo
SELECT assessment_type, COUNT(*) AS cantidad
FROM assessments
GROUP BY assessment_type;

-- Rango de fechas de evaluaciones
SELECT MIN(date) AS fecha_minima, MAX(date) AS fecha_maxima
FROM assessments;

-- Distribución de pesos (weight)
SELECT weight, COUNT(*) AS cantidad
FROM assessments
GROUP BY weight
ORDER BY weight;

-- Evaluaciones por módulo y presentación
SELECT code_module, code_presentation, COUNT(*) AS total_assessments
FROM assessments
GROUP BY code_module, code_presentation
ORDER BY code_module, code_presentation;


-- FULLDOMAIN: Tabla `vle`

-- Tipos de actividad en el entorno virtual
SELECT activity_type, COUNT(*) AS total_actividades
FROM vle
GROUP BY activity_type
ORDER BY total_actividades DESC;

-- Rango de semanas cubiertas por recursos
SELECT MIN(week_from) AS semana_inicio, MAX(week_to) AS semana_fin
FROM vle;

-- Recursos por tipo, módulo y presentación
SELECT code_module, code_presentation, activity_type, COUNT(*) AS cantidad
FROM vle
GROUP BY code_module, code_presentation, activity_type
ORDER BY code_module, activity_type;
