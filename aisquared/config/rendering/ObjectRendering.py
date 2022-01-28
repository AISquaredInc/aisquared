from aisquared.base import ALLOWED_LOCATIONS, ALLOWED_COLORS, BaseObject

class ObjectRendering(BaseObject):
    """
    Object which dictates how to render object detection in images
    """

    def __init__(
        self,
        color = ALLOWED_COLORS[-1],
        thickness = '5px',
        placement = ALLOWED_LOCATIONS[-1],
        include_probability = False,
        badge_color = ALLOWED_COLORS[-2],
        font_color = ALLOWED_COLORS[-4],
        font_size = '5px'
    ):
        super().__init__()
        self.color = color
        self.thickness = thickness
        if placement not in ALLOWED_LOCATIONS:
            raise ValueError(f'Placement must be one of {ALLOWED_LOCATIONS}, got {placement}')
        self.placement = placement
        self.include_probability = include_probability
        self.badge_color = badge_color
        self.font_color = font_color
        self.font_size = font_size

    def to_dict(self):
        """Return the object as a dictionary"""
        return {
            'className' : 'ObjectDetection',
            'params' : {
                'color' : self.color,
                'thickness' : self.thickness,
                'placement' : self.placement,
                'includeProbability' : self.include_probability,
                'badgeColor' : self.badge_color,
                'fontColor' : self.font_color,
                'fontSize' : self.font_size
            }
        }
