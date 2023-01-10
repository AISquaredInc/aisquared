from aisquared.base import BaseObject


class DeployedAnalytic(BaseObject):
    """
    Interaction with a remote analytic

    Example usage:

    >>> import aisquared
    >>> analytic = aisquared.config.analytic.DeployedAnalytic(
        'analytic_url',
        'text'
    )
    >>> analytic.to_dict()
    {'className': 'DeployedAnalytic',
    'params': {'url': 'analytic_url',
    'inputType': 'text',
    'secret': 'request',
    'header': None}}
    """

    def __init__(
        self,
        url: str,
        input_type: str,
        secret: str = 'request',
        header: dict = None
    ):
        """
        Parameters
        ----------
        url : str
            The base URL for the remote analytic
        input_type : str
            The input types supplied to the analytic. Either one of 'cv', 'text', or 'tabular'
        secret : str (default 'request')
            The secret key used to interact with the service. Default value of 'request'
            indicates that the user inputs the key whenever the analytic is started again
        header : dict or None (default None)
            Header to use when calling the endpoint
        """
        super().__init__()
        self.url = url
        self.input_type = input_type
        self.secret = secret
        self.header = header

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
    def header(self):
        return self._header

    @header.setter
    def header(self, value):
        self._header = value

    def to_dict(self) -> dict:
        return {
            'className': 'DeployedAnalytic',
            'params': {
                'url': self.url,
                'inputType': self.input_type,
                'secret': self.secret,
                'header': self.header
            }
        }
