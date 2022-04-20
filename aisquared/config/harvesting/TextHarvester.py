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
        regex = None,
        flags = 'gu'
    ):
        """
        Parameters
        ----------
        how : str (default 'all')
            How to harvest text (supports ['how', 'all'])
        regex : str or None (default None)
            Javascript-compatible regular expression to use to harvest individual strings
        flags : str or None (default 'gu')
            Flags to use with the Regex
        """
        super().__init__()
        self.how = how
        self.regex = regex
        self.flags = flags

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

    @property
    def flags(self):
        return self._flags
    @flags.setter
    def flags(self, value):
        self._flags = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'TextHarvester',
            'params' : {
                'how' : self.how,
                'regex' : self.regex,
                'flags' : self.flags
            }
        }
