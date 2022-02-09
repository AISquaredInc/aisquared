from aisquared.base import BaseObject

class DeployedModel(BaseObject):
    """
    Interaction with a remote model
    """
    def __init__(
        self,
        url,
        input_type,
        secret = 'request',
        format = None
    ):
        """
        Parameters
        ----------
        url : str
            The base URL for the remote endpoint
        input_type : str
            The input type to the model. Either one of 'cv' or 'text'
        secret : str (default 'request')
            The secret key used to interact with the service. Default value of 'request'
            indicates that the user inputs the key whenever the analytic is started again
        format : dict or None (default None)
            Additional formatting parameters for how to format requests
        """
        super().__init__()
        self.url = url
        self.input_type = input_type
        self.secret = secret
        self.format = format

    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, value):
        self._url = value

    @property
    def input_type(self):
        return self._input_type
    @input_type.setter
    def input_type(self, value):
        self._input_type = value

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
        """
        Get the config object as a dictionary
        """
        return {
            'className' : 'DeployedModel',
            'params' : {
                'url' : self.url,
                'inputType' : self.input_type,
                'secret' : self.secret,
                'format' : self.format
            }
        }