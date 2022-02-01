from aisquared.base import COLORS, BADGES, BaseObject

class WordRendering(BaseObject):
    """
    Object for rendering badges on individual words
    """

    def __init__(
        self,
        content_key = None,
        badge_shape = BADGES[-1],
        badge_color = COLORS[-1]
    ):
        f"""
        Parameters
        ----------
        content_key : str or None (default None)
            The key from the results to use in rendering
        badge_shape : str (default {BADGES[-1]})
            The badge shape to use
        badge_color : str (default {COLORS[-1]})
            The badge color to use
        """
        super().__init__()
        self.content_key = content_key
        self.badge_shape = badge_shape
        self.badge_color = badge_color

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
        if value not in COLORS:
            raise ValueError(f'badge_color must be one of {COLORS}')
        self._badge_color = value

    def to_dict(self):
        return {
            'className' : 'WordRendering',
            'params' : {
                'contentKey' : self.content_key,
                'badgeShape' : self.badge_shape,
                'badgeColor' : self.badge_color 
            }
        }
