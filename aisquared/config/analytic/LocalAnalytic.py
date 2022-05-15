from aisquared.base import BaseObject

class LocalAnalytic(BaseObject):
    """
    Interaction with an analytic (lookup table) saved to the 
    local file system
    """

    def __init__(
        self,
        path,
        input_type,
    ):
        """
        Parameters
        ----------
        path : str or path-like or file-like
            The path to the analytic saved on disk
        input_type : str
            The input type to the analytic. Either one of 'cv', 'text', or 'tabular'
        """
        super().__init__()
        self.path = path
        self.input_type = input_type

    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, value):
        self._path = value

    @property
    def input_type(self):
        return self._input_type
    @input_type.setter
    def input_type(self, value):
        self._input_type = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'LocalAnalytic',
            'params' : {
                'path' : self.path,
                'inputType' : self.input_type
            }
        }