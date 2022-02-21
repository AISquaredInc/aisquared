from lib2to3.pytree import Base
from aisquared.base import BaseObject

class BinaryFeedback(BaseObject):
    
    def __init__(self, label_map):
        super().__init__()
        self.label_map = label_map

    @property
    def label_map(self):
        return self._label_map
    @label_map.setter
    def label_map(self, value):
        if not isinstance(value, list) or len(value) != 2:
            raise ValueError('label_map must be list of length 2')
        self._label_map = value

    def to_dict(self):
        return {
            'className' : 'BinaryFeedback',
            'params' : {
                'labelMap' : self.label_map
            }
        }