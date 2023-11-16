from typing import Union

from .DatabricksAPIException import DatabricksAPIException
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
            token: str = None,
            persist: bool = True
    ) -> None:
        if url is None:
            url = input('Enter URL: ')
        if username is None:
            username = input('Enter Username: ')
        if token is None:
            token = getpass('Enter Secret Token: ')

        if persist:
            with open(CLIENT_CONFIG_FILE, 'w') as f:
                json.dump(
                    {
                        'url': url,
                        'username': username,
                        'token': token
                    },
                    f
                )

            self._load_info()
        
        else:
            self._base_url = url
            self._username = username
            self._token = token

    def _load_info(self, config_file: str = CLIENT_CONFIG_FILE) -> None:
        with open(config_file, 'r') as f:
            data = json.load(f)

        self._base_url = data['url']
        self._username = data['username']
        self._token = data['token']

    @property
    def headers(self) -> dict:
        return {
            'authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json'
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
                url=f'{self.base_url}/api/2.0/workspace/list',
                headers=self.headers,
                json={'path': f'/Users/{self.username}'}
            )
        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        if as_df:
            return pd.json_normalize(resp.json()['objects'])
        return resp.json()

    def upload_to_workspace(self, filename: str, overwrite: bool = False) -> bool:

        file_b64 = base64.b64encode(
            open(filename, 'rb').read()).decode('ascii')
        with requests.Session() as sess:
            resp = sess.post(
                url=f'{self.base_url}/api/2.0/workspace/import',
                headers=self.headers,
                json={
                    'path': f'/Users/{self.username}/{os.path.basename(filename)}',
                    'language': 'PYTHON',
                    'overwrite': overwrite,
                    'content': file_b64
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
                url=f'{self.base_url}/api/2.0/workspace/export',
                headers=self.headers,
                json={
                    'path': filename,
                    'format': 'SOURCE',
                    'direct_download': True
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
                url=f'{self.base_url}/api/2.0/workspace/delete',
                headers=self.headers,
                json={
                    'path': filename
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        return resp.ok

    # TODO: create_job

    def create_job(
            self,
            job_name,
            tasks,
            libraries,
            compute_name,
            spark_version,
            node_type_id,
            cron_syntax=None,
            timezone=None
    ):

        # Create the array of libraries
        library_array = [
            {'pypi': {'package': library}} for library in libraries
        ]

        # Create the array of tasks from the name : notebook locations in the dictionary of tasks
        task_array = []
        for i in range(len(tasks.keys())):
            task_name = list(tasks.keys())[i]
            task_notebook = list(tasks.values())[i]

            task_dict = {
                'task_key': task_name,
                'run_if': 'ALL_SUCCESS',
                'notebook_task': {
                    'notebook_path': task_notebook,
                    'source': 'WORKSPACE'
                },
                'job_cluster_key': compute_name,
                'libraries': library_array,
                'timeout_seconds': 0,
                'email_notifications': {},
                'notification_settings': {
                    'no_alert_for_skipped_runs': False,
                    'no_alert_for_canceled_runs': False,
                    'alert_on_last_attempt': False
                },
                'webhook_notifications': {},
            }

            if i != 0:
                task_dict['depends_on'] = [
                    {
                        'task_key': list(tasks.keys())[i - 1]
                    }
                ]

            task_array.append(task_dict)

        # Create the job_clusters dictionary
        job_clusters = [{
            'job_cluster_key': compute_name,
            'new_cluster': {
                'cluster_name': '',
                'spark_version': spark_version,
                'spark_conf': {
                    'spark.master': 'local[*, 4]'
                },
                'num_workers': 0,
                'node_type_id': node_type_id,
                'enable_elastic_disk': True,
                'data_security_mode': 'LEGACY_SINGLE_USER_STANDARD',
                'runtime_engine': 'STANDARD',
                'spark_env_vars': {
                    'PYSPARK_PYTHON': '/databricks/python3/bin/python'
                }
            }
        }]

        # Create the entire json to be sent with the request
        job_dict = {
            'name': job_name,
            'email_notifications': {
                'no_alert_for_skipped_runs': False
            },
            'webhook_notifications': {},
            'timeout_seconds': 0,
            'max_concurrent_runs': 1,
            'tasks': task_array,
            'job_clusters': job_clusters,
            'run_as': {
                'user_name': self.username
            }
        }

        if cron_syntax and timezone:
            job_dict['schedule'] = {
                'quartz_cron_expression': cron_syntax,
                'timezone_id': timezone,
                'pause_status': 'UNPAUSED'
            }

        with requests.Session() as sess:
            resp = sess.post(
                url=f'{self.base_url}/api/2.1/jobs/create',
                headers=self.headers,
                json=job_dict
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        return resp.ok

    def list_jobs(self, as_df: bool = True):
        with requests.Session() as sess:
            resp = sess.get(
                url=f'{self.base_url}/api/2.1/jobs/list',
                headers=self.headers,
                json={
                    'limit': 100
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        if as_df:
            return pd.json_normalize(resp.json()['jobs'])

        return resp.json()

    def delete_job(self, job_id) -> bool:
        with requests.Session() as sess:
            resp = sess.post(
                url=f'{self.base_url}/api/2.1/jobs/delete',
                headers=self.headers,
                json={
                    'job_id': job_id
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        return resp.ok

    def run_job(self, job_id) -> int:
        with requests.Session() as sess:
            resp = sess.post(
                url=f'{self.base_url}/api/2.1/jobs/run-now',
                headers=self.headers,
                json={
                    'job_id': job_id
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        return resp.json()['run_id']

    def list_served_models(self, as_df: bool = True):
        with requests.Session() as sess:
            resp = sess.get(
                url=f'{self.base_url}/api/2.0/serving-endpoints',
                headers=self.headers
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        if as_df:
            return pd.json_normalize(resp.json()['endpoints'])
        else:
            return resp.json()

    def delete_served_model(self, model_name):
        with requests.Session() as sess:
            resp = sess.delete(
                url=f'{self.base_url}/api/2.0/serving-endpoints/{model_name}',
                headers=self.headers
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        return resp.ok

    def create_served_model(
            self,
            model_name,
            model_version,
            workload_size,
            scale_to_zero_enabled=True,
            workload_type='CPU'
    ):
        with requests.Session() as sess:
            resp = sess.post(
                url=f'{self.base_url}/api/2.0/serving-endpoints',
                headers=self.headers,
                json={
                    'name': model_name,
                    'config': {
                        'served_models': [{
                            'model_name': model_name,
                            'model_version': model_version,
                            'workload_size': workload_size,
                            'scale_to_zero_enabled': scale_to_zero_enabled,
                            'workload_type': workload_type
                        }]
                    }
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        return resp.json()

    def list_compute(self, as_df=True):
        with requests.Session() as sess:
            resp = sess.get(
                url=f'{self.base_url}/api/2.0/clusters/list',
                headers=self.headers
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        if as_df:
            return pd.json_normalize(resp.json()['clusters'])

        return resp.json()

    def delete_compute(self, compute_id):
        with requests.Session() as sess:
            resp = sess.post(
                url=f'{self.base_url}/api/2.0/clusters/permanent-delete',
                headers=self.headers,
                json={
                    'cluster_id': compute_id
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        return resp.ok

    def create_compute(
            self,
            compute_name,
            spark_version,
            node_type_id
    ):
        with requests.Session() as sess:
            resp = sess.post(
                url=f'{self.base_url}/api/2.0/clusters/create',
                headers=self.headers,
                json={
                    "cluster_name": compute_name,
                    "spark_version": spark_version,
                    "node_type_id": node_type_id,
                    "num_workers": 0,
                    "spark_conf": {
                        "spark.databricks.cluster.profile": "singleNode",
                        "spark.master": "[*, 4]"
                    },
                    "custom_tags": {
                        "ResourceClass": "SingleNode"
                    }
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        return resp.json()

    def start_compute(self, compute_id):
        with requests.Session() as sess:
            resp = sess.post(
                url=f'{self.base_url}/api/2.0/clusters/start',
                headers=self.headers,
                json={
                    'cluster_id': compute_id
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        return resp.ok

    def stop_compute(self, compute_id):
        with requests.Session() as sess:
            resp = sess.post(
                url=f'{self.base_url}/api/2.0/clusters/delete',
                headers=self.headers,
                json={
                    'cluster_id': compute_id
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        return resp.ok

    def list_registered_models(self, as_df=True):
        with requests.Session() as sess:
            resp = sess.get(
                url=f'{self.base_url}/api/2.0/mlflow/registered-models/list',
                headers=self.headers,
                json={
                    'max_results': 1000
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        if as_df:
            return pd.json_normalize(resp.json()['registered_models'])

        return resp.json()

    def delete_registered_model(self, model_name):
        with requests.Session() as sess:
            resp = sess.delete(
                url=f'{self.base_url}/api/2.0/mlflow/registered-models/delete',
                headers=self.headers,
                json={
                    'name': model_name
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        return resp.ok
