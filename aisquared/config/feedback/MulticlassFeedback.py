from cProfile import label
from typing import Type
from aisquared.base import BaseObject

class MulticlassFeedback(BaseObject):
    
    def __init__(self, label_map):
        super().__init__()
        self.label_map = label_map

    @property
    def label_map(self):
        return self._label_map
    @label_map.setter
    def label_map(self, value):
        if not isinstance(value, list):
            raise TypeError('label_map must be list')
        self._label_map = value

    def to_dict(self):
        return {
            'className' : 'MulticlassFeedback',
            'params' : {
                'labelMap' : self.label_map
            }
        }