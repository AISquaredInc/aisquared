from lib2to3.pytree import Base
from aisquared.base import BaseObject

class RegressionFeedback(BaseObject):
    
    def __init__(self):
        super().__init__()

    def to_dict(self):
        return {
            'className' : 'RegressionFeedback',
            'params' : dict()
        }