import json
from xml.etree.ElementInclude import include

class PopOutNLPRendering:
    def __init__(
        self,
        document_list
        include_prediction = True,
        include_score = True,
    ):
        self.document_list = document_list
        self.include_prediction = include_prediction
        self.include_score = include_score

    def to_dict(self):
        return {
            'className' : 'PopOutNLPRendering',
            'params' : {
                'includePrediction' : self.include_prediction,
                'includeScore' : self.include_score,
                'documentList' : self.document_list
            }
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())