from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from contextlib import contextmanager

from sqlalchemy import Column, SmallInteger, orm, inspect

from app.common.libs.error_code import NotFoundError


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        # if 'status' not in kwargs.keys():
        #     kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if not rv:
            raise NotFoundError(msg="数据不存在")
        return rv

    def first_or_404(self):
        rv = self.first()
        if not rv:
            raise NotFoundError(msg="数据不存在")
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True

    # create_time = Column(Integer)
    # deleted = Column(SmallInteger, default=0)

    def __init__(self):
        # self.create_time = int(datetime.now().timestamp())
        pass

    # @property
    # def create_datetime(self):
    #     if self.create_time:
    #         return datetime.fromtimestamp(self.create_time)
    #     else:
    #         return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    # def delete(self):
    #     self.deleted = 1

    def keys(self):
        return self.fields

    def __getitem__(self, item):
        return getattr(self, item)

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self

    # def single_to_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    #
    # # 多个对象
    # def dobule_to_dict(self):
    #     result = {}
    #     for key in self.__mapper__.c.keys():
    #         if getattr(self, key) is not None:
    #             result[key] = str(getattr(self, key))
    #         else:
    #             result[key] = getattr(self, key)
    #     return result
    #
    # # 配合多个对象使用的函数
    # @staticmethod
    # def to_json(all_vendors):
    #     v = [ven.dobule_to_dict() for ven in all_vendors]
    #     return v


class MixinJSONSerializer:

    @orm.reconstructor
    def init_on_load(self):
        self.fields = []
        # self._include = []
        self._exclude = []

        self._set_fields()
        self.__prune_fields()

    def _set_fields(self):
        pass

    def __prune_fields(self):
        columns = inspect(self.__class__).columns
        if not self.fields:
            all_columns = set(columns.keys())
            self.fields = list(all_columns - set(self._exclude))

    def hide(self, *args):
        for key in args:
            self.fields.remove(key)
        return self

    def keys(self):
        return self.fields

    def __getitem__(self, key):
        return getattr(self, key)
