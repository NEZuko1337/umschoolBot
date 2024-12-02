from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context
from app.db.base import Base, DATABASE_URL
from app.bot.models import Student, Score

# Настройка логирования
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные для автоматических миграций
target_metadata = Base.metadata

def do_run_migrations(connection):
    """Запуск миграций"""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Асинхронный запуск миграций"""
    connectable: AsyncEngine = create_async_engine(DATABASE_URL)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

if context.is_offline_mode():
    raise RuntimeError("Offline режим не поддерживается для асинхронных миграций")
else:
    import asyncio
    asyncio.run(run_migrations_online())
