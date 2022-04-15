from aisquared.base import BaseObject, QUALIFIERS

class ChainRendering(BaseObject):
    """
    Object which dictates how predictions from one analytic get passed to another analytic
    """

    def __init__(
        self,
        chained_value = 'prediction',
        parameter = None,
        qualifier = None,
        value = None,
    ):
        """
        Parameters
        ----------
        chained_value : str (default 'prediction')
            What to chain, typically either 'prediction' or 'data'
        parameter : str or None (default None)
            The parameter to check the value of. If None, passes all data
        qualifier : str or None (default None)
            How to compare `parameter` to `value`. Takes values of 'greater', 'less', 'greater_equal', 'less_equal', 'equal', 'in'
        value : str, float, list, or None (default None)
            The value to compare `parameter` to using `qualifier`
        """
        super().__init__()
        self.chained_value = chained_value
        self.parameter = parameter
        self.qualifier = qualifier
        self.value = value

    @property
    def chained_value(self):
        return self._chained_value
    @chained_value.setter
    def chained_value(self, value):
        if not isinstance(value, str):
            raise TypeError('chained_value must be str')
        self._chained_value = value
    
    @property
    def parameter(self):
        return self._parameter
    @parameter.setter
    def parameter(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError('parameter must be str')
        self._parameter = value

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
    def value(self, value):
        if not isinstance(value, (str, float, list)) and value is not None:
            raise TypeError('value must be string, float, list, or None')
        self._value = value

    def to_dict(self):
        return {
            'className' : 'ChainRendering',
            'params' : {
                'chainedValue' : self.chained_value,
                'parameter' : self.parameter,
                'qualifier' : self.qualifier,
                'value' : self.value
            }
        }
