from aisquared.base import BaseObject


class DeployedAnalytic(BaseObject):
    """
    Interaction with a remote endpoint.

    Example usage:

    >>> import aisquared
    >>> analytic = aisquared.config.analytic.DeployedAnalytic(
        'model_url',
        'POST',
        'text',
        {
            'Content-Type' : 'application/json'
        },
        {
            'data_to_be_sent' : '{{input}}'
        },
        'string'
    )
    >>> analytic.to_dict()
    {'className': 'DeployedAnalytic',
    'params': {'url': 'model_url',
    'method': 'POST',
    'inputType': 'text',
    'headers': {'Content-Type': 'application/json'},
    'body': {'data_to_be_sent': '{{input}}'},
    'dataType': 'string'}}

    """

    def __init__(
        self,
        url: str,
        method: str,
        input_type: str,
        headers: dict = None,
        body: dict = None,
        data_type: str = 'string'
    ):
        """
        Parameters
        ----------
        url : str
            The base URL for the remote analytic
        method : str
            The method for hitting the API. Either 'POST' or 'GET'
        input_type : str
            The input types supplied to the analytic. Either one of 'cv' or 'text'
        headers : dict or None (default None)
            Header to use when calling the endpoint
        body : dict or None
            Prototype request body to be sent
        data_type : str
            The data type for the input variable to be converted to, one of 'string', 'array', 'object', or 'number'

        Notes
        -----
        - To input harvested data to the body, use the string "{{input}}"
        """
        super().__init__()
        self.url = url
        self.method = method
        self.input_type = input_type
        self.headers = headers
        self.body = body
        self.data_type = data_type

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        if not isinstance(value, str):
            raise TypeError(f'method must be str, got {type(value)}')
        if value not in ['GET', 'POST']:
            raise ValueError(
                f'method must be one of "GET", "POST", got {value}')
        self._method = value

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
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        if not isinstance(value, dict):
            raise TypeError(f'body must be dict, got {type(value)}')
        self._body = value

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, value):
        if value not in ['string', 'array', 'object', 'number']:
            raise ValueError(
                f'data_type must be one of "string", "array", "object", or "number", got {value}')
        self._data_type = value

    def to_dict(self) -> dict:
        return {
            'className': 'DeployedAnalytic',
            'params': {
                'url': self.url,
                'method': self.method,
                'inputType': self.input_type,
                'headers': self.headers,
                'body': self.body,
                'dataType': self.data_type
            }
        }
