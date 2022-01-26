import json
from .ImageRendering import ImageRendering, _allowed_placements

class ObjectRendering(ImageRendering):
    
    def __init__(
        self,
        color = 'green',
        thickness = 5,
        placement = 'bottomleft'
    ):
        super(ImageRendering, self).__init__()
        self.color = color
        self.thickness = thickness
        if placement not in _allowed_placements:
            raise ValueError(f'Placement must be one of {_allowed_placements}, got {placement}')
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