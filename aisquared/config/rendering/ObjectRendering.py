import json
from .ImageRendering import ImageRendering, ALLOWED_PLACEMENTS
from .WordRendering import ALLOWED_COLORS

class ObjectRendering(ImageRendering):
    
    def __init__(
        self,
        color = ALLOWED_COLORS[0],
        thickness = 5,
        placement = 'bottomleft'
    ):
        super(ImageRendering, self).__init__()
        self.color = color
        self.thickness = thickness
        if placement not in ALLOWED_PLACEMENTS:
            raise ValueError(f'Placement must be one of {ALLOWED_PLACEMENTS}, got {placement}')
        self.placement = placement

    def to_dict(self):
        return {
            'className' : 'ObjectDetection',
            'params' : {
                'color' : self.color,
                'thickness' : self.thickness,
                'placement' : self.placement
            }
        }
