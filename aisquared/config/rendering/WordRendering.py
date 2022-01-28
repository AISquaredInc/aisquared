from aisquared.base import ALLOWED_COLORS, ALLOWED_BADGES, BaseObject

class WordRendering(BaseObject):
    
    def __init__(
        self,
        content_key = None,
        badge_shape = ALLOWED_BADGES[-1],
        badge_color = ALLOWED_COLORS[-1]
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
