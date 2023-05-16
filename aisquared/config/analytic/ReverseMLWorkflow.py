from aisquared.base import BaseObject


class ReverseMLWorkflow(BaseObject):
    """
    Interaction with a ReverseML CSV stored in S3

    Example usage:

    >>> import aisquared
    >>> analytic = aisquared.config.analytic.ReverseMLWorkflow(
        'bucket_name',
        'file_name',
        'column_name',
        'text'
    )
    >>> analytic.to_dict()
    {'className': 'ReverseMLWorkflow',
    'params': {'bucket': 'bucket_name',
    'fileNames': ['file_name'],
    'inputType': 'text',
    'column': 'column_name',
    'period': None,
    'secret': ''}}

    """

    def __init__(
        self,
        bucket: str,
        filenames: list,
        column: str,
        input_type: str,
        filter_type: str,
        filter_by_columns: list = None,
        period: int = None,
        secret: str = ''
    ):
        """
        Parameters
        ----------
        bucket : str
            The bucket the file lives in
        filenames : list of str
            The names for any specific files
        column : str
            The column name in the CSV file
        input_type : str
            Either one of 'text' or 'cv'
        filter_type : str
            The filter type
        filter_by_columns : str
            How to filter the columns of the ReverseMLWorkflow
        period : None or int (default None)
            The period for this to run
        secret : str (default '')
            A secret, if needed
        """
        super().__init__()
        self.bucket = bucket
        self.filenames = filenames
        self.column = column
        self.input_type = input_type
        self.filter_type = filter_type
        self.filter_by_columns = filter_by_columns
        self.period = period
        self.secret = secret

    @property
    def bucket(self):
        return self._bucket

    @bucket.setter
    def bucket(self, value):
        if not isinstance(value, str):
            raise TypeError('bucket must be string')
        self._bucket = value

    @property
    def filenames(self):
        return self._filenames

    @filenames.setter
    def filenames(self, value):
        if isinstance(value, str):
            value = [value]
        if not isinstance(value, list):
            raise TypeError('filenames must be a list')
        if not all([isinstance(v, str) for v in value]):
            raise TypeError('filenames must all be strings')
        self._filenames = value

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, value):
        if not isinstance(value, str):
            raise TypeError('column must be a string')
        self._column = value

    @property
    def input_type(self):
        return self._input_type

    @input_type.setter
    def input_type(self, value):
        self._input_type = value

    @property
    def filter_type(self):
        return self._filter_type

    @filter_type.setter
    def filter_type(self, value):
        if not isinstance(value, str):
            raise TypeError('filter_type must be str')
        self._filter_type = value

    @property
    def filter_by_columns(self):
        return self._filter_by_columns

    @filter_by_columns.setter
    def filter_by_columns(self, value):
        if not isinstance(value, list):
            raise TypeError('filter_by_columns must be list')
        if not all([isinstance(v, dict) for v in value]):
            raise TypeError('All items in filter_by_columns must be dict')

        def _check_item(v):
            if 'inputType' not in v.keys():
                raise ValueError(
                    'All items in filter_by_columns must have "inputType" key')

            if v['inputType'] not in v.keys():
                if 'columnValue' not in v.keys():
                    raise ValueError(
                        'All items in filter_by_columns must have "columnValue" key if "inputType" is "static"')

            if 'columnName' not in v.keys():
                raise ValueError(
                    'All items in filter_by_columns must have "columnName" ke')

            if v['inputType'] not in ['group', 'input', 'static']:
                raise ValueError(
                    f'"inputType" must be one of "group", "input", or "static", got {v["inputType"]}')

            return True

        if not all([_check_item(v) for v in value]):
            raise ValueError('Not all items pass validation')

        self._filter_by_columns = value

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

    @property
    def secret(self):
        return self._secret

    @secret.setter
    def secret(self, value):
        self._secret = value

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'ReverseMLWorkflow',
            'params': {
                'bucket': self.bucket,
                'fileNames': self.filenames,
                'inputType': self.input_type,
                'filterType': self.filter_type,
                'column': self.column,
                'period': self.period,
                'secret': self.secret,
                'filterByColumns': self.filter_by_columns
            }
        }
