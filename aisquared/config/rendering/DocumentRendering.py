from aisquared.base import COLORS, BaseObject

class DocumentRendering(BaseObject):
    """
    Object which dictates how to render predictions on entire documents
    """

    def __init__(
        self,
        prediction_key = 'className',
        words = None,
        documents = None,
        include_probability = False,
        probability_key = 'probability',
        underline_color = COLORS[-1]
    ):
        f"""
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
        underline_color : str (default {COLORS[-1]})
        """
        super().__init__()
        self.prediction_key = prediction_key
        self.words = words
        self.documents = documents
        self.include_probability = include_probability
        self.probability_key = probability_key
        self.underline_color = underline_color

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
        if value not in COLORS:
            raise ValueError(f'color must be one of {COLORS}')
        self._underline_color = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'DocumentRendering',
            'params' : {
                'predictionKey' : self.prediction_key,
                'words' : self.words,
                'documents' : self.documents,
                'includeProbability' : self.include_probability,
                'probabilityKey' : self.probability_key,
                'underlineColor' : self.underline_color
            }
        }
