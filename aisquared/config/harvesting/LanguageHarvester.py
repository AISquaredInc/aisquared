from inspect import Parameter
from aisquared.base import BaseObject

class LanguageHarvester(BaseObject):
    """
    Object to harvest language/text
    """
    def __init__(
        self,
        how = 'all',
        regex = None
    ):
        """
        Parameters
        ----------
        how : str (default 'all')
            How to harvest text (supports 'all' or 'regex')
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
        if value not in ['all', 'regex']:
            raise ValueError(f"how must be one of 'all', 'regex', got {value}")
        self._how = value

    @property
    def regex(self):
        return self._regex
    @regex.setter
    def regex(self, value):
        self._regex = value

    def to_dict(self):
        return {
            'className' : 'LanguageHarvester',
            'params' : {
                'how' : self.how,
                'regex' : self.regex
            }
        }