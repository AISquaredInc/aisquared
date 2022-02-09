from aisquared.base import BaseObject

class BinaryClassification(BaseObject):
    """
    Postprocesssing configuration object for binary classification
    """

    def __init__(
        self,
        label_map,
        threshold = 0.5
    ):
        """
        Parameters
        ----------
        label_map : list
            List of two values to be mapped to the model outputs
        threshold : float (default 0.5)
            The threshold for the second value to the label map to be the one chosen
        """
        super().__init__()
        self.label_map = label_map
        self.threshold = threshold

    @property
    def label_map(self):
        return self._label_map
    @label_map.setter
    def label_map(self, value):
        if not isinstance(value, list):
            raise TypeError('label_map must be a list')
        if len(value) != 2:
            raise ValueError('label_map must have exactly two values for binary classification')
        self._label_map = value

    @property
    def threshold(self):
        return self._threshold
    @threshold.setter
    def threshold(self, value):
        if not isinstance(value, float):
            raise TypeError('threshold must be float-valued')
        if value < 0 or value > 1:
            raise ValueError('threshold value must be between 0 and 1')
        self._threshold = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'BinaryClassification',
            'params' : {
                'labelMap' : self.label_map,
                'threshold' : self.threshold
            }
        }
