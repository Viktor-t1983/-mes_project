-- Performance Tuning for MES Database
-- Senior Security Engineer Level Optimizations

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_operations_employee_date 
ON operations(employee_id, start_time);

CREATE INDEX IF NOT EXISTS idx_mo_status_dates 
ON manufacturing_orders(status, start_date, end_date);

CREATE INDEX IF NOT EXISTS idx_defects_mo_date 
ON defect_reports(manufacturing_order_id, created_at);

-- Gamification performance indexes
CREATE INDEX IF NOT EXISTS idx_achievements_employee 
ON employee_achievements(employee_id, achieved_at);

CREATE INDEX IF NOT EXISTS idx_leaderboard_points 
ON employees(points DESC) WHERE points > 0;

-- Query performance optimization
ANALYZE;
