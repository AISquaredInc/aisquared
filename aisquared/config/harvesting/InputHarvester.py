from aisquared.base import BaseObject

class InputHarvester(BaseObject):
    """
    Object to harvest user-input text
    """
    def __init__(
            self,
            input_type = 'text',
            max_length = None,
            features = None
    ):
        """
        Parameters
        ----------
        input_type : str (default 'text')
            What kind of input to harvest
            NOTE: Supports 'text', 'image', or 'tabular'
        max_length : int or None (default None)
            The maximum length of harvested text
        features : list or None (default None)
            Features to be harvested, if using 'tabular' harvesting.
            Otherwise ignored
        """
        super().__init__()
        self.input_type = input_type
        self.max_length = max_length
        self.features = features

    # input_type
    @property
    def input_type(self):
        return self._input_type
    @input_type.setter
    def input_type(self, value):
        if value not in ['text', 'image', 'tabular']:
            raise ValueError("InputHarvester supports 'text', 'image', or 'tabular' input")
        self._input_type = value

    # max_length
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

    # features
    @property
    def features(self):
        return self._features
    @features.setter
    def features(self, value):
        
        # Check that the value is not None
        if value is not None:
            
            # Check that the value is a list if not None
            if not isinstance(value, list):
                raise TypeError('features must be list or None')
            
            # Validate each instance in the list is a dictionary
            if not all([isinstance(val, dict) for val in value]):
                raise ValueError('Each value within `features` must be a dictionary')
            
            # Validate each of the names and dtypes for all features
            for val in value:
                if not val.get('name'):
                    raise ValueError('Each feature must have a `name` key')
                if val.get('dtype') not in ['string', 'numeric']:
                    raise ValueError('Each feature must have `dype` set to either `string` or `numeric`')
            
        self._features = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'InputHarvester',
            'params' : {
                'inputType' : self.input_type,
                'maxLength' : self.max_length,
                'features' : self.features
            }
        }
