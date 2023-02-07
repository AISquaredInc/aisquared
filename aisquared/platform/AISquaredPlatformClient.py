from typing import Union

from getpass import getpass
import pandas as pd
import requests
import platform
import json
import os

if platform.system() == 'Windows':
    basedir = os.getenv('HOMEPATH')
else:
    basedir = os.getenv('HOME')

DIRECTORY = os.path.join(basedir, '.aisquared')
CONFIG_FILE = os.path.join(DIRECTORY, '.aisquared.json')


class AISquaredAPIException(Exception):
    pass


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
    Connection successful
    200

    """

    def __init__(self):

        try:
            self._load_info(CONFIG_FILE)
        except Exception as e:
            print('It appears you are not authenticated to the AI Squared Platform. Please run Client.login() before performing any action')

    def login(
        self,
        url: str = None,
        port: int = 8080,
        username: str = None,
        password: str = None
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
        port : int (default 8080)
            The API port for the call
        username : str or None (default None)
            The username
        password : str or None (default None)
            The password

        """
        if url is None:
            url = input('Enter URL: ')
        if username is None:
            username = input('Enter Username: ')
        if password is None:
            password = getpass('Enter Password: ')

        with requests.Session() as sess:
            resp = sess.post(
                f'{url}:{port}/api/v1/auth/login',
                data={
                    'username': username,
                    'password': password
                }
            )
        if resp.status_code != 200:
            raise AISquaredAPIException('Authentication failed')
        else:
            token = resp.json()['token']['access_token']

        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)

        with open(CONFIG_FILE, 'w') as f:
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

    def _load_info(self, config_file: str = CONFIG_FILE) -> None:
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

    @property
    def headers(self):
        """Headers used for authentication with the AI Squared Platform"""
        return {
            'authorization': f'Bearer {self._token}',
            'authType': 'jwt'
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

    def list_models(self, as_df: bool = True, port: int = 8080) -> Union[pd.DataFrame, dict]:
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
        port : int (default 8080)
            The API port for the call

        Returns
        -------
        models : pandas DataFrame or dictionary
            The models

        """
        with requests.Session() as sess:
            url = f'{self.base_url}:{port}/api/v1/models?userOnly=true'
            resp = sess.get(
                url,
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(json.dumps(resp.json()))

        else:
            if as_df:
                df = pd.DataFrame(resp.json()['data']['models'])
                df['name'] = df.config.apply(lambda c: c['params']['name'])
                new_cols = ['name', 'id']
                new_cols += [c for c in df.columns if c not in new_cols]
                return df[new_cols]

            return resp.json()['data']['models']

    def upload_model(self, model_file: str, port: int = 8081) -> str:
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
            The API port to use

        Returns
        -------
        successful : bool
            Whether the action was successful

        """
        with open(model_file, 'rb') as f:

            with requests.Session() as sess:
                resp = sess.post(
                    f'{self.base_url}:{port}/upload/v1/models',
                    headers=self.headers,
                    files={'model': f}
                )

        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())

        return resp.json()['data']['id']

    def get_model(self, id: str, port: int = 8080) -> dict:
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
            The API port for the call

        Returns
        -------
        data : dictionary
            Metadata about the model coupled with the model's configuration information

        """
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/api/v1/models/{id}',
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())
        return resp.json()['data']

    def delete_model(self, id: str, port: int = 8080) -> bool:
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
            The API port for the model

        Returns
        -------
        success : bool
            Whether the action was successful

        """
        with requests.Session() as sess:
            resp = sess.delete(
                f'{self.base_url}:{port}/api/v1/models/{id}',
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())
        return resp.json()['success']

    # Sharing operations for models

    def list_model_users(self, id: str, as_df: bool = True, port: int = 8080) -> Union[pd.DataFrame, dict]:
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
            The API port for the call

        Returns
        -------
        model_users : pandas DataFrame or dictionary
            The users for the model

        """
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/api/v1/models/{id}/users',
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())

        else:
            if as_df:
                return pd.DataFrame(resp.json()['data']).sort_values(by='shared', ascending=False).reset_index(drop=True)

            return resp.json()

    def share_model_with_user(self, model_id: str, user_id: str, port: int = 8080) -> bool:
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
            The API port for the call

        Returns
        -------
        success : bool
            Whether the action was successful

        """
        with requests.Session() as sess:
            resp = sess.put(
                f'{self.base_url}:{port}/api/v1/models/{model_id}/users/{user_id}',
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())
        return resp.json()['success']

    def unshare_model_with_user(self, model_id: str, user_id: str, port: int = 8080) -> bool:
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
            The API port for the call

        Returns
        -------
        success : bool
            Whether the action was successful

        """
        with requests.Session() as sess:
            resp = sess.delete(
                f'{self.base_url}:{port}/api/v1/models/{model_id}/users/{user_id}',
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())
        return resp.json()['success']

    def share_model_with_group(self, model_id: str, group_id: str, port: int = 8080) -> bool:
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
            The ID for the group to be shared with
        port : int (default 8080)
            The API port to use

        Returns
        -------
        success : bool
            Returns True if successful
        """
        with requests.Session() as sess:
            resp = sess.put(
                f'{self.base_url}:{port}/api/v1/models/{model_id}/groups/{group_id}',
                headers=self.headers
            )
        if not resp.ok:
            raise AISquaredAPIException(resp.json())
        return resp.ok

    def unshare_model_with_group(self, model_id: str, group_id: str, port: int = 8080) -> bool:
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
            The API port to use

        Returns
        -------
        success : bool
            Returns True if successful
        """
        with requests.Session() as sess:
            resp = sess.delete(
                f'{self.base_url}:{port}/api/v1/models/{model_id}/groups/{group_id}',
                headers=self.headers
            )

        if not resp.ok:
            raise AISquaredAPIException(resp.json())
        return resp.ok

    # Feedback operations

    def list_model_feedback(self, model_id: str, limit: int = 10, as_df: bool = True, port: int = 8080) -> Union[dict, pd.DataFrame]:
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
            The API port to use

        Returns
        -------
        feedback : dict or pandas DataFrame
            The feedback
        """
        with requests.Session() as sess:
            resp = sess.get(f'{self.base_url}:{port}/api/v1/feedback/models?modelId={model_id}&page=1&pageSize={limit}',
                            headers=self.headers
                            )
        if not resp.ok:
            if resp.status_code == 404:
                return None
            raise AISquaredAPIException(resp.json())
        if as_df:
            return pd.DataFrame(resp.json()['data']['modelFeedback'])
        return resp.json()['data']

    def list_prediction_feedback(self, prediction_id: str, as_df: bool = True, port: int = 8080) -> Union[pd.DataFrame, dict]:
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
            The API port to use

        Returns
        -------
        results : pandas DataFrame or dict
            The results from the platform

        """

        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/api/v1/feedback/predictions?modelId={prediction_id}',
                headers=self.headers
            )

        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())

        if as_df:
            return pd.DataFrame(resp.json()['data'])
        return resp.json()

    def list_model_prediction_feedback(self, model_id: str, as_df: bool = True, port: int = 8080) -> Union[dict, pd.DataFrame]:
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
            The API port to use

        Returns
        -------
        results : dict or pandas DataFrame
            The results from the platform
        """
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/api/v1/feedback/predictions?modelId={model_id}',
                headers=self.headers
            )
        if not resp.ok:
            raise AISquaredAPIException(resp.json())

        if as_df:
            data = resp.json()['data']
            return pd.concat([pd.json_normalize(v) for v in data.values()]).reset_index(drop=True)

        return resp.json()

    # User and group management

    def create_user(
            self,
            user_name: str,
            first_name: str,
            last_name: str,
            email: str,
            role_id: str,
            active: bool = True,
            middle_name: str = None,
            company_id: str = None,
            password: str = None,
            port: int = 8085
    ) -> dict:
        """
        Create a user within the platform

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.create_user(
            'user name',
            'first_name',
            'last_name',
            'user_email',
            'role_id'
        )
        *Dictionary with user information*

        Parameters
        ----------
        user_name : str
            The display name of the user
        first_name : str
            The user's first name
        last_name : str
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
            The API port to use

        Returns
        -------
        user_data : dict
            Metadata about the user
        """
        json_data = {
            'active': active,
            'userName': user_name,
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
            'roleId': role_id
        }

        if middle_name:
            json_data['middleName'] = middle_name
        if company_id:
            json_data['companyId'] = company_id
        if password:
            json_data['password'] = password

        with requests.Session() as sess:
            resp = sess.post(
                f'{self.base_url}:{port}/userservice/v1/user',
                json=json_data,
                headers=self.headers
            )

        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())
        else:
            return resp.json()

    def update_user(
            self,
            user_id: str,
            user_name: str,
            first_name: str,
            last_name: str,
            email: str,
            role_id: str,
            active: bool = True,
            middle_name: str = None,
            company_id: str = None,
            password: str = None,
            port: int = 8085
    ) -> bool:
        """
        Update information about a user

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.update_user(
            'user_id',
            'user name',
            'first_name',
            'last_name',
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
        first_name : str
            The first name of the user
        last_name : str
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
            The API port to use

        Returns
        -------
        success : bool
            Returns True if update is successful
        """
        json_data = {
            'active': active,
            'userName': user_name,
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
            'roleId': role_id
        }

        if active:
            json_data['active'] = active
        if middle_name:
            json_data['middleName'] = middle_name
        if company_id:
            json_data['companyId'] = company_id
        if password:
            json_data['password'] = password

        with requests.Session() as sess:
            resp = sess.put(
                f'{self.base_url}:{port}/userservice/v1/user/{user_id}',
                json=json_data,
                headers=self.headers
            )

        if not resp.ok:
            raise AISquaredAPIException(resp.json())
        else:
            return resp.ok

    def delete_user(self, user_id: str, port: int = 8085) -> bool:
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
            The API port to use

        Returns
        -------
        result : bool
            Returns True if the call is successful
        """
        with requests.Session() as sess:
            resp = sess.delete(
                f'{self.base_url}:{port}/userservice/v1/user/{user_id}',
                headers=self.headers
            )
        if resp.status_code != 204:
            raise AISquaredAPIException(resp.json())
        else:
            return True

    def get_user(self, user_id: str, port: int = 8085) -> dict:
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
            The API port to use

        Returns
        -------
        user_info : dict
            The information about the user
        """
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/userservice/v1/user/{user_id}',
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())
        else:
            return resp.json()

    def get_group(self, group_id: str, port: int = 8086) -> dict:
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
            The API port to use

        Returns
        -------
        group_info : dict
            The information about the group
        """
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/groupservice/v1/group/{group_id}',
                headers=self.headers
            )

        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())
        return resp.json()

    def create_group(self, group_name: str, role_id: str, port: int = 8086) -> dict:
        """
        Create a group in the platform

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.create_group(
            'group_name',
            'role_id'
        )
        *dictionary containing group information*

        Parameters
        ----------
        group_name : str
            The display name of the group
        role_id : str
            The role ID for the group
        port : int (default 8086)
            The API port to use

        Returns
        -------
        group_info : dict
            Metadata about the created group
        """
        with requests.Session() as sess:
            resp = sess.post(
                f'{self.base_url}:{port}/groupservice/v1/group',
                json={
                    'displayName': group_name,
                    'roleId': role_id
                },
                headers=self.headers
            )

        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())
        return resp.json()

    def delete_group(self, group_id, port=8086) -> bool:
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
            The API port to use

        Returns
        -------
        result : bool
            Returns True if successful
        """
        with requests.Session() as sess:
            resp = sess.delete(
                f'{self.base_url}:{port}/groupservice/v1/group/{group_id}',
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())
        return resp.ok

    def update_group(self, group_id: str, display_name: str, role_id: str, port: int = 8086) -> bool:
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
            The API port to use

        Returns
        -------
        success : bool
            Returns True if successful
        """
        with requests.Session() as sess:
            resp = sess.put(
                f'{self.base_url}:{port}/groupservice/v1/group/{group_id}',
                json={
                    'displayName': display_name,
                    'roleId': role_id
                },
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())
        return resp.ok

    def add_users_to_group(self, group_id: str, user_ids: list, port: int = 8086) -> bool:
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
            The API port to use

        Returns
        -------
        success : bool
            Returns True if operation was successful
        """
        with requests.Session() as sess:
            resp = sess.put(
                f'{self.base_url}:{port}/groupservice/v1/membership',
                json={
                    'groupId': group_id,
                    'userIds': user_ids
                },
                headers=self.headers
            )
        if not resp.ok:
            raise AISquaredAPIException(resp.json())
        return resp.ok

    def remove_users_from_group(self, group_id: str, user_ids: list, port: int = 8086) -> bool:
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
            The API port to use

        Returns
        -------
        success : bool
            Returns True if successful
        """
        with requests.Session() as sess:
            resp = sess.delete(
                f'{self.base_url}:{port}/groupservice/v1/membership',
                json={
                    'groupId': group_id,
                    'userIds': user_ids
                },
                headers=self.headers
            )
        if resp.ok:
            return resp.ok
        else:
            raise AISquaredAPIException(resp.json())

    def list_users(self, as_df: bool = True, port: int = 8080) -> Union[pd.DataFrame, dict]:
        """
        List all users

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.list_users()
        *DataFrame with results*

        Parameters
        ----------
        as_df : bool (default True)
            Whether to return the data as a Pandas DataFrame
        port : int (default 8080)
            The API port for the call

        Returns
        -------
        users : pandas DataFrame or dictionary
            The response from the API

        """
        with requests.Session() as sess:
            model_resp = sess.get(
                f'{self.base_url}:{port}/api/v1/models?page=1',
                headers=self.headers
            )
            if model_resp.status_code != 200:
                raise AISquaredAPIException('There was an error')
            model_id = pd.DataFrame(
                model_resp.json()['data']['models']).id.iloc[0]
            user_resp = sess.get(
                f'{self.base_url}:{port}/api/v1/models/{model_id}/users',
                headers=self.headers
            )

        if user_resp.status_code != 200:
            raise AISquaredAPIException(user_resp.json())

        if as_df:
            return pd.DataFrame(user_resp.json()['data']).iloc[:, :-1].sort_values(by='displayName').reset_index(drop=True)
        return user_resp.json()

    def list_groups(self, as_df: bool = True, port: int = 8083) -> Union[pd.DataFrame, dict]:
        """
        List all groups

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.list_groups()
        *DataFrame with results*

        Parameters
        ----------
        as_df : bool (default True)
            Whether to return the result as a pandas DataFrame
        port : int (default 8083)
            The API port for the call

        Returns
        -------
        groups : pandas DataFrame or dictionary
            The response from the API

        """
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/scim/v2/Groups?count=10&startIndex=1',
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())

        if as_df:
            resp = resp.json()
            ids = [i['id'] for i in resp['Resources']]
            names = [i['displayName'] for i in resp['Resources']]
            members = []

            members = [[(u['value'], u['display'])
                        for u in i['members'] if i != []] for i in resp['Resources']]
            return pd.DataFrame({'id': ids, 'name': names, 'members': members})

        return resp.json()

    def list_group_users(self, group_id: str, as_df: bool = True, port: int = 8083) -> Union[pd.DataFrame, dict]:
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
            The API port to use

        Returns
        -------
        users : pandas DataFrame or dictionary
            The response from the API

        """
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/scim/v2/Groups/{group_id}',
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())

        if as_df:
            resp = resp.json()
            ids = []
            names = []
            for d in resp['members']:
                ids.append(d['value'])
                names.append(d['display'])

            return pd.DataFrame({'id': ids, 'displayName': names})
        return resp.json()

    # Metrics

    def list_user_usage_metrics(self, user_id: str, period: str = 'hourly', as_df: bool = True, port: int = 8080) -> Union[dict, pd.DataFrame]:
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
            The API port to use

        Returns
        -------
        results : pandas DataFrame or dict
            The results from the platform
        """
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/api/v1/usage-metrics?period={period}&entityId={user_id}&entity=user&action=run',
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())
        if as_df:
            return pd.DataFrame(resp.json()['data']['plotXYData'])
        return resp.json()

    def list_model_usage_metrics(self, model_id: str, period: str = 'hourly', as_df: bool = True, port: int = 8080) -> Union[dict, pd.DataFrame]:
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
            The API port to use

        Returns
        -------
        results : pandas DataFrame or dict
            The results from the platform

        """
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/api/v1/usage-metrics?period={period}&entity=model&entityId={model_id}&action=run',
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())

        if as_df:
            return pd.DataFrame(resp.json()['data']['plotXYData'])

        return resp.json()

    # Additional utilities

    def get_user_id_by_name(self, name: str) -> str:
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

        Returns
        -------
        id : str
            The ID of the user

        """

        users = self.list_users()
        this_user = users[users.displayName == name]

        if this_user.shape[0] == 0:
            raise ValueError('No user of that name appears to exist')

        return this_user.id.iloc[0]

    def get_model_id_by_name(self, model_name: str) -> str:
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

        Returns
        -------
        model_id : str
            The model's ID

        """

        models = self.list_models()
        this_model = models[models.name == model_name]

        if this_model.shape[0] == 0:
            raise ValueError('No model with that name appears to exist')

        return this_model.id.iloc[0]

    def get_group_id_by_name(self, group_name: str) -> str:
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

        Returns
        -------
        group_id : str
            The ID of the group
        """
        groups = self.list_groups()
        this_group = groups[groups.name == group_name]

        if this_group.shape[0] == 0:
            raise ValueError('No group with that name appears to exist')

        return this_group.id.iloc[0]

    def test_connection(self, port: int = 8080) -> int:
        """
        Test whether there is a healthy connection to the platform

        >>> import aisquared
        >>> client = aisquared.platform.AISquaredPlatformClient()
        >>> client.test_connection()
        Connection successful
        200

        Parameters
        ----------
        port : int (default 8080)
            The API port for the call

        Returns
        -------
        status_code : int
            The status code when checking the health API

        """
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/api/v1/health'
            )
        if resp.status_code == 200:
            print('Connection successful')
        else:
            print(
                f'There may be connection issues: status code {resp.status_code}')

        return resp.status_code
