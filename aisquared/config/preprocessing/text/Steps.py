from aisquared.base import BaseObject

_ALLOWED_PADS = [
    'pre',
    'post'
]


class Tokenize(BaseObject):
    """Preprocessing Step to tokenize text"""

    def __init__(
        self,
        split_sentences=False,
        split_words=True,
        token_pattern='\b\w\w+\b'
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
            'className': 'Tokenize',
            'params': {
                'splitSentences': self.split_sentences,
                'splitWords': self.split_words,
                'tokenPattern': self.token_pattern
            }
        }


class RemoveCharacters(BaseObject):
    """Preprocessing step to remove characters from text"""

    def __init__(
        self,
        remove_digits=True,
        remove_punctuation=True
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
            'className': 'RemoveCharacters',
            'params': {
                'removeDigits': self.remove_digits,
                'removePunctuation': self.remove_punctuation
            }
        }


class ConvertToCase(BaseObject):
    """Text preprocessing object to convert inputs to all lowercase or all uppercase"""

    def __init__(
        self,
        lowercase=True
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
            'className': 'ConvertToCase',
            'params': {
                'lowercase': self.lowercase
            }
        }


class ConvertToVocabulary(BaseObject):
    """Text preprocessing object to convert tokens to integer vocabularies"""

    def __init__(
        self,
        vocabulary,
        start_character=1,
        oov_character=2,
        max_vocab=None
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
            'className': 'ConvertToVocabulary',
            'params': {
                'vocabulary': self.vocabulary,
                'startCharacter': self.start_character,
                'oovCharacter': self.oov_character,
                'maxVocab': self.max_vocab
            }
        }


class PadSequences(BaseObject):
    """Text preprocessing object to pad sequences"""

    def __init__(
        self,
        pad_character=0,
        length=128,
        pad_location='post',
        truncate_location='post'
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
        if value <= 0:
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
            raise ValueError(
                f'truncate_location must be one of {_ALLOWED_PADS}')
        self._truncate_location = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'PadSequences',
            'params': {
                'padCharacter': self.pad_character,
                'length': self.length,
                'padLocation': self.pad_location,
                'truncateLocation': self.truncate_location
            }
        }


class Trim(BaseObject):
    """Text preprocessing class to trim whitespace from text"""

    def __init__(self):
        super().__init__()

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'Trim',
            'params': {}
        }
