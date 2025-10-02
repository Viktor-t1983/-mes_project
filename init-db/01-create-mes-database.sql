-- MES Database Initialization - Production Security
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Security: Create application user with limited privileges
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'mes_app') THEN
        CREATE ROLE mes_app WITH LOGIN PASSWORD 'app_secure_password';
    END IF;
END
\$\$;

-- Security: Grant minimal required permissions
GRANT CONNECT ON DATABASE mes_db TO mes_app;
GRANT USAGE ON SCHEMA public TO mes_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO mes_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO mes_app;

-- Security: Set up audit trail
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name TEXT NOT NULL,
    operation TEXT NOT NULL,
    old_values JSONB,
    new_values JSONB,
    user_id TEXT,
    ip_address INET,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

GRANT INSERT ON audit_log TO mes_app;
