import json

_allowed_placements = [
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

class ImagePrediction:

    def __init__(
        self,
        color = 'green',
        thickness = 5,
        placement = 'bottomleft'
    ):
        self.color = color
        self.thickness = thickness
        if placement not in _allowed_placements:
            raise ValueError(f'Placement must be one of {_allowed_placements}, got {placement}')
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
