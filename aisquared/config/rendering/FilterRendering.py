from typing import Union
from aisquared.base import BaseObject, QUALIFIERS

_ALLOWED_SOURCES = [
    'inputs',
    'outputs'
]


class FilterRendering(BaseObject):
    """
    Object which dictates how predictions are to be passed to downstream analytics

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.rendering.FilterRendering(
        'inputs',
        'key',
        'gt',
        0.2
    )
    >>> my_obj.to_dict()
    {'className': 'FilterRendering',
    'params': {'source': 'inputs', 'key': 'key', 'qualifier': 'gt', 'value': 0.2}}

    """

    def __init__(
        self,
        source: str,
        key: str,
        qualifier: str,
        value: Union[list, str, int, float]
    ):
        """
        Parameters
        ----------
        source : either one of 'inputs', 'outputs'
            The source to look for the key value
        key : str
            The key to use for filtering
        qualifier : one of 'gt', 'lt', 'gte', 'lte', 'in', 'ne', 'nin'
            Qualifier to use for filtering
        value : list, string, or numeric
            The value to use to filter value on
        """
        super().__init__()
        self.source = source
        self.key = key
        self.qualifier = qualifier
        self.value = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        if value not in _ALLOWED_SOURCES:
            raise ValueError(f'source must be one of {_ALLOWED_SOURCES}')
        self._source = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        if not isinstance(value, str):
            raise TypeError('key must be string')
        self._key = value

    @property
    def qualifier(self):
        return self._qualifier

    @qualifier.setter
    def qualifier(self, value):
        if value not in QUALIFIERS:
            raise ValueError(f'qualifier must be one of {QUALIFIERS}')
        self._qualifier = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if not isinstance(val, (list, str, int, float)):
            raise TypeError('value must be list, string, or numeric')
        self._value = val

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'FilterRendering',
            'params': {
                'source': self.source,
                'key': self.key,
                'qualifier': self.qualifier,
                'value': self.value
            }
        }
