from aisquared.base import BaseObject


class ReverseMLWorkflow(BaseObject):
    """
    Interaction with a ReverseML CSV stored in S3
    """

    def __init__(
        self,
        bucket,
        filename,
        column,
        period=None
    ):
        """
        Parameters
        ----------
        bucket : str
            The bucket the file lives in
        filename : str
            The name for the specific file
        column : str
            The column name in the CSV file
        period : None or int (default None)
            The period for this to run
        """
        super().__init__()
        self.bucket = bucket
        self.filename = filename
        self.column = column
        self.period = period

    @property
    def bucket(self):
        return self._bucket

    @bucket.setter
    def bucket(self, value):
        if not isinstance(value, str):
            raise TypeError('bucket must be string')
        self._bucket = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if not isinstance(value, str):
            raise TypeError('filename must be string')
        self._filename = value

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, value):
        if not isinstance(value, str):
            raise TypeError('column must be a string')
        self._column = value

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        if value is not None:
            if not isinstance(value, int):
                raise TypeError('period must be int if provided')
            if value < 1:
                raise ValueError('period must be greater than or equal to 1')
        self._period = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'ReverseMLWorkflow',
            'params': {
                'bucket': self.bucket,
                'fileName': self.filename,
                'column': self.column,
                'period': self.period
            }
        }
