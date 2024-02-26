from aisquared.base import BaseObject


class OnnxModel(BaseObject):
    """
    Run an ONNX model locally
    """

    def __init__(
            self,
            path: str,
            input_shape: list,
            input_type: str = 'text'
    ):
        super().__init__()
        self.path = path
        self.input_shape = input_shape
        self.input_type = input_type

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, value):
        if not isinstance(value, str):
            raise TypeError(f'path must be str, got {type(value)}')
        self._path = value

    @property
    def input_shape(self):
        return self._input_shape
    
    @input_shape.setter
    def input_shape(self, value):
        if not isinstance(value, list) and not all([isinstance(v, int) for v in value]):
            raise TypeError('input_shape must be a list of integers')
        self._input_shape = value

    @property
    def input_type(self):
        return self._input_type
    
    @input_type.setter
    def input_type(self, value):
        if value not in ['text', 'cv']:
            raise ValueError(f'input_type must be one of "text", "cv", got {value}')
        self._input_type = value

    def to_dict(self):
        return {
            'className' : 'OnnxModel',
            'params' : {
                'path': self.path,
                'inputShape' : self.input_shape,
                'inputType' : self.input_type
            }
        }
