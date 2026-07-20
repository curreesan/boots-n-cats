from sqlalchemy import create_engine, inspect

from app.core.config import settings

url = settings.database_url.replace("+asyncpg", "")
engine = create_engine(url)
insp = inspect(engine)
print(insp.get_table_names())