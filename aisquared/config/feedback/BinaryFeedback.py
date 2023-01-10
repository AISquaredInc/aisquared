from aisquared.base import BaseObject


class BinaryFeedback(BaseObject):
    """
    Feedback for binary classification

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.feedback.BinaryFeedback(['class1', 'class2'])
    >>> my_obj.to_dict()
    {'className': 'BinaryFeedback', 'params': {'labelMap': ['class1', 'class2']}}

    """

    def __init__(self, label_map: list):
        """
        Parameters
        ----------
        label_map : list of two values
            The two values to map to
        """
        super().__init__()
        self.label_map = label_map

    @property
    def label_map(self):
        return self._label_map

    @label_map.setter
    def label_map(self, value):
        if not isinstance(value, list) or len(value) != 2:
            raise ValueError('label_map must be list of length 2')
        self._label_map = value

    def to_dict(self) -> dict:
        """
        Return the object as a dictionary
        """
        return {
            'className': 'BinaryFeedback',
            'params': {
                'labelMap': self.label_map
            }
        }
