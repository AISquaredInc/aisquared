import json

class LanguagePreprocessor:
    """
    Preprocessor object for natural language
    """
    def __init__(
            self,
            vocabulary,
            padding_character = 0,
            start_character = 1,
            oov_character = 2,
            padding = 'post',
            max_len = 128
    ):
        """
        Parameters
        ----------
        vocabulary : dict
            Dictionary of string to int mappings for vocabulary
        padding_character : int (default 0)
            Character to indicate padding
        start_character : int (default 1)
            Character for the start of sequences
        oov_character : int (default 2)
            Character to indicate out of vocabulary words
        padding : str (default 'post')
            Whether padding should occur at the beginning or the end of sequences
        max_len : int (default 128)
            Maximum length of sequences
        """

        self.vocabulary = vocabulary
        self.padding_character = padding_character
        self.start_character = start_character
        self.oov_character = oov_character
        self.padding = padding
        self.max_len = max_len

    def to_dict(self):
        """
        Get the preprocessor object as a dictionary
        """
        return {
            'languagePreprocessor': {
                'vocabulary' : self.vocabulary,
                'paddingCharacter' : self.vocabulary,
                'startCharacter' : self.start_character,
                'oovCharacter' : self.oov_character,
                'padding' : self.padding,
                'maxLen' : self.max_len
            }
        }

    def to_json(self):
        """
        Get the preprocessor object as a JSON string
        """
        return json.dumps(self.to_dict())
