from aisquared.base import BaseObject

class ObjectDetection(BaseObject):
    """
    Postprocessing configuration object for object detection
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
            A list of values to map the output of the model to
        threshold : float (default 0.5)
            The confidence threshold to identify a detection
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
        self._label_map = value

    @property
    def threshold(self):
        return self._threshold
    @threshold.setter
    def threshold(self, value):
        if not isinstance(value, float):
            raise TypeError('threshold must be float-valued')
        if value < 0 or value > 1:
            raise ValueError('threshold must be between 0 and 1')
        self._threshold = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'ObjectDetection',
            'params' : {
                'labelMap' : self.label_map,
                'threshold' : self.threshold
            }
        }
        