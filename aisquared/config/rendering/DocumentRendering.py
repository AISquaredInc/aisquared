from aisquared.base import BaseObject


class DocumentRendering(BaseObject):
    """
    Object which dictates how to render predictions on entire documents
    """

    def __init__(
        self,
        prediction_key='className',
        words=None,
        documents=None,
        include_probability=False,
        probability_key='probability',
        underline_color='blue',
        classes=None,
        confidence_threshold=None,
        regression_threshold=None
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
        confidence_threshold : None or float (default None)
            The threshold for rendering, if provided
        regression_threshold : None or dict (default None)
            Information for regression rendering, with 'filter' and 'value' keys
        """
        super().__init__()
        self.prediction_key = prediction_key
        self.words = words
        self.documents = documents
        self.include_probability = include_probability
        self.probability_key = probability_key
        self.underline_color = underline_color
        self.classes = classes
        self.confidence_threshold = confidence_threshold
        self.regression_threshold = regression_threshold

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
    def confidence_threshold(self):
        return self._confidence_threshold

    @confidence_threshold.setter
    def confidence_threshold(self, value):
        self._confidence_threshold = value

    @property
    def regression_threshold(self):
        return self._regression_threshold

    @regression_threshold.setter
    def regression_threshold(self, value):
        self._regression_threshold = value

    def to_dict(self):
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
                'confidenceThreshold': self.confidence_threshold,
                'regressionThreshold': self.regression_threshold
            }
        }
