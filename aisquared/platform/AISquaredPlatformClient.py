from getpass import getpass
import pandas as pd
import requests
import platform
import json
import os


class AISquaredAPIException(Exception):
    pass


if platform.system() == 'Windows':
    basedir = os.getenv('HOMEPATH')
else:
    basedir = os.getenv('HOME')

DIRECTORY = os.path.join(basedir, '.aisquared')
CONFIG_FILE = os.path.join(DIRECTORY, '.aisquared.json')


class AISquaredPlatformClient:
    """
    Client for interacting with the AI Squared platform programmatically

    When using the client for the first time, it is important to run the `client.login()` method. When doing so, the
    client will ask for any required information interactively.
    """

    def __init__(self):

        try:
            self._load_info(CONFIG_FILE)
        except Exception as e:
            print('It appears you are not authenticated to the AI Squared Platform. Please run Client.login() before performing any action')

    def login(
        self,
        url=None,
        port=8080,
        username=None,
        password=None
    ):
        """
        Log in to the platform programmatically.  If no url, username, or password are provided, logs in interactively

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
            raise ValueError('Authentication failed')
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

    def _load_info(self, config_file=CONFIG_FILE):
        with open(config_file, 'r') as f:
            data = json.load(f)
        self._base_url = data['url']
        self._username = data['username']
        self._password = data['password']
        self._token = data['token']

    @property
    def headers(self):
        return {
            'authorization': f'Bearer {self._token}',
            'authType': 'jwt'
        }

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return '*' * len(self._password)

    @property
    def token(self):
        return '*' * len(self._token)

    @property
    def base_url(self):
        return self._base_url

    def test_connection(self, port=8080):
        """
        Test whether there is a healthy connection to the platform

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

    def list_models(self, as_df=True, all=False, port=8080):
        """
        List models within the platform

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

    def upload_model(self, model_file, port=8081):
        """
        Upload a model to the platform

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

    def get_model(self, id, port=8080):
        """
        Retrieve a model configuration

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

    def delete_model(self, id, port=8080):
        """
        Delete a model

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

    def list_model_users(self, id, as_df=True, port=8080):
        """
        List users for a model

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

    def share_model_with_user(self, model_id, user_id, port=8080):
        """
        Share a model with a user

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
        response : dictionary
            The response from the API
        """
        with requests.Session() as sess:
            resp = sess.put(
                f'{self.base_url}:{port}/api/v1/models/{model_id}/users/{user_id}',
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())
        return resp.json()['success']

    def unshare_model_with_user(self, model_id, user_id, port=8080):
        """
        Unshare a model with a user

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

    def get_model_id_by_name(self, model_name):
        """
        Retrieve a model's ID using the name of the model

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

    # TODO

    def share_model_with_group(self, model_id, group_id, port=8083):
        """Not yet implemented"""
        raise NotImplementedError('Functionality not yet implemented')

    # TODO
    def list_model_feedback(self, model_id, port=8080):
        """Not yet implemented"""
        raise NotImplementedError('Functionality not yet implemented')
        with requests.Session() as sess:
            resp = sess.get(f'{self.base_url}:{port}/api/v1/feedback/models/{model_id}',
                            headers=self.headers
                            )
        if resp.status_code != 200:
            if resp.status_code == 404:
                return None
            raise AISquaredAPIException(resp.json())
        return resp.json()

    # TODO
    def list_prediction_feedback(self, prediction_id, port=8080):
        """Not yet implemented"""
        raise NotImplementedError('Functionality not yet implemented')

    # TODO
    def list_model_predictions(self, model_id, port=8080):
        """Not yet implemented"""
        raise NotImplementedError('Functionality not yet implemented')
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/api/v1/predictions?modelID={model_id}',
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())
        else:
            return resp

    # TODO
    def list_model_prediction_feedback(self, model_id):
        """Not yet implemented"""
        raise NotImplementedError('Functionality not yet implemented')

    def list_users(self, as_df=True, port=8080):
        """
        List all users

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

    def list_groups(self, as_df=True, port=8083):
        """
        List all groups

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

    def list_group_users(self, group_id, as_df=True, port=8083):
        """
        List users in a group

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

    def get_user_id_by_name(self, name):
        """
        Get a user's ID from their display name

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

    # TODO
    def add_user_to_group(self, group_id, user_id):
        """Not yet implemented"""
        raise NotImplementedError('Functionality not yet implemented')

    # TODO
    def remove_user_from_group(self, group_id, user_id):
        """Not yet implemented"""
        raise NotImplementedError('Functionality not yet implemented')

    # TODO
    def get_user_usage_metrics(self, user_id, port=8080):
        """Not yet implemented"""
        raise NotImplementedError('Functionality not yet implemented')
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/api/v1/usage_metrics?period=hourly&entityId={user_id}',
                headers=self.headers
            )
        if resp.status_code != 200:
            raise AISquaredAPIException(resp.json())
        return resp.json()
