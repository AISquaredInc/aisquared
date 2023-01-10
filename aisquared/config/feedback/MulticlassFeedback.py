from aisquared.base import BaseObject


class MulticlassFeedback(BaseObject):
    """
    Feedback for multiclass classification

    Example Usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.feedback.MulticlassFeedback(['class1', 'class2', 'class3'])
    >>> my_obj.to_dict()
    {'className': 'MulticlassFeedback',
    'params': {'labelMap': ['class1', 'class2', 'class3']}}
    """

    def __init__(self, label_map: list):
        """
        Parameters
        ----------
        label_map : list
            List of class values
        """
        super().__init__()
        self.label_map = label_map

    @property
    def label_map(self):
        return self._label_map

    @label_map.setter
    def label_map(self, value):
        if not isinstance(value, list):
            raise TypeError('label_map must be list')
        self._label_map = value

    def to_dict(self) -> dict:
        """
        Return the object as a dictionary
        """
        return {
            'className': 'MulticlassFeedback',
            'params': {
                'labelMap': self.label_map
            }
        }
