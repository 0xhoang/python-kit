import datetime
import json
from decimal import Decimal
from enum import Enum


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.name
        if isinstance(obj, Decimal):
            return float(obj)
        else:
            return super(CustomJSONEncoder, self).default(obj)
