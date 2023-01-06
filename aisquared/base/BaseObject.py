import json


class BaseObject:
    """
    Base class used for all other classes within the aisquared package. This class is not meant
    to be used by any end user of this package, but is rather used throughout this package as a
    parent class.
    """

    def __init__(self):
        pass

    def to_dict(self) -> dict:
        """
        Get the object as a dictionary
        """
        raise NotImplementedError

    def to_json(self) -> str:
        """
        Return the object as a json string
        """
        return json.dumps(self.to_dict())
