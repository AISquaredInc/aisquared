from aisquared.base import BaseObject

class DeployedAnalytic(BaseObject):

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
            'className' : 'DeployedAnalytic',
            'params' : {
                'url' : self.url,
                'secret' : self.secret,
                'format' : self.format
            }
        }