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
    'header': None,
    'apiKeyHeaderName': None,
    'apiKeyPrefix': None}}
    """

    def __init__(
        self,
        url: str,
        input_type: str,
        secret: str = 'request',
        header: dict = None,
        api_key_header_name=None,
        api_key_prefix=None
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
        api_key_header_name : str or None (default None)
            The header name for the API key
        api_key_prefix : str or None (default None)
            The prefix for the API key
        """
        super().__init__()
        self.url = url
        self.input_type = input_type
        self.secret = secret
        self.header = header
        self.api_key_header_name = api_key_header_name
        self.api_key_prefix = api_key_prefix

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

    @property
    def api_key_header_name(self):
        return self._api_key_header_name

    @api_key_header_name.setter
    def api_key_header_name(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError('api_key_header_name must be str')
        self._api_key_header_name = value

    @property
    def api_key_prefix(self):
        return self._api_key_prefix

    @api_key_prefix.setter
    def api_key_prefix(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError('api_key_prefix must be str')
        self._api_key_prefix = value

    def to_dict(self) -> dict:
        return {
            'className': 'DeployedAnalytic',
            'params': {
                'url': self.url,
                'inputType': self.input_type,
                'secret': self.secret,
                'header': self.header,
                'apiKeyHeaderName': self.api_key_header_name,
                'apiKeyPrefix': self.api_key_prefix
            }
        }
