from xml.etree.ElementInclude import include
from aisquared.base import ALLOWED_COLORS, BaseObject

class DocumentRendering(BaseObject):
    
    def __init__(
        self,
        words = None,
        documents = None,
        include_probability = False,
        underline_color = ALLOWED_COLORS[-1]
    ):
        super().__init__()
        self.words = words
        self.documents = documents
        self.include_probability = include_probability
        self.underline_color = underline_color

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
