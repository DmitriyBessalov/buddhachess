import ormar
from app.db import database, metadata


class BaseModel(ormar.ModelMeta):
    class Meta:
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
