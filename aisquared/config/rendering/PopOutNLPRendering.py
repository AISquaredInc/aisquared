import json

class PopOutNLPRendering:
    def __init__(
        self,
        document_list
    ):
        self.document_list = document_list

    def to_dict(self):
        return {
            'className' : 'PopOutNLPRendering',
            'params' : {
                'documentList' : self.document_list
            }
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())