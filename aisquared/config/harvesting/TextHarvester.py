from aisquared.base import BaseObject

_ALLOWED_HOWS = [
    'all',
    'regex',
    'keywords'
]


class TextHarvester(BaseObject):
    """
    Object to harvest text
    """

    def __init__(
        self,
        how=_ALLOWED_HOWS[0],
        regex=None,
        flags='gu',
        body_only=False,
        keywords=None,
        limit=None
    ):
        """
        Parameters
        ----------
        how : str (default 'all')
            How to harvest text (supports ['all', 'regex', 'keywords'])
        regex : str or None (default None)
            Javascript-compatible regular expression to use to harvest individual strings
        flags : str or None (default 'gu')
            Flags to use with the Regex
        body_only : bool (default False)
            Whether to only harvest text from the body of the webpage
        keywords : list of str or None (default None)
            If provided, keywords to search for
        limit : int or None (default None)
            The limit to the number of times to perform the harvesting, if provided
        """
        super().__init__()
        self.how = how
        self.regex = regex
        self.flags = flags
        self.body_only = body_only
        self.keywords = keywords
        self.limit = limit

    @property
    def how(self):
        return self._how

    @how.setter
    def how(self, value):
        if value not in _ALLOWED_HOWS:
            raise ValueError(
                f"how must be one of {_ALLOWED_HOWS}, got {value}")
        self._how = value

    @property
    def regex(self):
        return self._regex

    @regex.setter
    def regex(self, value):
        self._regex = str(value) if value is not None else value

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value

    @property
    def body_only(self):
        return self._body_only

    @body_only.setter
    def body_only(self, value):
        if not isinstance(value, bool):
            raise TypeError('body_only must be Boolean')
        self._body_only = value

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, value):
        if not isinstance(value, int) and value is not None:
            raise TypeError('limit must be int or None')
        self._limit = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        if self.how == 'keywords':
            return {
                'className': 'TextHarvester',
                'params': {
                    'how': 'regex',
                    'regex': '|'.join(self.keywords),
                    'flags': self.flags,
                    'bodyOnly': self.body_only,
                    'limit': self.limit
                }
            }

        return {
            'className': 'TextHarvester',
            'params': {
                'how': self.how,
                'regex': self.regex,
                'flags': self.flags,
                'bodyOnly': self.body_only,
                'limit': self.limit
            }
        }
