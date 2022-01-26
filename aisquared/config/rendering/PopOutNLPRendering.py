import json

class PopOutNLPRendering:
    """
    Object which dictates pop-out rendering for NLP use cases
    """

    def __init__(
        self,
        document_list,
        include_prediction = True,
        include_score = True,
    ):
        """
        document_list : list
            List of documents to link to for each class or in aggregate
        include_prediction : bool (default True)
            Whether to include the predicted value for the text
        include_score : bool (default True)
            Whether to include the raw predicted score for the text
        """
        self.document_list = document_list
        self.include_prediction = include_prediction
        self.include_score = include_score

    def to_dict(self):
        """Return the object as a dictionary"""
        return {
            'className' : 'PopOutNLPRendering',
            'params' : {
                'includePrediction' : self.include_prediction,
                'includeScore' : self.include_score,
                'documentList' : self.document_list
            }
        }
    
    def to_json(self):
        """Return the object as a JSON string"""
        return json.dumps(self.to_dict())