from aisquared.base import BaseObject

class LocalModel(BaseObject):

    def __init__(
        self,
        model_path
    ):
        super().__init__()
        self.model_path = model_path

    def to_dict(self):
        return {
            'className' : 'LocalModel',
            'params' : {
                'modelPath' : self.model_path
            }
        }