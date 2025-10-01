-- Проверяем структуру таблицы defect_reports
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'defect_reports' 
ORDER BY ordinal_position;
