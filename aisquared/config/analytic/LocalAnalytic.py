from aisquared.base import BaseObject

class LocalAnalytic(BaseObject):
    """
    Interaction with an analytic (lookup table) saved to the 
    local file system
    """

    def __init__(
        self,
        path
    ):
        super().__init__()
        self.path = path

    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, value):
        self._path = value

    def to_dict(self):
        return {
            'className' : 'LocalAnalytic',
            'params' : {
                'path' : self.path
            }
        }