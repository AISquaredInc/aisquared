from aisquared.base import BaseObject


class S3Connector(BaseObject):
    """
    Interaction with an analytic stored in S3
    """

    def __init__(
        self,
        bucket,
        key
    ):
        """
        Parameters
        ----------
        bucket : str
            The bucket the file lives in
        key : str
            The key for the specific file
        """
        super().__init__()
        self.bucket = bucket
        self.key = key

    @property
    def bucket(self):
        return self._bucket

    @bucket.setter
    def bucket(self, value):
        if not isinstance(value, str):
            raise TypeError('bucket must be string')
        self._bucket = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        if not isinstance(value, str):
            raise TypeError('key must be string')
        self._key = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'S3Connector',
            'params': {
                'bucket': self.bucket,
                'key': self.key
            }
        }
