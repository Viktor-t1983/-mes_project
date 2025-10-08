from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from src.models.base import Base

# Импортируем ВСЕ модели, чтобы Alembic знал зависимости
from src.models.order import Order
from src.models.employee import Employee
from src.models.manufacturing_order import ManufacturingOrder
from src.models.operation import Operation
from src.models.defect_report import DefectReport
from src.models.machine import Machine
from src.models.project import Project
from src.models.meta_process import MetaProcess, MetaStep
from src.models.lms import TrainingCourse, EmployeeTraining, Certificate, WorkcenterAuthorization
from src.models.audit_log import AuditLog

# this is the Alembic Config object
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
