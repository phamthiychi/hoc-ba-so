from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.inspection import inspect

class Base(DeclarativeBase):
    pass

    def to_dict(self):
        result = {}

        for c in inspect(self).mapper.column_attrs:
            value = getattr(self, c.key)
            if isinstance(value, (str, int, float)) or value is None:
                result[c.key] = value
            else:
                result[c.key] = str(value)
        return result

    @classmethod
    def from_dict(cls, data: dict):
        columns = {c.key for c in inspect(cls).mapper.column_attrs}
        filtered_data = {
            k: v for k, v in data.items() if k in columns
        }
        return cls(**filtered_data)