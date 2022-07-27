from aisquared.base import BaseObject


class LocalONNXModel(BaseObject):
    """
    Interaction with an ONNX model currently saved to the local
    file system
    """

    def __init__(
            self,
            path,
            input_shape,
            input_type
    ):
        """
        Parameters
        ----------
        path : str or path-like or file-like
            The file path of the saved model
        input_shape : list
            List of integers corresponding to the input dimensions of the model,
            ignoring the number of samples as the first dimension
        input_type : str
            Input type to the model. Must be one of 'cv', 'text', or 'tabular'
        """
        super().__init__()
        self.path = path
        self.input_shape = input_shape
        self.input_type = input_type

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def input_shape(self):
        return self._input_shape

    @input_shape.setter
    def input_shape(self, value):
        if not isinstance(value, list) or not all([isinstance(val, int) for val in value]):
            raise TypeError('input_shape must be list of integers')
        self._input_shape = value

    @property
    def input_type(self):
        return self._input_type

    @input_type.setter
    def input_type(self, value):
        self._input_type = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'LocalONNXModel',
            'params': {
                'path': self.path,
                'inputShape': self.input_shape,
                'inputType': self.input_type
            }
        }
