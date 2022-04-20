from aisquared.base import BaseObject

class InputHarvester(BaseObject):
    """
    Object to harvest user-input text
    """
    def __init__(
            self,
            input_type = 'text',
            max_length = None
    ):
        """
        Parameters
        ----------
        input_type : str (default 'text')
            What kind of input to harvest
            NOTE: Currently only supports 'text'
        max_length : int or None (default None)
            The maximum length of harvested text
        """
        super().__init__()
        self.input_type = input_type
        self.max_length = max_length

    @property
    def input_type(self):
        return self._input_type
    @input_type.setter
    def input_type(self, value):
        if value != 'text':
            raise ValueError("InputHarvester currently only supports 'text' input")
        self._input_type = value

    @property
    def max_length(self):
        return self._max_length
    @max_length.setter
    def max_length(self, value):
        if not isinstance(value, int) and value is not None:
            raise TypeError('max_length must be int or None')
        if isinstance(value, int) and value <= 0:
            raise ValueError('max_length must be positive')
        self._max_length = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'InputHarvester',
            'params' : {
                'inputType' : self.input_type,
                'maxLength' : self.max_length
            }
        }
