import json
from .WordRendering import ALLOWED_COLORS

ALLOWED_PLACEMENTS = [
    'top',
    'bottom',
    'left',
    'right',
    'topleft',
    'topright',
    'bottomleft',
    'topright',
    None
]

class ImageRendering:

    def __init__(
        self,
        color = ALLOWED_COLORS[0],
        thickness = 5,
        placement = ALLOWED_PLACEMENTS[0]
    ):
        self.color = color
        self.thickness = thickness
        if placement not in ALLOWED_PLACEMENTS:
            raise ValueError(f'Placement must be one of {ALLOWED_PLACEMENTS}, got {placement}')
        self.placement = placement

    def to_dict(self):
        return {
            'className' : 'ImagePrediction',
            'params' : {
                'color' : self.color,
                'thickness' : self.thickness,
                'placement' : self.placement
            }
        }

    def to_json(self):
        return json.dumps(self.to_dict())
