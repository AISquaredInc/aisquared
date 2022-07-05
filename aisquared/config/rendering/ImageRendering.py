from aisquared.base import LOCATIONS, BaseObject


class ImageRendering(BaseObject):
    """
    Object which dictates how to render images
    """

    def __init__(
        self,
        color='blue',
        thickness='5px',
        placement=LOCATIONS[-1],
        include_probability=False,
        badge_color='white',
        font_color='black',
        font_size='5px',
        classes=None,
        confidence_threshold=None,
        regression_threshold=None
    ):
        """
        Parameters
        ----------
        color : str (default 'blue')
            The color of the box around images
        thickness : str (default '5px')
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
        font_size : str (default '5px')
            Text size
        classes : None or list (default None)
            If provided, list of classes that will be rendered
        confidence_threshold : None or float (default None)
            The threshold for rendering, if provided
        regression_threshold : None or dict (default None)
            Information for regression rendering, with 'filter' and 'value' keys
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
        self.confidence_threshold = confidence_threshold
        self.regression_threshold = regression_threshold

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
    def confidence_threshold(self):
        return self._confidence_threshold

    @confidence_threshold.setter
    def confidence_threshold(self, value):
        self._confidence_threshold = value

    @property
    def regression_threshold(self):
        return self._regression_threshold

    @regression_threshold.setter
    def regression_threshold(self, value):
        self._regression_threshold = value

    def to_dict(self):
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
                'confidenceThreshold': self.confidence_threshold,
                'regressionThreshold': self.regression_threshold
            }
        }
