from typing import Union
from aisquared.base import BaseObject


class DocumentRendering(BaseObject):
    """
    Object which dictates how to render predictions on entire documents

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.rendering.DocumentRendering()
    >>> my_obj.to_dict()
    {'className': 'DocumentRendering',
    'params': {'predictionKey': 'className',
    'words': None,
    'documents': None,
    'includeProbability': False,
    'probabilityKey': 'probability',
    'underlineColor': 'blue',
    'classes': None,
    'thresholdKey': None,
    'thresholdValue': None}}

    """

    def __init__(
        self,
        prediction_key: str = 'className',
        words: Union[list, dict, str] = None,
        documents: Union[list, dict, str] = None,
        include_probability: bool = False,
        probability_key: str = 'probability',
        underline_color: str = 'blue',
        classes: list = None,
        threshold_key: str = None,
        threshold_value: Union[int, float] = None
    ):
        """
        Parameters
        ----------
        prediction_key : str (default 'className')
            The key from the postprocessing objects to use to get the prediction
            For classification cases, use 'className'. For regression cases, use 'value'
        words : list, dict, string, or None (default None)
            Words to be highlighted
        documents : list, dict, string, or None (default None)
            Documents (typically in the form of URLs) to be recommended
        include_probability : bool (default False)
            Whether to include probabilities
        probability_key : str (default 'probability')
            Key to use to retrieve probability from results
        underline_color : str (default 'blue')
        classes : None or list (default None)
            If provided, list of classes that will be rendered
        threshold_key : None or str (default None)
            If provided, the key to threshold on
        threshold_value : None or numeric (default None)
            If provided with threshold_key, the value to threshold rendering upon
        """
        super().__init__()
        self.prediction_key = prediction_key
        self.words = words
        self.documents = documents
        self.include_probability = include_probability
        self.probability_key = probability_key
        self.underline_color = underline_color
        self.classes = classes
        self.threshold_key = threshold_key
        self.threshold_value = threshold_value

    @property
    def prediction_key(self):
        return self._prediction_key

    @prediction_key.setter
    def prediction_key(self, value):
        self._prediction_key = value

    @property
    def words(self):
        return self._words

    @words.setter
    def words(self, value):
        self._words = value

    @property
    def documents(self):
        return self._documents

    @documents.setter
    def documents(self, value):
        self._documents = value

    @property
    def include_probability(self):
        return self._include_probability

    @include_probability.setter
    def include_probability(self, value):
        self._include_probability = value

    @property
    def probability_key(self):
        return self._probability_key

    @probability_key.setter
    def probability_key(self, value):
        self._probability_key = value

    @property
    def underline_color(self):
        return self._underline_color

    @underline_color.setter
    def underline_color(self, value):
        self._underline_color = value

    @property
    def classes(self):
        return self._classes

    @classes.setter
    def classes(self, value):
        self._classes = value

    @property
    def threshold_key(self):
        return self._threshold_key

    @threshold_key.setter
    def threshold_key(self, value):
        self._threshold_key = value

    @property
    def threshold_value(self):
        return self._threshold_value

    @threshold_value.setter
    def threshold_value(self, value):
        self._threshold_value = value

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'DocumentRendering',
            'params': {
                'predictionKey': self.prediction_key,
                'words': self.words,
                'documents': self.documents,
                'includeProbability': self.include_probability,
                'probabilityKey': self.probability_key,
                'underlineColor': self.underline_color,
                'classes': self.classes,
                'thresholdKey': self.threshold_key,
                'thresholdValue': self.threshold_value
            }
        }
