from gino import Gino, create_engine
from gino.schema import GinoSchemaVisitor
# from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import partial
import json

from data.config import POSTGRES_URI

db = Gino()
json_serializer = partial(json.dumps, ensure_ascii=False)
engine = create_engine(POSTGRES_URI, json_serializer=json_serializer)
Session = sessionmaker()
Session.configure(bind=engine)


async def create_db():
    # Устанавливаем связь с базой данных
    gino_engine = await create_engine(POSTGRES_URI, json_serializer=json_serializer)
    await db.set_bind(gino_engine)
    await db.gino.create_all()

    db.gino: GinoSchemaVisitor
