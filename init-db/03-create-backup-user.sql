-- Backup User for MES Database
-- Security: Limited privileges for backup operations

DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'backup_user') THEN
        CREATE ROLE backup_user WITH LOGIN PASSWORD 'backup_secure_password';
    END IF;
END
\$\$;

-- Grant minimal backup privileges
GRANT CONNECT ON DATABASE mes_db TO backup_user;
GRANT USAGE ON SCHEMA public TO backup_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO backup_user;

-- Security: Cannot modify data
REVOKE INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public FROM backup_user;

COMMENT ON ROLE backup_user IS 'Read-only user for backup operations';
