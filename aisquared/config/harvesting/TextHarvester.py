from aisquared.base import BaseObject

_ALLOWED_HOWS = [
    'all',
    'regex'
]

class TextHarvester(BaseObject):
    """
    Object to harvest text
    """
    def __init__(
        self,
        how = _ALLOWED_HOWS[0],
        regex = None
    ):
        f"""
        Parameters
        ----------
        how : str (default {_ALLOWED_HOWS[0]})
            How to harvest text (supports {_ALLOWED_HOWS})
        regex : str or None (default None)
            Regular expression to use to harvest individual strings
        """
        super().__init__()
        self.how = how
        self.regex = regex

    @property
    def how(self):
        return self._how
    @how.setter
    def how(self, value):
        if value not in _ALLOWED_HOWS:
            raise ValueError(f"how must be one of {_ALLOWED_HOWS}, got {value}")
        self._how = value

    @property
    def regex(self):
        return self._regex
    @regex.setter
    def regex(self, value):
        self._regex = str(value)

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'TextHarvester',
            'params' : {
                'how' : self.how,
                'regex' : self.regex
            }
        }