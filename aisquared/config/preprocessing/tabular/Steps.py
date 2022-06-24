from aisquared.base import BaseObject

class ZScore(BaseObject):
    """
    Z-Score normalization preprocessing step

    Z-Score normalization takes each supplied column value, subtracts that column's provided mean, and divides
    by the provided standard deviation.
    """
    def __init__(
            self,
            means,
            stds,
            columns = None
    ):
        """
        means : list
            List of integer or float values which are the means of the associated columns
        stds : list
            List of integer or float values which are the standard deviations of the associated columns
        columns : None or list (default None)
            If provided, is a list of column indexes to apply normalization to
        """
        super().__init__()
        self.means = means
        self.stds = stds
        self.columns = columns

        if len(self.means) != len(self.stds):
            raise ValueError('means and stds must have the same length')
        if self.columns is not None:
            if len(self.columns) != len(self.means):
                raise ValueError('Number of columns must match number of means and stds')

    @property
    def means(self):
        return self._means
    @means.setter
    def means(self, value):
        if not isinstance(value, list):
            raise TypeError('means must be a list')
        if not all([isinstance(val, (int, float)) for val in value]):
            raise TypeError('Each value in means must be int or float')
        self._means = value

    @property
    def stds(self):
        return self._stds
    @stds.setter
    def stds(self, value):
        if not isinstance(value, list):
            raise TypeError('stds must be a list')
        if not all([isinstance(val, (int, float)) for val in value]):
            raise TypeError('Each value in stds must be int or float')
        self._stds = value


    @property
    def columns(self):
        return self._columns
    @columns.setter
    def columns(self, value):
        if not isinstance(value, list) and value is not None:
            raise TypeError('If provided, columns must be list')
        if isinstance(value, list) and not all([isinstance(val, int) for val in value]):
            raise TypeError('Each value of columns must be an int')
        self._columns = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'ZScore',
            'params' : {
                'means' : self.means,
                'stds' : self.stds,
                'columns' : self.columns
            }
        }

class MinMax(BaseObject):
    """
    Min-Max Scaling preprocessing step

    Min-Max Scaling takes all associated columns and maps values relative to the minimum and maximum values
    of the training data.
    """
    def __init__(
            self,
            mins,
            maxs,
            columns = None
    ):
        """
        Parameters
        ----------
        mins : list
            List of integers or floats associated with the minimum values of each column in the training data
        maxs : list
            List of integers or floats associated with the maximum values of each column in the training data
        columns : None or list (default None)
            If provided, a list of column indexes to apply scaling to
        """
        super().__init__()
        self.mins = mins
        self.maxs = maxs
        self.columns = columns
        if len(self.mins) != len(self.maxs):
            raise ValueError('Length of mins and maxs must equal')
        if self.columns is not None:
            if len(self.mins) != len(self.columns):
                raise ValueError('Number of mins and maxs must equal the number of columns')

    @property
    def mins(self):
        return self._mins
    @mins.setter
    def mins(self, value):
        if not isinstance(value, list):
            raise TypeError('mins must be a list')
        if not all([isinstance(val, (int, float)) for val in value]):
            raise TypeError('Each value in mins must be int or float')
        self._mins = value

    @property
    def maxs(self):
        return self._maxs
    @maxs.setter
    def maxs(self, value):
        if not isinstance(value, list):
            raise TypeError('maxs must be a list')
        if not all([isinstance(val, (int, float)) for val in value]):
            raise TypeError('Each value in maxs must be int or float')
        self._maxs = value

    @property
    def columns(self):
        return self._columns
    @columns.setter
    def columns(self, value):
        if not isinstance(value, list) and value is not None:
            raise TypeError('If passed, columns must be list')
        if value is not None:
            if not all([isinstance(val, int) for val in value]):
                raise TypeError('If passed, each value in columns must be an int')
        self._columns = value
        
    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'MinMax',
            'params' : {
                'mins' : self.mins,
                'maxs' : self.maxs,
                'columns' : self.columns
            }
        }

class OneHot(BaseObject):
    """
    One Hot encoding preprocessing step
    """
    def __init__(
            self,
            column,
            values
    ):
        """
        Parameters
        ----------
        column : int
            Integer index of the column to apply one hot encoding to
        values : list
            The values, in order, to create binary columns for. Note that if a default value is intended, that
            value should simply not be provided in this list
        """
        super().__init__()
        self.column = column
        self.values = values

    @property
    def column(self):
        return self._column
    @column.setter
    def column(self, value):
        if not isinstance(value, int):
            raise TypeError('column must be integer')
        self._column = value

    @property
    def values(self):
        return self._values
    @values.setter
    def values(self, value):
        if not isinstance(value, list):
            raise TypeError('values must be list')
        self._values = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'OneHot',
            'params' : {
                'column' : self.column,
                'values' : self.values
            }
        }

class DropColumn(BaseObject):
    """
    Drop a column from tabular data
    """
    def __init__(
            self,
            column
    ):
        """
        Parameters
        ----------
        column : int
            The column index to drop
        """
        super().__init__()
        self.column = column

    @property
    def column(self):
        return self._column
    @column.setter
    def column(self, value):
        if not isinstance(value, int):
            raise ValueError('column must be integer valued')
        self._column = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'DropColumn',
            'params' : {
                'column' : self.column
            }
        }
