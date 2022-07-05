import json


class BaseObject:
    """
    Base class used for all other classes within the aisquared package
    """

    def __init__(self):
        pass

    def to_dict(self):
        """
        Get the object as a dictionary
        """
        raise NotImplementedError

    def to_json(self):
        """
        Return the object as a json string
        """
        return json.dumps(self.to_dict())
