import json
from .ImagePrediction import ImagePrediction

class ObjectDetection(ImagePrediction):
    
    def __init__(
        self,
        color = 'green',
        thickness = 5,
        placement = 'bottomleft'
    ):
        super(ImagePrediction, self).__init__(
            color,
            thickness,
            placement
        )

    def to_dict(self):
        return {
            'className' : 'ObjectDetection',
            'params' : {
                'color' : self.color,
                'thickness' : self.thickness,
                'placement' : self.placement
            }
        }
