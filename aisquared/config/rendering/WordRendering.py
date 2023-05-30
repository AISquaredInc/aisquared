from typing import Union
from aisquared.base import BADGES, WORD_LISTS, BaseObject


class WordRendering(BaseObject):
    """
    Object for rendering badges on individual words

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.rendering.WordRendering()
    >>> my_obj.to_dict()
    {'className': 'WordRendering',
    'params': {'wordList': 'input',
    'resultKey': None,
    'contentKey': None,
    'badgeShape': 'star',
    'badgeColor': 'blue',
    'classes': None,
    'thresholdKey': None,
    'thresholdValue': None
    'position': 'after'}}

    """

    def __init__(
            self,
            word_list: str = WORD_LISTS[0],
            result_key: str = None,
            content_key: str = None,
            badge_shape: str = BADGES[-2],
            badge_color: str = 'blue',
            classes: list = None,
            threshold_key: str = None,
            threshold_value: Union[int, float] = None,
            position: str = 'after'
    ):
        """
        Parameters
        ----------
        word_list : str (default 'input')
            How to identify words to render, must be one of 'input', 'result'
        results_key : str or None (default None)
            The result key to use to render, only used if word_list is 'result'
        content_key : str or None (default None)
            The key from the results to use in rendering
        badge_shape : str (default 'star')
            The badge shape to use
        badge_color : str (default 'blue')
            The badge color to use
        classes : None or list (default None)
            If provided, list of classes that will be rendered
        threshold_key : None or string (default None)
            If provided, the key to look for to threshold
        theshold_value : None or numeric (default None)
            If provided with threshold_key, the minimum value required to render
        position : str (default 'after')
            The position of the rendering widget, either 'before' or 'after'
        """
        super().__init__()
        self.word_list = word_list
        self.result_key = result_key
        self.content_key = content_key
        self.badge_shape = badge_shape
        self.badge_color = badge_color
        self.classes = classes
        self.threshold_key = threshold_key
        self.threshold_value = threshold_value
        self.position = position

    @property
    def word_list(self):
        return self._word_list

    @word_list.setter
    def word_list(self, value):
        if value not in WORD_LISTS:
            raise ValueError(
                f'word_list must be one of {WORD_LISTS}, got {value}')
        self._word_list = value

    @property
    def result_key(self):
        return self._result_key

    @result_key.setter
    def result_key(self, value):
        self._result_key = value

    @property
    def content_key(self):
        return self._content_key

    @content_key.setter
    def content_key(self, value):
        self._content_key = value

    @property
    def badge_shape(self):
        return self._badge_shape

    @badge_shape.setter
    def badge_shape(self, value):
        if value not in BADGES:
            raise ValueError(f'badge_shape must be one of {BADGES}')
        self._badge_shape = value

    @property
    def badge_color(self):
        return self._badge_color

    @badge_color.setter
    def badge_color(self, value):
        self._badge_color = value

    @property
    def classes(self):
        return self._classes

    @classes.setter
    def classes(self, value):
        self._classes = value

    @property
    def threshold_key(self):
        return self._threshold_key

    @threshold_key.setter
    def threshold_key(self, value):
        self._threshold_key = value

    @property
    def threshold_value(self):
        return self._threshold_value

    @threshold_value.setter
    def threshold_value(self, value):
        self._threshold_value = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if not isinstance(value, str):
            raise TypeError('position must be string')
        if value not in ['before', 'after']:
            raise ValueError(
                f'position must be either "before" or "after", got {value}')
        self._position = value

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'WordRendering',
            'params': {
                'wordList': self.word_list,
                'resultKey': self.result_key,
                'contentKey': self.content_key,
                'badgeShape': self.badge_shape,
                'badgeColor': self.badge_color,
                'classes': self.classes,
                'thresholdKey': self.threshold_key,
                'thresholdValue': self.threshold_value,
                'position': self.position
            }
        }
