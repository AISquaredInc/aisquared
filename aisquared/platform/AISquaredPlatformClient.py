from typing import Union

from getpass import getpass
import pandas as pd
import warnings
import requests
import json
import os

from aisquared.base import DIRECTORY, CLIENT_CONFIG_FILE, ENDPOINTS

from .AISquaredAPIException import AISquaredAPIException
from .crudl import _list_models, _upload_model, _get_model, _delete_model
from .sharing import _list_model_users, _model_share_with_user, _model_share_with_group
from .feedback import _list_model_feedback, _list_prediction_feedback, _list_model_prediction_feedback
from .user_group import _create_user, _update_user, _delete_user, _get_user, _get_group, _create_group, _delete_group, _update_group, _users_to_group, _list_users, _list_groups, _list_group_users, _list_roles
from .metrics import _list_user_usage_metrics, _list_model_usage_metrics
from .additional_utils import _test_connection


class AISquaredPlatformClient:
    """
    Client for interacting with the AI Squared platform programmatically

    When using the client for the first time, it is important to run the `client.login()` method. When doing so, the
    client will ask for any required information interactively.

    >>> import aisquared
    >>> client = aisquared.platform.AISquaredPlatformClient()
    >>> # If you have never logged in before, run the following code:
    >>> client.login()
    >>> # Test connection
    >>> client.test_connection()
    True

    """

    def __init__(
        self,
        use_port: bool = False
    ):
        """
        Parameters
        ----------
        use_port : bool (default False)
            Whether to default to using the port parameter for all API calls
        """

        try:
            self._load_info(CLIENT_CONFIG_FILE)
        except Exception as e:
            warnings.warn(
                'It appears you are not authenticated to the AI Squared Platform. Please run Client.login() before performing any action'
            )

        self.use_port = use_port

    @property
    def use_port(self):
        return self._use_port

    @use_port.setter
    def use_port(self, value):
        if not isinstance(value, bool):
            raise TypeError('use_port must be Boolean')
        self._use_port = value

    def login(
        self,
        url: str = None,
        port: int = 8080,
        username: str = None,
        password: str = None,
        use_port: bool = None
    ) -> None:
        """
        Log in to the platform programmatically.  If no url, username, or password are provided, logs in interactively

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.login()
        Enter URL: https://platform.squared.ai
        Enter Username: your.email@your_domain.com
        Enter Password: <hidden>

        Parameters
        ----------
        url : str or None (default None)
            The URL for the platform API
        port : int or None (default 8080)
            The API port for the call. This can be handled automatically by the platform ALB
        username : str or None (default None)
            The username
        password : str or None (default None)
            The password
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        """
        if url is None:
            url = input('Enter URL: ')
        if username is None:
            username = input('Enter Username: ')
        if password is None:
            password = getpass('Enter Password: ')

        if use_port is None:
            use_port = self.use_port

        call_url = self._format_url(url, port, use_port)

        with requests.Session() as sess:
            resp = sess.post(
                f'{call_url}/{ENDPOINTS["login"]}',
                data={
                    'username': username,
                    'password': password
                }
            )

        if not resp.ok:
            raise AISquaredAPIException('Authentication failed')
        else:
            token = resp.json()['token']['access_token']

        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)

        with open(CLIENT_CONFIG_FILE, 'w') as f:
            json.dump(
                {
                    'url': url,
                    'username': username,
                    'password': password,
                    'token': token
                },
                f
            )

        self._load_info()

    def _load_info(self, config_file: str = CLIENT_CONFIG_FILE) -> None:
        """
        NOT MEANT TO BE CALLED BY THE USER

        Function to load configuration information for the client
        """
        with open(config_file, 'r') as f:
            data = json.load(f)
        self._base_url = data['url']
        self._username = data['username']
        self._password = data['password']
        self._token = data['token']

    def _format_url(self, url: str, port: int, use_port: bool):
        """
        NOT MEANT TO BE CALLED BY THE END USER

        Format a URL based on parameters for whether the user is interacting with the ALB or not

        Parameters
        ----------
        url : string
            The base url to format
        port : int
            The port to use
        use_port : bool
            Whether to use the port

        Returns
        -------
        formatted_url : str
            The formatted URL
        """

        if use_port:
            return f'{url}:{port}'
        else:
            return url

    @property
    def headers(self):
        """Headers used for authentication with the AI Squared Platform"""
        return {
            'authorization': f'Bearer {self._token}',
            'authType': 'jwt',
            'User-Agent': 'AI Squared/1.0'
        }

    @property
    def username(self) -> str:
        """The username associated with the client"""
        return self._username

    @property
    def password(self) -> str:
        """The password associated with the client"""
        return '*' * len(self._password)

    @property
    def token(self) -> str:
        """The token associated with the client"""
        return '*' * len(self._token)

    @property
    def base_url(self) -> str:
        """The base URL associated with the client"""
        return self._base_url

    # CRUDL operations for models

    def list_models(self, as_df: bool = True, port: int = 8080, use_port: bool = None) -> Union[pd.DataFrame, dict]:
        """
        List models within the platform

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.list_models()
        *DataFrame with results*

        Parameters
        ----------
        as_df : bool (default True)
            Whether to return the response as a pandas DataFrame
        port : default None
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        models : pandas DataFrame or dictionary
            The models

        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _list_models(url, self.headers, as_df)

    def upload_model(self, model_file: str, port: int = 8081, use_port: bool = None) -> str:
        """
        Upload a model to the platform

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.upload_model('my_model_filename.air')
        True

        Parameters
        ----------
        model_file : path or path-like
            The path to the model file
        port : int (default 8081)
            The API port to use. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        successful : bool
            Whether the action was successful

        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _upload_model(
            url,
            self.headers,
            model_file
        )

    def get_model(self, id: str, port: int = 8080, use_port: bool = None) -> dict:
        """
        Retrieve a model configuration

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.get_model('model_id')
        *JSON Response including model data and metadata*

        Parameters
        ----------
        id : str
            The ID for the model
        port : int (default 8080)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        model : dictionary
            Metadata about the model coupled with the model's configuration information

        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _get_model(url, self.headers, id)

    def delete_model(self, id: str, port: int = 8080, use_port: bool = None) -> bool:
        """
        Delete a model

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.delete_model('model_id')
        True

        Parameters
        ----------
        id : str
            The ID for the model
        port : int (default 8080)
            The API port for the model. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        success : bool
            Whether the action was successful

        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _delete_model(url, self.headers, id)

    # Sharing operations for models

    def list_model_users(self, id: str, as_df: bool = True, port: int = 8080, use_port: bool = None) -> Union[pd.DataFrame, dict]:
        """
        List users for a model

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.list_model_users('model_id')
        *DataFrame with results*

        Parameters
        ----------
        id : str
            The ID for the model
        as_df : bool (default True)
            Whether to return the response as a Pandas DataFrame
        port : int (default 8080)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        model_users : pandas DataFrame or dictionary
            The users for the model

        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _list_model_users(url, self.headers, id, as_df)

    def share_model_with_user(self, model_id: str, user_id: str, port: int = 8080, use_port: bool = None) -> bool:
        """
        Share a model with a user

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.share_model_with_user('model_id', 'user_id')
        True

        Parameters
        ----------
        model_id : str
            The ID for the model
        user_id : str
            The ID for the user
        port : int (default 8080)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        success : bool
            Whether the action was successful

        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _model_share_with_user(
            url,
            self.headers,
            model_id,
            user_id,
            True
        )

    def unshare_model_with_user(self, model_id: str, user_id: str, port: int = 8080, use_port: bool = None) -> bool:
        """
        Unshare a model with a user

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.unshare_model_with_user('model_id', 'user_id')
        True

        Parameters
        ----------
        model_id : str
            The ID for the model
        user_id : str
            The ID for the user
        port : int (default 8080)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        success : bool
            Whether the action was successful

        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _model_share_with_user(
            url,
            self.headers,
            model_id,
            user_id,
            False
        )

    def share_model_with_group(self, model_id: str, group_id: str, port: int = 8080, use_port: bool = None) -> bool:
        """
        Share a model with a group

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.share_model_with_group('model_id', 'group_id')
        True

        Parameters
        ----------
        model_id : str
            The ID for the model to be shared
        group_id : str
            The ID for the group to be shared with. This can be handled automatically by the platform ALB
        port : int (default 8080)
            The API port to use. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value


        Returns
        -------
        success : bool
            Returns True if successful
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _model_share_with_group(
            url,
            self.headers,
            model_id,
            group_id,
            True
        )

    def unshare_model_with_group(self, model_id: str, group_id: str, port: int = 8080, use_port: bool = None) -> bool:
        """
        Unshare a model with a group

        >>> import aisquared
        >>> client = aisquared.client.AISquaredPlatformClient()
        >>> client.unshare_model_with_group('model_id', 'group_id')
        True

        Parameters
        ----------
        model_id : str
            The ID of the model
        group_id : str
            The ID of the group
        port : int (default 8080)
            The API port to use. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        success : bool
            Returns True if successful
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _model_share_with_group(
            url,
            self.headers,
            model_id,
            group_id,
            False
        )

    # Feedback operations

    def list_model_feedback(self, model_id: str, limit: int = 10, as_df: bool = True, port: int = 8080, use_port: bool = None) -> Union[dict, pd.DataFrame]:
        """
        List feedback on a model

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.list_model_feedback('model_id')
        *DataFrame with Results*

        Parameters
        ----------
        model_id : str
            The ID of the model
        limit : int (default 10)
            The maximum number of feedback items to return
        port : int (default 8080)
            The API port to use. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        feedback : dict or pandas DataFrame
            The feedback
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _list_model_feedback(
            url,
            self.headers,
            model_id,
            limit,
            as_df
        )

    def list_prediction_feedback(self, prediction_id: str, as_df: bool = True, port: int = 8080, use_port: bool = None) -> Union[pd.DataFrame, dict]:
        """
        List prediction feedback given a prediction ID

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.list_prediction_feedback('prediction_id')
        *DataFrame with results*

        Parameters
        ----------
        prediction_id : str
            The prediction ID
        as_df : bool (default True)
            Whether to return the results as a pandas DataFrame
        port : int (default 8080)
            The API port to use. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        results : pandas DataFrame or dict
            The results from the platform

        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _list_prediction_feedback(
            url,
            self.headers,
            prediction_id,
            as_df
        )

    def list_model_prediction_feedback(self, model_id: str, as_df: bool = True, port: int = 8080, use_port: bool = None) -> Union[dict, pd.DataFrame]:
        """
        List all feedback for a model

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.list_model_prediction_feedback('model_id')
        *DataFrame with Results*

        Parameters
        ----------
        model_id : str
            The ID of the model requested
        as_df : bool (default True)
            Whether to return the results as a pandas DataFrame
        port : int (default 8080)
            The API port to use. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        results : dict or pandas DataFrame
            The results from the platform
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _list_model_prediction_feedback(
            url,
            self.headers,
            model_id,
            as_df
        )

    # User and group management

    def create_user(
            self,
            user_name: str,
            given_name: str,
            family_name: str,
            email: str,
            role_id: str,
            active: bool = True,
            middle_name: str = None,
            company_id: str = None,
            password: str = None,
            port: int = 8085,
            use_port: bool = None
    ) -> dict:
        """
        Create a user within the platform

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.create_user(
            'user name',
            'given_name',
            'family_name',
            'user_email',
            'role_id'
        )
        *Dictionary with user information*

        Parameters
        ----------
        user_name : str
            The display name of the user
        given_name : str
            The user's first name
        family_name : str
            The user's last name
        email : str
            The user's email
        role_id : str
            The ID of the role to be given to the user
        active : bool (default True)
            Whether the user is active
        middle_name : str or None (default None)
            The user's middle name
        company_id : str or None (default None)
            The user's company ID
        password : str or None (default None)
            The user's password
        port : int (default 8085)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        user_data : dict
            Metadata about the user
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _create_user(
            url,
            self.headers,
            user_name,
            given_name,
            family_name,
            email,
            role_id,
            active,
            middle_name,
            company_id,
            password
        )

    def update_user(
            self,
            user_id: str,
            user_name: str,
            given_name: str,
            family_name: str,
            email: str,
            role_id: str,
            active: bool = True,
            middle_name: str = None,
            company_id: str = None,
            password: str = None,
            port: int = 8085,
            use_port: bool = None
    ) -> bool:
        """
        Update information about a user

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.update_user(
            'user_id',
            'user name',
            'given_name',
            'family_name',
            'user_email',
            'role_id'
        )
        True

        Parameters
        ----------
        user_id : str
            The ID of the user to update
        user_name : str
            The display name of the user
        given_name : str
            The first name of the user
        family_name : str
            The last name of the user
        email : str
            The user's email
        role_id : str
            The ID of the user's role
        active : bool (default True)
            Whether the user is active
        middle_name : str or None (default None)
            The user's middle name
        company_id : str or None (default None)
            The user's company ID
        password : str or None (default None)
            The user's password
        port : int (default 8085)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        success : bool
            Returns True if update is successful
        """

        json_data = {
            'active': active,
            'userName': user_name,
            'givenName': given_name,
            'familyName': family_name,
            'email': email,
            'roleId': role_id
        }

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _update_user(
            url,
            self.headers,
            user_id,
            user_name,
            given_name,
            family_name,
            email,
            role_id,
            active,
            middle_name,
            company_id,
            password
        )

    def delete_user(self, user_id: str, port: int = 8085, use_port: bool = None) -> bool:
        """
        Delete a user from the system

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.delete_user('user_id')
        True

        Parameters
        ----------
        user_id : str
            The user's ID
        port : int (default 8085)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        result : bool
            Returns True if the call is successful
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _delete_user(
            url,
            self.headers,
            user_id
        )

    def get_user(self, user_id: str, port: int = 8085, use_port: bool = None) -> dict:
        """
        Retrieve a user's information from the platform

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.get_user('user_id')
        *dictionary with results*

        Parameters
        ----------
        user_id: str
            The ID of the user
        port : int (default 8085)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        user_info : dict
            The information about the user
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _get_user(url, self.headers, user_id)

    def get_group(self, group_id: str, port: int = 8086, use_port: bool = None) -> dict:
        """
        Retrieve information about a group

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.get_group('group_id')
        *dictionary containing group data*

        Parameters
        ----------
        group_id : str
            The ID of the group requested
        port : int (default 8086)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        group_info : dict
            The information about the group
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _get_group(
            url,
            self.headers,
            group_id
        )

    def create_group(self, display_name: str, role_id: str, port: int = 8086, use_port: bool = None) -> dict:
        """
        Create a group in the platform

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.create_group(
            'group display name',
            'role_id'
        )
        *dictionary containing group information*

        Parameters
        ----------
        display_name : str
            The display name of the group
        role_id : str
            The role ID for the group
        port : int (default 8086)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value


        Returns
        -------
        group_info : dict
            Metadata about the created group
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _create_group(
            url,
            self.headers,
            display_name,
            role_id
        )

    def delete_group(self, group_id, port=8086, use_port: bool = None) -> bool:
        """
        Delete a group from the platform

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.delete_group('group_id')
        True

        Parameters
        ----------
        group_id : str
            The ID of the group to delete
        port : int (default 8086)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        result : bool
            Returns True if successful
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _delete_group(
            url,
            self.headers,
            group_id
        )

    def update_group(self, group_id: str, display_name: str, role_id: str, port: int = 8086, use_port: bool = None) -> bool:
        """
        Update information about a group

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.update_group(
            'group_id',
            'group display name',
            'role_id'
        )
        True

        Parameters
        ----------
        group_id : str
            The ID of the group to update
        display_name : str
            The display name of the group
        role_id : str
            The ID of the role for the group
        port : int (default 8086)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        success : bool
            Returns True if successful
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _update_group(
            url,
            self.headers,
            group_id,
            display_name,
            role_id
        )

    def add_users_to_group(self, group_id: str, user_ids: list, port: int = 8086, use_port: bool = None) -> bool:
        """
        Add users to a group

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.add_users_to_group('group_id', ['user_id_1', 'user_id_2'])
        True

        Parameters
        ----------
        group_id : str
            The group to add the users to
        user_ids : list of str
            The IDs of the users to add
        port : int (default 8086)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        success : bool
            Returns True if operation was successful
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _users_to_group(
            url,
            self.headers,
            group_id,
            user_ids,
            True
        )

    def remove_users_from_group(self, group_id: str, user_ids: list, port: int = 8086, use_port: bool = None) -> bool:
        """
        Remove users from a group

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.remove_users_from_group('group_id', ['user_id_1', 'user_id_2'])
        True

        Parameters
        ----------
        group_id : str
            The ID of the group
        user_ids : list of str
            The IDs of the users to remove
        port : int (default = 8086)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        success : bool
            Returns True if successful
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _users_to_group(
            url,
            self.headers,
            group_id,
            user_ids,
            False
        )

    def list_users(self, max_count: int = 100, as_df: bool = True, port: int = 8080, use_port: bool = None) -> Union[pd.DataFrame, dict]:
        """
        List all users

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.list_users()
        *DataFrame with results*

        Parameters
        ----------
        max_count : int (default 100)
            The maximum number of users to return
        as_df : bool (default True)
            Whether to return the data as a Pandas DataFrame
        port : int (default 8080)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        users : pandas DataFrame or dictionary
            The response from the API

        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _list_users(
            url,
            self.headers,
            max_count,
            as_df
        )

    def list_groups(self, max_count: int = 100, as_df: bool = True, port: int = 8083, use_port: bool = None) -> Union[pd.DataFrame, dict]:
        """
        List all groups

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.list_groups()
        *DataFrame with results*

        Parameters
        ----------
        max_count : int (default 100)
            The maximum number of groups to return
        as_df : bool (default True)
            Whether to return the result as a pandas DataFrame
        port : int (default 8083)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        groups : pandas DataFrame or dictionary
            The response from the API

        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _list_groups(
            url,
            self.headers,
            max_count,
            as_df
        )

    def list_group_users(self, group_id: str, as_df: bool = True, port: int = 8083, use_port: bool = None) -> Union[pd.DataFrame, dict]:
        """
        List users in a group

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.list_group_users('group_id')
        *DataFrame with results*

        Parameters
        ----------
        group_id : str
            The ID for the group
        as_df : bool (default True)
            Whether to return the response as a pandas DataFrame
        port : int (default 8083)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        users : pandas DataFrame or dictionary
            The response from the API

        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _list_group_users(
            url,
            self.headers,
            as_df,
            group_id
        )

    def list_roles(self, as_df: bool = True, port: int = 8086, use_port: bool = None) -> Union[pd.DataFrame, dict]:
        """
        List the roles available in the platform

        Example usage:

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.list_roles()
        *DataFrame with results*

        Parameters
        ----------
        as_df : bool (default True)
            Whether to return the results as a pandas DataFrame
        port : int (default 8086)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        roles : pandas DataFrame or dict
            The roles
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _list_roles(
            url,
            self.headers,
            as_df
        )

    # Metrics

    def list_user_usage_metrics(self, user_id: str, period: str = 'hourly', as_df: bool = True, port: int = 8080, use_port: bool = None) -> Union[dict, pd.DataFrame]:
        """
        Get usage metrics for a user

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.get_user_usage_metrics('user_id')
        *DataFrame with results*

        Parameters
        ----------
        user_id : str
            The ID of the user
        period : str (default 'hourly')
            The period to group metrics into
        as_df : bool (default True)
            Whether to return results as a pandas DataFrame
        port : int (default 8080)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        results : pandas DataFrame or dict
            The results from the platform
        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _list_user_usage_metrics(
            url,
            self.headers,
            user_id,
            period,
            as_df
        )

    def list_model_usage_metrics(self, model_id: str, period: str = 'hourly', as_df: bool = True, port: int = 8080, use_port: bool = None) -> Union[dict, pd.DataFrame]:
        """
        Get usage metrics for a model

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.get_model_usage_metrics('model_id')
        *DataFrame with results*

        Parameters
        ----------
        model_id : str
            The ID of the model
        period : str (default 'hourly')
            The period to group metrics into
        as_df : bool (default True)
            Whether to return results as a pandas DataFrame
        port : int (default 8080)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value


        Returns
        -------
        results : pandas DataFrame or dict
            The results from the platform

        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _list_model_usage_metrics(
            url,
            self.headers,
            model_id,
            period,
            as_df
        )

    # Additional utilities

    def get_user_id_by_name(self, name: str, port: int = 8080, use_port: bool = None) -> str:
        """
        Get a user's ID from their display name

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.get_user_id_by_name('User Name')
        *user_id*

        Parameters
        ----------
        name : str
            The display name of the user
        port : int (default 8080)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        id : str
            The ID of the user

        """

        users = self.list_users(port=port, use_port=use_port)
        this_user = users[users.displayName == name]

        if this_user.shape[0] == 0:
            raise ValueError('No user of that name appears to exist')

        return this_user.id.iloc[0]

    def get_model_id_by_name(self, model_name: str, port: int = 8080, use_port: bool = None) -> str:
        """
        Retrieve a model's ID using the name of the model

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.get_model_id_by_name('my_awesome_model')
        *model_id*

        Parameters
        ----------
        model_name : str
            The name of the model
        port : int (default 8080)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value


        Returns
        -------
        model_id : str
            The model's ID

        """

        models = self.list_models(port=port, use_port=use_port)
        this_model = models[models.name == model_name]

        if this_model.shape[0] == 0:
            raise ValueError('No model with that name appears to exist')

        return this_model.id.iloc[0]

    def get_group_id_by_name(self, group_name: str, port: int = 8083, use_port: bool = None) -> str:
        """
        Get the ID of a group by searching for its display name

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.get_group_id_by_name('Group Name')
        *group_id*

        Parameters
        ----------
        group_name : str
            The display name of the group
        port : int (default 8083)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        group_id : str
            The ID of the group
        """

        groups = self.list_groups(port=port, use_port=use_port)
        this_group = groups[groups.name == group_name]

        if this_group.shape[0] == 0:
            raise ValueError('No group with that name appears to exist')

        return this_group.id.iloc[0]

    def get_role_id_by_role_name(self, role_name: str, port: int = 8086, use_port: bool = None) -> str:
        """
        Get the ID of a role by searching for its display name

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.get_role_id_by_role_name('Role Name')
        *role_id*

        Parameters
        ----------
        role_name : str
            The name of the role
        port : int (default 8086)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        role_id : str
            The ID of the role
        """

        roles = self.list_roles(port=port, use_port=use_port)
        this_role = roles[roles.name == role_name]

        if this_role.shape[0] == 0:
            raise ValueError('No role with that name appears to exist')

        return this_role.id.iloc[0]

    def test_connection(self, port: int = 8080, use_port: bool = None) -> bool:
        """
        Test whether there is a healthy connection to the platform

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.test_connection()
        True

        Parameters
        ----------
        port : int (default 8080)
            The API port for the call. This can be handled automatically by the platform ALB
        use_port : bool or None (default None)
            Whether to use port in URL formatting. If None, defaults to class value

        Returns
        -------
        success : bool
            True if connection was successful

        """

        if use_port is None:
            use_port = self.use_port

        url = self._format_url(self.base_url, port, use_port)

        return _test_connection(self.base_url)
