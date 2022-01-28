import json
from .ImageRendering import ImageRendering, ALLOWED_PLACEMENTS
from .WordRendering import ALLOWED_COLORS

class ObjectRendering(ImageRendering):
    """
    Object which dictates how to render object detection in images
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
            The color to place as a box around objects
        thickness : int (default 5)
            The thickness, in pixels, of boxes around objects
        placement : str (default {ALLOWED_PLACEMENTS[0]})
            The placement of the text indicating the object detected
        """
        super(ImageRendering, self).__init__()
        self.color = color
        self.thickness = thickness
        if placement not in ALLOWED_PLACEMENTS:
            raise ValueError(f'Placement must be one of {ALLOWED_PLACEMENTS}, got {placement}')
        self.placement = placement

    def to_dict(self):
        """Return the object as a dictionary"""
        return {
            'className' : 'ObjectDetection',
            'params' : {
                'color' : self.color,
                'thickness' : self.thickness,
                'placement' : self.placement
            }
        }
