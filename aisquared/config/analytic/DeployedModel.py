from aisquared.base import BaseObject


class DeployedModel(BaseObject):
    """
    Interaction with a remote model

    Example usage:

    >>> import aisquared
    >>> analytic = aisquared.config.analytic.DeployedModel(
        'model_url',
        'text'
    )
    >>> analytic.to_dict()
    {'className': 'DeployedModel',
    'params': {'url': 'model_url',
    'inputType': 'text',
    'headers': None,
    'bodyKey': None,
    'returnKey': None}}

    """

    def __init__(
        self,
        url: str,
        input_type: str,
        headers: dict = None,
        body_key: str = None,
        return_key: str = None
    ):
        """
        Parameters
        ----------
        url : str
            The base URL for the remote endpoint
        input_type : str
            The input type to the model. Either one of 'cv', 'text', or 'tabular'
        headers : dict or None (default None)
            Headers to use when calling the endpoint
        body_key : str or None (default None)
            The key to use for the data to be sent to the endpoint
        return_key : str or None (default None)
            The key to parse the returned value from
        """
        super().__init__()
        self.url = url
        self.input_type = input_type
        self.headers = headers
        self.body_key = body_key
        self.return_key = return_key

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
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value

    @property
    def body_key(self):
        return self._body_key

    @body_key.setter
    def body_key(self, value):
        self._body_key = value

    @property
    def return_key(self):
        return self._return_key

    @return_key.setter
    def return_key(self, value):
        self._return_key = value

    def to_dict(self) -> dict:
        """
        Get the config object as a dictionary
        """
        return {
            'className': 'DeployedModel',
            'params': {
                'url': self.url,
                'inputType': self.input_type,
                'headers': self.headers,
                'bodyKey': self.body_key,
                'returnKey': self.return_key
            }
        }
