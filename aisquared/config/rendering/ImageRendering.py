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
    """
    Object which dictates how to render images
    """

    def __init__(
        self,
        color = ALLOWED_COLORS[0],
        thickness = 5,
        placement = ALLOWED_PLACEMENTS[0]
    ):
        f"""
        Parameters
        ----------
        color : str (default {ALLOWED_COLORS[0]})
            The color for the box around the image to be
        thickness : int (default 5)
            The pixel thickness of the box around the image
        placement : str (default {ALLOWED_PLACEMENTS[0]})
            The placement of the prediction inside the box
        """
        self.color = color
        self.thickness = thickness
        if placement not in ALLOWED_PLACEMENTS:
            raise ValueError(f'Placement must be one of {ALLOWED_PLACEMENTS}, got {placement}')
        self.placement = placement

    def to_dict(self):
        """Return the object as a dictionary"""
        return {
            'className' : 'ImagePrediction',
            'params' : {
                'color' : self.color,
                'thickness' : self.thickness,
                'placement' : self.placement
            }
        }

    def to_json(self):
        """Return the object as a JSON string"""
        return json.dumps(self.to_dict())
