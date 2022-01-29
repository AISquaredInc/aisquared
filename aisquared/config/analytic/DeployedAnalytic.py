from aisquared.base import BaseObject

class DeployedAnalytic(BaseObject):
    """
    Interaction with a remote analytic
    """
    def __init__(
        self,
        url,
        secret = 'request',
        format = None
    ):
        """
        Parameters
        ----------
        url : str
            The base URL for the remote analytic
        secret : str (default 'request')
            The secret key used to interact with the service. Default value of 'request' 
            indicates that the user inputs the key whenever the analytic is started again
        format : dict or None (default None)
            Additional formatting parameters for how to format requests
        """
        super().__init__()
        self.url = url
        self.secret = secret
        self.format = format

    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, value):
        self._url = value

    @property
    def secret(self):
        return self._secret
    @secret.setter
    def secret(self, value):
        self._secret = value

    @property
    def format(self):
        return self._format
    @format.setter
    def format(self, value):
        self._format = value

    def to_dict(self):
        return {
            'className' : 'DeployedAnalytic',
            'params' : {
                'url' : self.url,
                'secret' : self.secret,
                'format' : self.format
            }
        }