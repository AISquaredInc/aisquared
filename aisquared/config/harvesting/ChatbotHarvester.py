from aisquared.base import BaseObject


class ChatbotHarvester(BaseObject):
    """
    Object to harvest for a chatbot

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.harvesting.ChatbotHarvester(
        max_length = 128
    )
    >>> my_obj.to_dict()
    {'className': 'ChatbotHarvester',
    'params': {'maxLength': '128',
    'inputType': 'text'}}

    """

    def __init__(
            self,
            max_length: int = None
    ):
        """
        Parameters
        ----------
        max_length : int or None (default None)
            The maximum length of text allowed
        """
        super().__init__()
        self.max_length = max_length
        self.input_type = 'text'

    @property
    def max_length(self):
        return self._max_length

    @max_length.setter
    def max_length(self, value):
        if value is not None:
            if not isinstance(value, int):
                raise TypeError('max_length must be int')
        self._max_length = str(value) if isinstance(value, int) else value

    def to_dict(self):
        return {
            'className': 'ChatbotHarvester',
            'params': {
                'maxLength': self.max_length,
                'inputType': self.input_type
            }
        }
