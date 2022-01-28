from lib2to3.pytree import Base
from aisquared.base import BaseObject

class LanguageHarvester(BaseObject):

    def __init__(
        self,
        how = 'all',
        regex = None
    ):

        super().__init__()
        self.how = how
        self.regex = regex

    def to_dict(self):
        return {
            'className' : 'LanguageHarvester',
            'params' : {
                'how' : self.how,
                'regex' : self.regex
            }
        }