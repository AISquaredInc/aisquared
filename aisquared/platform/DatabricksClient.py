from typing import Union

from DatabricksAPIException import DatabricksAPIException
from aisquared.base import DIRECTORY

from getpass import getpass
import pandas as pd
import warnings
import requests
import base64
import json
import os

CLIENT_CONFIG_FILE = os.path.join(DIRECTORY, '.databricks.json')

class DatabricksClient:

    def __init__(
            self
    ):
        try:
            self._load_info(CLIENT_CONFIG_FILE)
        except Exception as e:
            warnings.warn(
                'It appears you are not authenticated to Databricks yet. Please run Client.login() before performing any action'
            )

    def login(
            self,
            url: str = None,
            username: str = None,
            token: str = None
    ) -> None:
        if url is None:
            url = input('Enter URL: ')
        if username is None:
            username = input('Enter Username: ')
        if token is None:
            token = getpass('Enter Secret Token: ')

        with open(CLIENT_CONFIG_FILE, 'w') as f:
            json.dump(
                {
                    'url' : url,
                    'username' : username,
                    'token' : token
                },
                f
            )

        self._load_info()

    def _load_info(self, config_file: str = CLIENT_CONFIG_FILE) -> None:
        with open(config_file, 'r') as f:
            data = json.load(f)

        self._base_url = data['url']
        self._username = data['username']
        self._token = data['token']

    @property
    def headers(self) -> dict:
        return {
            'authorization' : f'Bearer {self._token}',
            'Content-Type' : 'application/json'
        }
    
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def base_url(self) -> str:
        return self._base_url
    
    @property
    def token(self) -> str:
        return '*' * len(self._token)
    
    def list_workspace(self, as_df: bool = True) -> Union[pd.DataFrame, dict]:
        with requests.Session() as sess:
            resp = sess.get(
                url = f'{self.base_url}/api/2.0/workspace/list',
                headers = self.headers,
                json = {'path' : f'/Users/{self.username}'}
            )
        if not resp.ok:
            raise DatabricksAPIException(resp.text)
        
        if as_df:
            return pd.json_normalize(resp.json()['objects'])
        return resp.json()
    
    def upload_to_workspace(self, filename: str, overwrite: bool = False) -> bool:

        file_b64 = base64.b64encode(open(filename, 'rb').read()).decode('ascii')
        with requests.Session() as sess:
            resp = sess.post(
                url = f'{self.base_url}/api/2.0/workspace/import',
                headers = self.headers,
                json = {
                    'path' : f'/Users/{self.username}/{os.path.basename(filename)}',
                    'language' : 'PYTHON',
                    'overwrite' : overwrite,
                    'content' : file_b64
                }
            )
        
        if not resp.ok:
            raise DatabricksAPIException(resp.text)
        
        return resp.ok
    
    def download_from_workspace(self, filename: str) -> str:
        if not filename.startswith(f'/Users/{self.username}/'):
            filename = f'/Users/{self.username}/{filename}'
        with requests.Session() as sess:
            resp = sess.get(
                url = f'{self.base_url}/api/2.0/workspace/export',
                headers = self.headers,
                json = {
                    'path' : filename,
                    'format' : 'SOURCE',
                    'direct_download' : True
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        return resp.text
    
    def delete_from_workspace(self, filename: str) -> bool:
        if not filename.startswith(f'/Users/{self.username}/'):
            filename = f'/Users/{self.username}/{filename}'
        with requests.Session() as sess:
            resp = sess.post(
                url = f'{self.base_url}/api/2.0/workspace/delete',
                headers = self.headers,
                json = {
                    'path' : filename
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)
        
        return resp.ok

    # TODO: create_job, delete_job, run_job

    def list_jobs(self, as_df: bool = True):
        with requests.Session() as sess:
            resp = sess.get(
                url = f'{self.base_url}/api/2.1/jobs/list',
                headers = self.headers,
                json = {
                    'limit' : 100
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)
        
        if as_df:
            return pd.json_normalize(resp.json()['jobs'])

        return resp.json()

    # TODO: list_served_models, create_served_model, delete_served_model
