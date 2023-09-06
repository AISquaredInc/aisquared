from aisquared.base import BaseObject


class TextRendering(BaseObject):
    """
    Class for rendering text

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.rendering.TextRendering(
        prediction_value_key = 'my_key'
    )
    >>> my_obj.to_dict()
    {'className': 'TextRendering',
    'params': {'predictionValueKey': 'my_key'}}
    """

    def __init__(
            self,
            prediction_value_key: str = None
    ):
        """
        Parameters
        ----------
        prediction_value_key : str or None (default None)
            If present, the key in the prediction to render
        """
        super().__init__()
        self.prediction_value_key = prediction_value_key

    @property
    def prediction_value_key(self):
        return self._prediction_value_key

    @prediction_value_key.setter
    def prediction_value_key(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError(
                    f'prediction_value_key must be str, got {type(value)}')
        self._prediction_value_key = value

    def to_dict(self):
        return {
            'className': 'TextRendering',
            'params': {
                'predictionValueKey': self.prediction_value_key
            }
        }
