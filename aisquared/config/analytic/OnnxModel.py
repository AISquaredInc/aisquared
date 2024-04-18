from aisquared.base import BaseObject
import base64


class OnnxModel(BaseObject):
    """
    Run an ONNX model locally
    """

    def __init__(
            self,
            path: str,
            input_shape: list,
            output_key: str,
            return_key: str = None,
            input_type: str = 'text'
    ):
        super().__init__()
        self.path = path
        self.input_shape = input_shape
        self.output_key = output_key
        self.return_key = return_key
        self.input_type = input_type

        with open(self.path, 'rb') as f:
            data = f.read()
        self.onnx_data = base64.b64encode(data).decode('ascii')

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
    def output_key(self):
        return self._output_key

    @output_key.setter
    def output_key(self, value):
        if not isinstance(value, str):
            raise TypeError('output_key must be str')
        self._output_key = value

    @property
    def return_key(self):
        return self._return_key

    @return_key.setter
    def return_key(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError('return_key must be string or None')
        self._return_key = value

    @property
    def input_type(self):
        return self._input_type

    @input_type.setter
    def input_type(self, value):
        if value not in ['text', 'cv']:
            raise ValueError(
                f'input_type must be one of "text", "cv", got {value}')
        self._input_type = value

    @property
    def onnx_data(self):
        return self._onnx_data

    @onnx_data.setter
    def onnx_data(self, value):
        if not isinstance(value, str):
            raise TypeError('onnx_data must be a string')
        self._onnx_data = value

    def to_dict(self):
        return {
            'className': 'OnnxModel',
            'params': {
                'path': self.path,
                'inputShape': self.input_shape,
                'outputKey': self.output_key,
                'returnKey': self.return_key,
                'inputType': self.input_type,
                'onnxData': self.onnx_data
            }
        }
