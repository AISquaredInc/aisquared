from lib2to3.pytree import Base
from aisquared.base import BaseObject

class ImageHarvester(BaseObject):

    def __init__(
        self,
        how = 'all'
    ):
        super().__init__()
        self.how = how

    def to_dict(self):
        return {
            'className' : 'ImageHarvester',
            'params' : {
                'how' : self.how
            }
        }
