from pydantic import BaseModel
import sqlalchemy.dialects as dialects

from utils.exceptions import MissingRecordException


class BaseDBTransaction:
    def __init__(self, session):
        self.session = session
        self.model = None
        self.dialect = getattr(dialects, self.session.bind.dialect.name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            try:
                self.session.commit()
            except Exception:
                self.session.rollback()
                raise

    def new_object(self, data):
        if isinstance(data, BaseModel):
            data = data.model_dump()
        return self.model(**data)

    def add(self, obj):
        self.session.add(obj)

    def get(self, obj_id):
        return self.session.query(self.model).get(obj_id)

    def get_all(self, page=None, page_size=None):
        return self.query(page=page, page_size=page_size)

    def query(self, page=None, page_size=None, *args, **kwargs):
        query = self.session.query(self.model).filter_by(*args, **kwargs)
        if page and page_size:
            skip = (page - 1) * page_size
            query = query.limit(page_size).offset(skip)
        return query.all()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        self.session.delete(obj)

    def update(self, obj_id, data):
        if isinstance(data, BaseModel):
            data = data.model_dump(exclude={"id"})
        data.pop("id", None)
        obj = self.get(obj_id)
        if obj is None:
            raise MissingRecordException(
                f"{self.model.__name__} with id {obj_id} does not exist"
            )
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        return obj

    def bulk_insert(self, data):
        stmt = self.dialect.insert(self.model).values(data)
        stmt = stmt.on_conflict_do_nothing()
        self.session.execute(stmt)
