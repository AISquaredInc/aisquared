from aisquared.base import BaseObject

_ALLOWED_PADS = [
    'pre',
    'post'
]

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
    
class AddValue(BaseObject):
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
        super().__init__()
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
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'Add',
            'params' : {
                'value' : self.value
            }
        }

class SubtractValue(BaseObject):
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
        super().__init__()
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
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'Subtract',
            'params' : {
                'value' : self.value
            }
        }

class MultitplyValue(BaseObject):
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
        super().__init__()
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
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'Multiply',
            'params' : {
                'value' : self.value
            }
        }

class DivideValue(BaseObject):
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
        super().__init__()
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
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'Divide',
            'params' : {
                'value' : self.value
            }
        }

class ConvertToColor(BaseObject):
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
        super().__init__()
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
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'ConvertToColor',
            'params' : {
                'color' : self.color
            }
        }
    
class Resize(BaseObject):
    """
    Preprocessing step to resize an image
    """
    def __init__(
            self,
            size,
            method = 'bilinear',
            preserve_aspect_ratio = False
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
        """
        super().__init__()
        self.size = size
        self.method = method
        self.preserve_aspect_ratio = preserve_aspect_ratio

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

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'Resize',
            'params' : {
                'size' : self.size,
                'method' : self.method,
                'preserveAspectRatio' : self.preserve_aspect_ratio
            }
        }

class Tokenize(BaseObject):
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
        super().__init__()
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
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'Tokenize',
            'params' : {
                'splitSentences' : self.split_sentences,
                'splitWords' : self.split_words,
                'tokenPattern' : self.token_pattern
            }
        }

class RemoveCharacters(BaseObject):
    """Preprocessing step to remove characters from text"""
    def __init__(
        self,
        remove_digits = True,
        remove_punctuation = True
    ):
        """
        Parameters
        ----------
        remove_digits : bool (default True)
            Whether to remove digits from input text
        remove_punctuation : bool (default True)
            Whether to remove punctuation from input text
        """
        super().__init__()
        self.remove_digits = remove_digits
        self.remove_punctuation = remove_punctuation

    @property
    def remove_digits(self):
        return self._remove_digits
    @remove_digits.setter
    def remove_digits(self, value):
        if not isinstance(value, bool):
            raise TypeError('remove_digits must be bool')
        self._remove_digits = value
    
    @property
    def remove_punctuation(self):
        return self._remove_punctuation
    @remove_punctuation.setter
    def remove_punctuation(self, value):
        if not isinstance(value, bool):
            raise TypeError('remove_punctuation must be bool')
        self._remove_punctuation = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'RemoveCharacters',
            'params' : {
                'removeDigits' : self.remove_digits,
                'removePunctuation' : self.remove_punctuation
            }
        }

class ConvertToCase(BaseObject):
    """Text preprocessing object to convert inputs to all lowercase or all uppercase"""
    def __init__(
        self,
        lowercase = True
    ):
        """
        Parameters
        ----------
        lowercase : bool (default True)
            Whether to convert to lower case. If False, converts to all uppercase
        """
        super().__init__()
        self.lowercase = lowercase

    @property
    def lowercase(self):
        return self._lowercase
    @lowercase.setter
    def lowercase(self, value):
        if not isinstance(value, bool):
            raise TypeError('lowercase must be bool')
        self._lowercase = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'ConvertToCase',
            'params' : {
                'lowercase' : self.lowercase
            }
        }

class ConvertToVocabulary(BaseObject):
    """Text preprocessing object to convert tokens to integer vocabularies"""
    def __init__(
        self,
        vocabulary,
        start_character = 1,
        oov_character = 2,
        max_vocab = None
    ):
        """
        Parameters
        ----------
        vocabulary : dict
            Dictionary of string -> integer mappings
        start_character : int (default 1)
            The character to use for the start of an input sequence
        oov_character : int (default 2)
            The character to use for out of vocabulary tokens
        max_vocab : int or None (default None)
            The maximum vocabulary integer to use. If None, all vocabulary are used
        """
        super().__init__()
        self.vocabulary = vocabulary
        self.start_character = start_character
        self.oov_character = oov_character
        self.max_vocab = max_vocab

    @property
    def vocabulary(self):
        return self._vocabulary
    @vocabulary.setter
    def vocabulary(self, value):
        if not isinstance(value, dict):
            raise TypeError('vocabulary must be dictionary')
        if not all([isinstance(k, str) for k in value.keys()]):
            raise ValueError('All keys in vocabulary must be strings')
        if not all([isinstance(v, int) for v in value.values()]):
            raise ValueError('All values in vocabulary must be integers')
        self._vocabulary = value

    @property
    def start_character(self):
        return self._start_character
    @start_character.setter
    def start_character(self, value):
        if not isinstance(value, int):
            raise TypeError('start_character must be int')
        self._start_character = value
    
    @property
    def oov_character(self):
        return self._oov_character
    @oov_character.setter
    def oov_character(self, value):
        if not isinstance(value, int):
            raise TypeError('oov_character must be int')
        self._oov_character = value

    @property
    def max_vocab(self):
        return self._max_vocab
    @max_vocab.setter
    def max_vocab(self, value):
        if value is not None:
            if not isinstance(value, int):
                raise TypeError('max_vocab must be int')
        self._max_vocab = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'ConvertToVocabulary',
            'params' : {
                'vocabulary' : self.vocabulary,
                'startCharacter' : self.start_character,
                'oovCharacter' : self.oov_character,
                'maxVocab' : self.max_vocab
            }
        }

class PadSequences(BaseObject):
    """Text preprocessing object to pad sequences"""
    def __init__(
        self,
        pad_character = 0,
        length = 128,
        pad_location = 'post',
        truncate_location = 'post'
    ):
        """
        Parameters
        ----------
        pad_character : int (default 0)
            The character to use for padding
        length : int (default 128)
            The length to pad sequences to
        pad_location : str (default 'post')
            One of either 'pre' or 'post', corresponding to how
            sequences are to be padded
        truncate_location : str (default 'post')
            One of either 'pre' or 'post', corresponding to how
            sequences are to be truncated
        """
        super().__init__()
        self.pad_character = pad_character
        self.length = length
        self.pad_location = pad_location
        self.truncate_location = truncate_location

    @property
    def pad_character(self):
        return self._pad_character
    @pad_character.setter
    def pad_character(self, value):
        if not isinstance(value, int):
            raise TypeError('pad_character must be int')
        self._pad_character = value
    
    @property
    def length(self):
        return self._length
    @length.setter
    def length(self, value):
        if not isinstance(value, int):
            raise TypeError('length must be int')
        if value <= 0 :
            raise ValueError('length must be greater than 0')
        self._length = value

    @property
    def pad_location(self):
        return self._pad_location
    @pad_location.setter
    def pad_location(self, value):
        if not isinstance(value, str):
            raise TypeError('pad_location must be str')
        if value not in _ALLOWED_PADS:
            raise ValueError(f'pad_location must be one of {_ALLOWED_PADS}')
        self._pad_location = value

    @property
    def truncate_location(self):
        return self._truncate_location
    @truncate_location.setter
    def truncate_location(self, value):
        if not isinstance(value, str):
            raise TypeError('truncate_location must be str')
        if value not in _ALLOWED_PADS:
            raise ValueError(f'truncate_location must be one of {_ALLOWED_PADS}')
        self._truncate_location = value
    
    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'PadSequences',
            'params' : {
                'padCharacter' : self.pad_character,
                'length' : self.length,
                'padLocation' : self.pad_location,
                'truncateLocation' : self.truncate_location
            }
        }
