# thirdparty
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class BaseModel:
    def to_dict(self):
        return {
            c.key: str(getattr(self, c.key)) if getattr(self, c.key) is not None else None
            for c in inspect(self).mapper.column_attrs
        }

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, ", ".join([f'{k}="{v}"' for k, v in self.__dict__.items()]))
