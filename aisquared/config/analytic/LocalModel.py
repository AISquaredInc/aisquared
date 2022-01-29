from aisquared.base import BaseObject

class LocalModel(BaseObject):
    """
    Interaction with a model currently saved to the local 
    file system
    """
    def __init__(
        self,
        model_path
    ):
        """
        Parameters
        ----------
        model_path : str or file-like
            The file path of the saved model
        """
        super().__init__()
        self.model_path = model_path

    @property
    def model_path(self):
        return self._model_path
    @model_path.setter
    def model_path(self, value):
        self._model_path = value

    def to_dict(self):
        return {
            'className' : 'LocalModel',
            'params' : {
                'modelPath' : self.model_path
            }
        }