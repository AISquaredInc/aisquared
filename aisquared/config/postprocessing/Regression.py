from typing import Union
from aisquared.base import BaseObject


class Regression(BaseObject):
    """
    Postprocessing configuration object for Regression

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.postprocessing.Regression(
        10,
        100
    )
    >>> my_obj.to_dict()
    {'className': 'Regression', 'params': {'min': 10, 'max': 100, 'round': False}}

    """

    def __init__(
        self,
        min: Union[int, float] = None,
        max: Union[int, float] = None,
        round: bool = False
    ):
        """
        Parameters
        ----------
        min : None, int, or float (default None)
            The value to map an output of 0 to from the model
        max : None, int, or float (default None)
            The value to map an output of 1 to from the model
        round : bool (default False)
            Whether to round the output
        """
        super().__init__()
        self.min = min
        self.max = max
        self.round = round

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        if not isinstance(value, (float, int)) and value is not None:
            raise TypeError('min must be None, float, or int')
        self._min = value

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        if not isinstance(value, (float, int)) and value is not None:
            raise TypeError('max must be None, float, or int')
        self._max = value

    @property
    def round(self):
        return self._round

    @round.setter
    def round(self, value):
        if not isinstance(value, bool):
            raise TypeError('round must be Boolean valued')
        self._round = value

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'Regression',
            'params': {
                'min': self.min,
                'max': self.max,
                'round': self.round
            }
        }
