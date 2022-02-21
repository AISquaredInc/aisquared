from aisquared.base import BaseObject

class SimpleFeedback(BaseObject):
    
    def __init__(self):
        super().__init__()

    def to_dict(self):
        return {
            'className' : 'SimpleFeedback',
            'params' : dict()
        }