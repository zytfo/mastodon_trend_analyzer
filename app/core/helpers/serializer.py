# thirdparty
from sqlalchemy import inspect


class SqlalchemyEntitySerializer:
    class Meta:
        model = None
        fields = "__all__"

    def __init__(self, instance, context=None):
        self._instance = instance

        if context is None:
            context = {}
        self.context = context

    def marshal(self):
        if self.Meta.fields == "__all__":
            return self.__marshal(inspect(self._instance).mapper.column_attrs.keys())
        elif isinstance(self.Meta.fields, (list, tuple, set, frozenset)):
            return self.__marshal(self.Meta.fields)

    def __marshal(self, cols):
        return {c: self.__prepared(c) for c in cols}

    def __prepared(self, key):
        if hasattr(self, key) and callable(getattr(self, key)):
            return getattr(self, key)()
        elif hasattr(self, key):
            return getattr(self, key)
        else:
            return getattr(self._instance, key)
