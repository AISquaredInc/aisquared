from aisquared.base import BaseObject


class SimpleFeedback(BaseObject):
    """
    Simple thumbs-up/thumbs-down feedback for predictions
    """

    def __init__(self):
        super().__init__()

    def to_dict(self):
        """
        Return the object as a dictionary
        """
        return {
            'className': 'SimpleFeedback',
            'params': dict()
        }
