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
    """
    Client for working with a connected Databricks environment

    When using the client for the first time, it is important to authenticate the
    client using the `client.login()` method. When doing so, the client will ask for any
    required information interactively.

    >>> import aisquared
    >>> client = aisquared.platform.DatabricksClient()
    >>> # If you have never logged in before, run the following code:
    >>> client.login()
    >>> # Interactive session requesting required information
    """

    def __init__(
            self
    ):
        """
        Initialize the object
        """
        try:
            self._load_info(CLIENT_CONFIG_FILE)
        except Exception:
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
        """
        Log in to the Databricks environment programmatically

        >>> import aisquared
        >>> client = aisquared.platform.DatabricksClient()
        >>> client.login()
        Enter URL: {Databricks_workspace_url}
        Enter Username: your.email@your_domain.com
        Enter Secret Token: <hidden>

        Parameters
        ----------
        url : str or None (default None)
            The URL of the Databricks workspace
        username : str or None (default None)
            The username in the Databricks workspace
        token : str or None (default None)
            The secret token for the Databricks workspace
        persist : bool (default True)
            Whether to persist the login information, eliminating
            the need to run this command again in the future
        """
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
        """
        NOT MEANT TO BE CALLED BY THE END USER

        Load login information
        """
        with open(config_file, 'r') as f:
            data = json.load(f)

        self._base_url = data['url']
        self._username = data['username']
        self._token = data['token']

    @property
    def headers(self) -> dict:
        """API headers for calls to the API"""
        return {
            'authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json'
        }

    @property
    def username(self) -> str:
        """The user's username"""
        return self._username

    @property
    def base_url(self) -> str:
        """The base URL for the workspace"""
        return self._base_url

    @property
    def token(self) -> str:
        """The token to use for the workspace"""
        return '*' * len(self._token)

    def list_workspace(self, as_df: bool = True) -> Union[pd.DataFrame, dict]:
        """
        List files in the connected Databricks workspace

        Parameters
        ----------
        as_df : bool (default True)
            Whether to return the results as a pandas DataFrame

        Returns
        -------
        results : dict or pd.DataFrame
            The files in the workspace
        """
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
        """
        Upload a file to the workspace

        Parameters
        ----------
        filename : str
            The name of the file to upload
        overwrite : bool (default False)
            Whether to overwrite the file if one of the same name already
            exists in the workspace

        Returns
        -------
        success : bool
            Whether the upload was successful
        """
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
        """
        Download a file from the workspace

        Parameters
        ----------
        filename : str
            The filename of the file to download

        Returns
        -------
        contents : str
            The contents of the file
        """
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
        """
        Delete a file from the workspace

        Parameters
        ----------
        filename : str
            The name of the file to delete

        Returns
        -------
        success : bool
            Whether the operation is successful
        """
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

    def create_job(
            self,
            job_name: str,
            tasks: list,
            libraries: list,
            compute_name: str,
            spark_version: str,
            node_type_id: str,
            cron_syntax: str = None,
            timezone: str = None
    ) -> bool:
        """
        Create a job using notebooks and/or scripts in the workspace

        Parameters
        ----------
        job_name : str
            The name for the job
        tasks : list of dict
            List of {task_name : task_script} dictionary pairs to run in the job
        libraries : list of str
            The dependent libraries to install on all compute
        compute_name : str
            The name of the compute to provision specifically for this job
        spark_version : str
            The version of Spark to use on the compute instances
        node_type_id : str
            The node type to use
        cron_syntax : str or None (default None)
            If the job is to be set to a schedule, the cron syntax for that schedule
        timezone : str or None (default None)
            The timezone to set the schedule to, if cron syntax is provided

        Returns
        -------
        success : bool
            Whether the create job call was successful
        """

        # Create the array of libraries
        library_array = [
            {'pypi': {'package': library}} for library in libraries
        ]

        # Create the array of tasks from the name : notebook locations in the dictionary of tasks
        task_array = []
        for i in range(len(tasks)):
            task_name = list(tasks[i].keys())[0]
            task_notebook = list(tasks[i].values())[0]

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
                        'task_key': list(tasks[i - 1].keys())[0]
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

    def list_jobs(self, as_df: bool = True) -> Union[dict, pd.DataFrame]:
        """
        List all jobs in the workspace

        Parameters
        ----------
        as_df : bool (default True)
            Whether to return a pandas DataFrame

        Returns
        -------
        jobs : dict or pandas DataFrame
            The jobs that exist in the workspace
        """
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

    def delete_job(self, job_id: str) -> bool:
        """
        Delete a job from the workspace

        Parameters
        ----------
        job_id : str
            The ID of the job to delete

        Returns
        -------
        success : bool
            Whether the delete operation was successful
        """
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

    def run_job(self, job_id: str) -> int:
        """
        Run a job

        Parameters
        ----------
        job_id : str
            The ID of the job to run

        Returns
        -------
        run_id : int
            The ID of the specific run that was created
        """
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

    def update_job(
            self,
            job_id: int,
            job_name: str,
            tasks: list,
            libraries: list,
            compute_name: str,
            spark_version: str,
            node_type_id: str,
            cron_syntax: str = None,
            timezone: str = None
    ) -> bool:
        """
        Update a job by Job ID using notebooks and/or scripts in the workspace

        Parameters
        ----------
        job_id : int
            The unique identifier of the job to update
        job_name : str
            The new name for the job
        tasks : list of dict
            List of {task_name : task_script} dictionary pairs to run in the updated job
        libraries : list of str
            The dependent libraries to install on all compute for the new job
        compute_name : str
            The name of the compute to provision specifically for the new job
        spark_version : str
            The version of Spark to use on the compute instances
        node_type_id : str
            The node type to use
        cron_syntax : str or None (default None)
            If the new job is to be set to a schedule, the cron syntax for that schedule
        timezone : str or None (default None)
            The timezone to set the schedule to, if cron syntax is provided

        Returns
        -------
        success : bool
            Whether the update job call was successful
        """
        # Create the array of libraries
        library_array = [
            {'pypi': {'package': library}} for library in libraries
        ]

        # Create the array of tasks from the name : notebook locations in the dictionary of tasks
        task_array = []
        for i in range(len(tasks)):
            task_name = list(tasks[i].keys())[0]
            task_notebook = list(tasks[i].values())[0]

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
                        'task_key': list(tasks[i - 1].keys())[0]
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
                url=f'{self.base_url}/api/2.1/jobs/reset',
                headers=self.headers,
                json={
                    'job_id': job_id,
                    'new_settings': job_dict
                }
            )

        if not resp.ok:
            raise DatabricksAPIException(resp.text)

        return resp.ok

    def list_served_models(self, as_df: bool = True) -> Union[dict, pd.DataFrame]:
        """
        List served models in the workspace

        Parameters
        ----------
        as_df : bool (default True)
            Whether to return results as a pandas DataFrame

        Returns
        -------
        models : dict or pandas DataFrame
            The models served in the workspace
        """
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

    def delete_served_model(self, model_name: str) -> bool:
        """
        Delete a served model in the workspace

        Parameters
        ----------
        model_name : str
            The name of the model to delete

        Returns
        -------
        success : bool
            Whether the delete operation was successful
        """
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
            model_name: str,
            model_version: str,
            workload_size: str,
            scale_to_zero_enabled: bool = True,
            workload_type: str = 'CPU'
    ) -> dict:
        """
        Create a model serving endpoint

        Parameters
        ----------
        model_name : str
            The name of the model to serve
        model_version : str
            The version of the model to serve
        workload_size : str
            The workload size of the serving endpoint
        scale_to_zero_enabled : bool (default True)
            Whether to allow for scaling the endpoint to zero
        workload type : str (default 'CPU')
            The workload type - either 'CPU' or 'GPU'

        Returns
        -------
        configuration : dict
            Configuration information about the serving endpoint
        """
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

    def list_compute(self, as_df: bool = True) -> Union[dict, pd.DataFrame]:
        """
        List compute in the workspace

        Parameters
        ----------
        as_df : bool (default True)
            Whether to return a pandas DataFrame

        Returns
        -------
        compute : dict or pd.DataFrame
            The compute resources in the workspace
        """
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

    def delete_compute(self, compute_id: str) -> bool:
        """
        Delete a compute resource in the workspace

        Parameters
        ----------
        compute_id : str
            The ID for the compute to delete

        Returns
        -------
        success : bool
            Whether the operation was successful
        """
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
            compute_name: str,
            spark_version: str,
            node_type_id: str
    ) -> dict:
        """
        Create a compute resource

        Parameters
        ----------
        compute_name : str
            The name of the compute to create
        spark_version : str
            The spark version to use for the compute resource
        node_type_id : str
            The node type ID to use

        Returns
        -------
        compute_info : dict
            The information about the created compute resource
        """
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

    def start_compute(self, compute_id: str) -> bool:
        """
        Start a compute resource

        Parameters
        ----------
        compute_id : str
            The ID of the compute to start

        Returns
        -------
        success : bool
            Whether the start operation was successful
        """
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

    def stop_compute(self, compute_id: str) -> bool:
        """
        Stop a compute resource

        Parameters
        ----------
        compute_id : str
            The ID of the compute to start

        Returns
        -------
        success : bool
            Whether the stop operation was successful
        """
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

    def list_registered_models(self, as_df: bool = True) -> Union[dict, pd.DataFrame]:
        """
        List registered models in the workspace

        Parameters
        ----------
        as_df : bool (default True)
            Whether to return a pandas DataFrame

        Returns
        -------
        models : dict or pandas DataFrame
            The models in the workspace
        """
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

    def delete_registered_model(self, model_name: str) -> bool:
        """
        Delete a registered model

        Parameters
        ----------
        model_name : str
            The name of the model to delete

        Returns
        -------
        success : bool
            Whether the delete operation was successful
        """
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
