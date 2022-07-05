from aisquared.base import BaseObject


class MulticlassClassification(BaseObject):
    """
    Postprocessing configuration object for multiclass classification
    """

    def __init__(
            self,
            label_map,
    ):
        """
        Parameters
        ----------
        label_map : list
            A list of values to map the output of the model to
        """
        super().__init__()
        self.label_map = label_map

    @property
    def label_map(self):
        return self._label_map

    @label_map.setter
    def label_map(self, value):
        if not isinstance(value, list):
            raise ValueError('label_map must be a list')
        if len(value) <= 2:
            raise ValueError(
                'For multiclass classification, the label map must have more than two values. If there are only two values, use the `BinaryClassification` class')
        self._label_map = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'MulticlassClassification',
            'params': {
                'labelMap': self.label_map
            }
        }
