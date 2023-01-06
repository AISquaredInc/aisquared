from aisquared.base import BaseObject


class LocalModel(BaseObject):
    """
    Interaction with a model currently saved to the local
    file system

    Example usage:

    >>> import aisquared
    >>> analytic = aisquared.config.analytic.LocalModel(
        'model_path',
        'text'
    )
    >>> analytic.to_dict()
    {'className': 'LocalModel',
    'params': {'path': 'model_path',
    'inputType': 'text'}}

    """

    def __init__(
        self,
        path: str,
        input_type: str
    ):
        """
        Parameters
        ----------
        path : str or path-like or file-like
            The file path of the saved model
        input_type : str
            Input type to the model. Must be one of 'cv', 'text', or 'tabular'
        """
        super().__init__()
        self.path = path
        self.input_type = input_type

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def input_type(self):
        return self._input_type

    @input_type.setter
    def input_type(self, value):
        self._input_type = value

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'LocalModel',
            'params': {
                'path': self.path,
                'inputType': self.input_type
            }
        }
