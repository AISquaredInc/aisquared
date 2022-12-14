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

class AISquaredPlatformClient:

    def __init__(self):

        try:
            self.load_info(CONFIG_FILE)
        except Exception as e:
            print('It appears you are not authenticated to the AI Squared Platform. Please run Client.login() before performing any action')

    def login(
        self,
        url = None,
        port = 8080,
        username = None,
        password = None
    ):
        if url is None:
            url = input('Enter URL: ')
        if username is None:
            username = input('Enter Username: ')
        if password is None:
            password = getpass('Enter Password: ')

        with requests.Session() as sess:
            resp = sess.post(
                f'{url}:{port}/api/v1/auth/login',
                data = {
                    'username' : username,
                    'password' : password
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
                    'url' : url,
                    'username' : username,
                    'password' : password,
                    'token' : token
                },
                f
            )

        self.load_info()

    def load_info(self, config_file = CONFIG_FILE):
        with open(config_file, 'r') as f:
            data = json.load(f)
        self.base_url = data['url']
        self.username = data['username']
        self._password = data['password']
        self._token = data['token']

    @property
    def headers(self):
        return {
            'authorization' : f'Bearer {self._token}',
            'authType' : 'jwt'
        }

    def test_connection(self, port = 8080):
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/api/v1/health'
            )
        if resp.status_code == 200:
            print('Connection successful')
        else:
            print(f'There may be connection issues: status code {resp.status_code}')

    def list_models(self, as_df = False, port = 8080):
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/api/v1/models?page=1',
                headers = self.headers
            )
        if resp.status_code != 200:
            raise Exception(json.dumps(resp.json()))
        
        else:
            if as_df:
                df = pd.DataFrame(resp.json()['data']['models'])
                df['name'] = df.config.apply(lambda c : c['params']['name'])
                new_cols = ['name', 'id']
                new_cols += [c for c in df.columns if c not in new_cols]
                return df[new_cols]
            
            return resp.json()['data']['models']

    def get_model(self, id, port = 8080):
        with requests.Session() as sess:
            resp = sess.get(
                f'{self.base_url}:{port}/api/v1/models/{id}',
                headers = self.headers
            )
        if resp.status_code != 200:
            raise Exception(resp.json())
        return resp.json()
