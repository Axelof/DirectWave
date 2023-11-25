import json
from enum import Enum
from functools import partial


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value

        return super().default(obj)


custom_encoder = CustomJsonEncoder()
custom_json_dumps = partial(json.dumps, cls=CustomJsonEncoder)
