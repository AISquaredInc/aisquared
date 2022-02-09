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
        """
        Parameters
        ----------
        path : str or path-like or file-like
            The path to the analytic saved on disk
        """
        super().__init__()
        self.path = path

    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, value):
        self._path = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'LocalAnalytic',
            'params' : {
                'path' : self.path
            }
        }