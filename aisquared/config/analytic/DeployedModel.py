from aisquared.base import BaseObject

class DeployedModel(BaseObject):

    def __init__(
        self,
        url,
        secret = 'request',
        format = None
    ):
        super().__init__()
        self.url = url
        self.secret = secret
        self.format = format

    def to_dict(self):
        return {
            'className' : 'DeployedModel',
            'params' : {
                'url' : self.url,
                'secret' : self.secret,
                'format' : self.format
            }
        }