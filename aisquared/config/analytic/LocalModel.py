from aisquared.base import BaseObject

class LocalModel(BaseObject):
    """
    Interaction with a model currently saved to the local 
    file system
    """
    def __init__(
        self,
        path
    ):
        """
        Parameters
        ----------
        path : str or file-like
            The file path of the saved model
        """
        super().__init__()
        self.model_path = path

    @property
    def model_path(self):
        return self._path
    @model_path.setter
    def model_path(self, value):
        self._path = value

    def to_dict(self):
        return {
            'className' : 'LocalModel',
            'params' : {
                'path' : self.path
            }
        }