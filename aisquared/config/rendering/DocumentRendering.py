from aisquared.base import COLORS, BaseObject

class DocumentRendering(BaseObject):
    """
    Object which dictates how to render predictions on entire documents
    """

    def __init__(
        self,
        words = None,
        documents = None,
        include_probability = False,
        underline_color = COLORS[-1]
    ):
        f"""
        Parameters
        ----------
        words : list, dict, or None (default None)
            Words to be highlighted
        documents : list, dict, or None (default None)
            Documents (typically in the form of URLs) to be recommended
        include_probability : bool (default False)
            Whether to include probabilities
        underline_color : str (default {COLORS[-1]})
        """
        super().__init__()
        self.words = words
        self.documents = documents
        self.include_probability = include_probability
        self.underline_color = underline_color

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
    def underline_color(self):
        return self._underline_color
    @underline_color.setter
    def underline_color(self, value):
        if value not in COLORS:
            raise ValueError(f'color must be one of {COLORS}')
        self._underline_color = value

    def to_dict(self):
        return {
            'className' : 'DocumentRendering',
            'params' : {
                'words' : self.words,
                'documents' : self.documents,
                'includeProbability' : self.include_probability,
                'underlineColor' : self.underline_color
            }
        }
