from typing import Union
from aisquared.base import LOCATIONS, BaseObject


class ImageRendering(BaseObject):
    """
    Object which dictates how to render images

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.rendering.ImageRendering()
    >>> my_obj.to_dict()
    {'className': 'ImageRendering',
    'params': {'color': 'blue',
    'thickness': '5',
    'placement': 'bottomleft',
    'includeProbability': False,
    'badgeColor': 'white',
    'fontColor': 'black',
    'fontSize': '5',
    'classes': None,
    'thresholdKey': None,
    'thresholdValue': None}}

    """

    def __init__(
        self,
        color: str = 'blue',
        thickness: str = '5',
        placement: str = LOCATIONS[-1],
        include_probability: bool = False,
        badge_color: str = 'white',
        font_color: str = 'black',
        font_size: str = '5',
        classes: list = None,
        threshold_key: str = None,
        threshold_value: Union[int, float] = None
    ):
        """
        Parameters
        ----------
        color : str (default 'blue')
            The color of the box around images
        thickness : str (default '5')
            The thickness of the box around images
        placement : str (default 'bottomleft')
            The placement of the predicted value in the box
            around images
        include_probability : bool (default False)
            Whether to render calculated probabilities
        badge_color : str (default 'white')
            Background color of the text region
        font_color : str (default 'black')
            Color of the text
        font_size : str (default '5')
            Text size
        classes : None or list (default None)
            If provided, list of classes that will be rendered
        threshold_key : None or str (default None)
            If provided, the key to use for thresholding
        threshold_value : None or numeric (default None)
            If provided with threshold_key, the value to use to threshold rendering
        """
        super().__init__()
        self.color = color
        self.thickness = thickness
        self.placement = placement
        self.include_probability = include_probability
        self.badge_color = badge_color
        self.font_color = font_color
        self.font_size = font_size
        self.classes = classes
        self.threshold_key = threshold_key
        self.threshold_value = threshold_value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = value

    @property
    def placement(self):
        return self._placement

    @placement.setter
    def placement(self, value):
        if value not in LOCATIONS:
            raise ValueError(f'placement must be one of {LOCATIONS}')
        self._placement = value

    @property
    def include_probability(self):
        return self._include_probability

    @include_probability.setter
    def include_probability(self, value):
        self._include_probability = value

    @property
    def badge_color(self):
        return self._badge_color

    @badge_color.setter
    def badge_color(self, value):
        self._badge_color = value

    @property
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, value):
        self._font_color = value

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self._font_size = value

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

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'ImageRendering',
            'params': {
                'color': self.color,
                'thickness': self.thickness,
                'placement': self.placement,
                'includeProbability': self.include_probability,
                'badgeColor': self.badge_color,
                'fontColor': self.font_color,
                'fontSize': self.font_size,
                'classes': self.classes,
                'thresholdKey': self.threshold_key,
                'thresholdValue': self.threshold_value
            }
        }
