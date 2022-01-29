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
        super().__init__()
        self.content_key = content_key
        self.badge_shape = badge_shape
        self.badge_color = badge_color

    def to_dict(self):
        return {
            'className' : 'WordRendering',
            'params' : {
                'contentKey' : self.content_key,
                'badgeShape' : self.badge_shape,
                'badgeColor' : self.badge_color 
            }
        }
