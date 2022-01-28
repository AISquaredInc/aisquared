import json

class BaseObject:

    def __init__(self):
        pass

    def to_dict(self):
        raise NotImplemented

    def to_json(self):
        return json.dumps(self.to_dict())
