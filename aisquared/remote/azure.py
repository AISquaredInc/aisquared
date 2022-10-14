try:
    from azure.storage.blob import BlobServiceClient
except:
    pass

from getpass import getpass
import platform
import stat
import json
import os

if platform.system() == 'Windows':
    basedir = os.getenv('HOMEPATH')
else:
    basedir = os.getenv('HOME')

DIRECTORY = os.path.join(basedir, '.aisquared')
AZURE_FILE = os.path.join(DIRECTORY, 'azure_config.json')


class AzureClient:
    """
    Client for interacting with and viewing models stored in Azure
    """

    def __init__(self):
        try:
            with open(AZURE_FILE, 'r') as f:
                loaded = json.load(f)
            connection_string = loaded['connectionString']
            self._client = BlobServiceClient.from_connection_string(
                connection_string)
        except Exception:
            raise RuntimeError(
                'Connection could not be made. Please ensure you have configured the connection string by running `AzureClient.configure`')

    def get_default_container(self):
        """
        Returns the name of the default container
        """
        try:
            with open(AZURE_FILE, 'r') as f:
                loaded = json.load(f)
            return loaded['defaultContainer']
        except Exception:
            raise ValueError(
                'It does not appear that a default container is configured. Try running `AzureClient.configure()` to configure')

    def list_models(self, container=None, detailed=False):
        """
        List models in storage

        Parameters
        ----------
        container : str or None (default None)
            Container to search for models in
        detailed : bool (default False)
            Whether to return additional metadata about models
        """
        if container is None:
            container = self.get_default_container()
        container_client = self._client.get_container_client(container)
        listed = container_client.list_blobs()
        if detailed:
            return list(listed)
        return [
            content['name'] for content in listed
        ]

    def delete_model(self, model_name, container=None):
        """
        Delete a model

        Parameters
        ----------
        model_name : str
            The name of the model to delete
        container : str or None (default None)
            Container to delete from
        """
        if container is None:
            container = self.get_default_container()
        container_client = self._client.get_container_client(container)
        container_client.delete_blob(model_name)

    def download_model(self, model_name, container=None):
        """
        Download a model

        Parameters
        ----------
        model_name : str
            The name of the model to download
        container : str or None (default None)
            Container to download from
        """
        if container is None:
            container = self.get_default_container()
        container_client = self._client.get_container_client(container)
        with open(model_name, 'wb') as f:
            f.write(container_client.download_blob(model_name).readall())

    def upload_model(self, model_path, container=None, overwrite=False):
        """
        Upload a model

        Parameters
        ----------
        model_path : str or path-like
            The path of the model saved locally
        container : str or None (default None)
            The container to upload to
        overwrite : bool (default False)
            Whether to overwrite model if it already exists
        """
        if container is None:
            container = self.get_default_container()
        container_client = self._client.get_container_client(container)
        object_name = os.path.basename(model_path)
        if os.path.splitext(object_name)[-1] != '.air':
            raise ValueError(
                'It does not appear that the specified file is the correct file type')
        with open(object_name, 'rb') as f:
            container_client.upload_blob(
                object_name,
                f,
                overwrite=overwrite
            )

    @staticmethod
    def configure(
        connection_string=None,
        default_container=None
    ):
        """Configure the default behavior to use"""
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)
        if connection_string is None:
            connection_string = getpass('Connection String: ')
        if default_container is None:
            default_container = input('Default Container: ')
        with open(AZURE_FILE, 'w') as f:
            json.dump(
                {
                    'connectionString': connection_string,
                    'defaultContainer': default_container
                },
                f
            )
        os.chmod(AZURE_FILE, stat.S_IREAD | stat.S_IWRITE)
