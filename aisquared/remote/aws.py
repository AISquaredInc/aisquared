import platform
import boto3
import stat
import json
import os

if platform.system() == 'Windows':
    basedir = os.getenv('HOMEPATH')
else:
    basedir = os.getenv('HOME')

DIRECTORY = os.path.join(basedir, '.aisquared')
AWS_FILE = os.path.join(DIRECTORY, 'aws_config.json')


class AWSClient:
    """
    Client for interacting with and viewing models stored in AWS S3 Storage
    """

    def __init__(self):
        self._client = boto3.client('s3')

    def get_default_bucket(self):
        """
        Returns the name of the default bucket
        """
        try:
            with open(AWS_FILE, 'r') as f:
                loaded = json.load(f)
            return loaded['defaultBucket']
        except Exception:
            raise ValueError(
                'It does not appear that a default bucket is configured. Try running `AWSClient.configure()` with a default bucket name to configure')

    def list_models(self, bucket=None, detailed=False):
        """
        List models in storage

        Parameters
        ----------
        bucket : str or None (default None)
            Bucket to search for models in
        detailed : bool (default False)
            Whether to return additional metadata about models
        """
        if bucket is None:
            bucket = self.get_default_bucket()
        listed = self._client.list_objects_v2(Bucket=bucket)
        if detailed:
            return listed
        try:
            return [content['Key'] for content in listed['Contents']]
        except Exception:
            return listed

    def delete_model(self, model_name, bucket=None):
        """
        Delete a model

        Parameters
        ----------
        model_name : str
            The name of the model to delete
        bucket : str or None (default None)
            Bucket to delete from
        """
        if bucket is None:
            bucket = self.get_default_bucket()
        self._client.delete_object(Bucket=bucket, Key=model_name)

    def download_model(self, model_name, bucket=None):
        """
        Download a model

        Parameters
        ----------
        model_name : str
            The name of the model to download
        bucket : str or None (default None)
            Bucket to download from
        """
        if bucket is None:
            bucket = self.get_default_bucket()
        self._client.download_file(bucket, model_name, model_name)

    def upload_model(self, model_path, bucket=None, overwrite=False):
        """
        Upload a model

        Parameters
        ----------
        model_path : str or path-like
            The path of the model saved locally
        bucket : str or None (default None)
            The bucket to upload to
        overwrite : bool (default False)
            Whether to overwrite the model if it already exists
        """
        if bucket is None:
            bucket = self.get_default_bucket()
        object_name = os.path.basename(model_path)
        if os.path.splitext(object_name)[-1] != '.air':
            raise ValueError(
                'It does not appear that the specified file is the correct file type')
        if not overwrite:
            if object_name in self.list_models():
                raise ValueError(
                    'Model with the same name already exists. To overwrite the model, set overwrite to True')
        self._client.upload_file(model_path, bucket, object_name)

    @staticmethod
    def configure(default_bucket):
        """Configure the default behaviors to use"""
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)
        with open(AWS_FILE, 'w') as f:
            json.dump({'defaultBucket': default_bucket}, f)
        os.chmod(AWS_FILE, stat.S_IREAD | stat.S_IWRITE)
