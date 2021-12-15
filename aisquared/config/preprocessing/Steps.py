import json
from typing import Type

class PreProcStep:
    """
    Base class for preprocessing steps
    """
    def to_dict(self):
        """
        Get the step as a dictionary
        """
        raise NotImplementedError

    def to_json(self):
        """
        Get the step as a JSON string
        """
        return json.dumps(self.to_dict())

class ZScore(PreProcStep):
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
        super(PreProcStep, self).__init__()
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
        return {
            'className' : 'ZScore',
            'params' : {
                'means' : self.means,
                'stds' : self.stds,
                'columns' : self.columns
            }
        }

class MinMax(PreProcStep):
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
        super(PreProcStep, self).__init__()
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
        return {
            'className' : 'MinMax',
            'params' : {
                'mins' : self.mins,
                'maxs' : self.maxs,
                'columns' : self.columns
            }
        }

class OneHot(PreProcStep):
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
        super(PreProcStep, self).__init__()
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
        return {
            'className' : 'OneHot',
            'params' : {
                'column' : self.column,
                'values' : self.values
            }
        }

class DropColumn(PreProcStep):

    def __init__(
            self,
            column
    ):
        super(PreProcStep, self).__init__()
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
        return {
            'className' : 'DropColumn',
            'params' : {
                'column' : self.column
            }
        }
    
class AddValue(PreProcStep):
    """
    Preprocessing step to add a value to all pixels in an image
    """
    def __init__(
            self,
            value
    ):
        """
        Parameters
        ----------
        value : int or float
            The value to add
        """
        super(PreProcStep, self).__init__()
        self.value = value

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('value must be int or float')
        self._value = value

    def to_dict(self):
        return {
            'className' : 'AddValue',
            'params' : {
                'value' : self.value
            }
        }

class SubtractValue(PreProcStep):
    """
    Preprocessing step to subtract a value from all pixels in an image
    """
    def __init__(
            self,
            value
    ):
        """
        Parameters
        ----------
        value : int or float
            The value to subtract
        """
        super(PreProcStep, self).__init__()
        self.value = value

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('value must be int or float')
        self._value = value

    def to_dict(self):
        return {
            'className' : 'SubtractValue',
            'params' : {
                'value' : self.value
            }
        }

class MultitplyValue(PreProcStep):
    """
    Preprocessing step to multiply all pixels in an image by a value
    """
    def __init__(
            self,
            value
    ):
        """
        Parameters
        ----------
        value : int or float
            The value to multiply all pixels by
        """
        super(PreProcStep, self).__init__()
        self.value = value

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('value must be int or float')
        self._value = value

    def to_dict(self):
        return {
            'className' : 'MultiplyValue',
            'params' : {
                'value' : self.value
            }
        }

class DivideValue(PreProcStep):
    """
    Preprocessing step to divide all pixels in an image by a value
    """
    def __init__(
            self,
            value
    ):
        """
        Parameters
        ----------
        value : int or float
            The value to divide all pixels by
        """
        super(PreProcStep, self).__init__()
        self.value = value

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('value must be int or float')
        self._value = value

    def to_dict(self):
        return {
            'className' : 'DivideValue',
            'params' : {
                'value' : self.value
            }
        }

class ConvertToColor(PreProcStep):
    """
    Preprocessing step to convert images to a color scheme
    """
    def __init__(self, color):
        """
        Parameters
        ----------
        color : str
            Either 'RGB' or 'B+W', each corresponding to RGB or grayscale color schemes, respectively
        """
        super(PreProcStep, self).__init__()
        self.color = color

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise TypeError('color must be string')
        if value not in ['RGB', 'B+W']:
            raise ValueError('color must be one of `RGB` or `B+W`')
        self._color = value

    def to_dict(self):
        return {
            'className' : 'ConvertToColor',
            'params' : {
                'color' : self.color
            }
        }
    
class Resize(PreProcStep):
    """
    Preprocessing step to resize an image
    """
    def __init__(
            self,
            size,
            method = 'bilinear',
            preserve_aspect_ratio = False,
            antialias = False
    ):
        """
        Parameters
        ----------
        size : list
            List of two integer values, supplied as [`height`, `width`], to resize images to
        method : str (default 'bilinear')
            The method to use for resizing. Must be one of 'bilinear', 'lanczos3', 'lanczos5', 'bicubic', 'gaussian',
            'nearest', or 'mitchellcubic'
        preserve_aspect_ratio : bool (default False)
            Whether to preserve aspect ratio when resizing
        antialias : bool (default False)
            Whether to apply antialiasing when downsampling an image. Has no effect when upsampling
        """
        self.size = size
        self.method = method
        self.preserve_aspect_ratio = preserve_aspect_ratio
        self.antialias = antialias

    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, value):
        if not isinstance(value, list):
            raise TypeError('size must be a list')
        if len(value) != 2 or not all([isinstance(val, int) for val in value]):
            raise ValueError('size must be a list of two integers')
        self._size = value

    @property
    def method(self):
        return self._method
    @method.setter
    def method(self, value):
        allowed_methods = [
            'bilinear',
            'lanczos3',
            'lanczos5',
            'bicubic',
            'gaussian',
            'nearest',
            'area',
            'mitchellcubic'
        ]
        if value not in allowed_methods:
            raise ValueError(f'method must be one of {allowed_methods}')
        self._method = value

    @property
    def preserve_aspect_ratio(self):
        return self._preserve_aspect_ratio
    @preserve_aspect_ratio.setter
    def preserve_aspect_ratio(self, value):
        if not isinstance(value, bool):
            raise TypeError('preserve_aspect_ratio must be bool')
        self._preserve_aspect_ratio = value

    @property
    def antialias(self):
        return self._antialias
    @antialias.setter
    def antialias(self, value):
        if not isinstance(value, bool):
            raise TypeError('antialias must be bool')
        self._antialias = value

    def to_dict(self):
        return {
            'className' : 'Resize',
            'params' : {
                'size' : self.size,
                'method' : self.method,
                'preserveAspectRatio' : self.preserve_aspect_ratio,
                'antialias' : self.antialias
            }
        }

class Tokenize(PreProcStep):
    """Preprocessing Step to tokenize text"""
    def __init__(
        self,
        split_sentences = False,
        split_words = True,
        token_pattern = '(?u)\\b\\w\\w+\\b'
    ):
        """
        Parameters
        ----------
        split_sentences : bool (default False)
            Whether to split on sentences first
        split_words : bool (default True)
            Whether to split on words
        token_pattern : str (default '(?u)\\b\\w\\w+\\b')
            Regex to tokenize on
        """
        super(PreProcStep, self).__init__()
        self.split_sentences = split_sentences
        self.split_words = split_words
        self.token_pattern = token_pattern

    @property
    def split_sentences(self):
        return self._split_sentences
    @split_sentences.setter
    def split_sentences(self, value):
        if not isinstance(value, bool):
            raise TypeError('split_sentences must be bool')
        self._split_sentences = value

    @property
    def split_words(self):
        return self._split_words
    @split_words.setter
    def split_words(self, value):
        if not isinstance(value, bool):
            raise TypeError('split_words must be bool')
        self._split_words = value

    @property
    def token_pattern(self):
        return self._token_pattern
    @token_pattern.setter
    def token_pattern(self, value):
        if not isinstance(value, str):
            raise TypeError('token_pattern must be string')
        self._token_pattern = value

    def to_dict(self):
        return {
            'className' : 'Tokenize',
            'params' : {
                'splitSentences' : self.split_sentences,
                'splitWords' : self.split_words,
                'tokenPattern' : self.token_pattern
            }
        }

class RemoveCharacters(PreProcStep):
    pass

class ConvertToCase(PreProcStep):
    pass

class ConvertToVocabulary(PreProcStep):
    pass

class PadSequences(PreProcStep):
    pass
