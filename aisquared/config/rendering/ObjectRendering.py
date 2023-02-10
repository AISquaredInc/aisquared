from aisquared.base import LOCATIONS, COLORS, BaseObject


class ObjectRendering(BaseObject):
    """
    Object which dictates how to render object detection in images

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.rendering.ObjectRendering()
    >>> my_obj.to_dict()
    {'className': 'ObjectRendering',
    'params': {'color': 'blue',
    'thickness': '5',
    'placement': 'bottomleft',
    'includeProbability': False,
    'badgeColor': 'white',
    'fontColor': 'black',
    'fontSize': '5'}}

    """

    def __init__(
        self,
        color: str = COLORS[-1],
        thickness: str = '5',
        placement: str = LOCATIONS[-1],
        include_probability: bool = False,
        badge_color: str = COLORS[-2],
        font_color: str = COLORS[-4],
        font_size: str = '5'
    ):
        """
        Parameters
        ----------
        color : str (default 'blue')
            The color of the box around images
        thickness : str (default '5')
            The thickness of the box around images
        placement : str (default 'bottomleft')
            The placement of the prediction text
        include_probability : bool (default False)
            Whether to render calculated probabilities
        badge_color : str (default 'white')
            Background color for the text region
        font_color : str (default 'black')
            Color of the text
        font_size : str (default '5')
            Text size
        """
        super().__init__()
        self.color = color
        self.thickness = thickness
        self.placement = placement
        self.include_probability = include_probability
        self.badge_color = badge_color
        self.font_color = font_color
        self.font_size = font_size

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if value not in COLORS:
            raise ValueError(f'color must be one of {COLORS}')
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
        if value not in COLORS:
            raise ValueError(f'badge_color must be one of {COLORS}')
        self._badge_color = value

    @property
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, value):
        if value not in COLORS:
            raise ValueError(f'font_color must be one of {COLORS}')
        self._font_color = value

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self._font_size = value

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'ObjectRendering',
            'params': {
                'color': self.color,
                'thickness': self.thickness,
                'placement': self.placement,
                'includeProbability': self.include_probability,
                'badgeColor': self.badge_color,
                'fontColor': self.font_color,
                'fontSize': self.font_size
            }
        }
