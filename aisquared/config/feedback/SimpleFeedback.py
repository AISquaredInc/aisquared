from aisquared.base import BaseObject


class SimpleFeedback(BaseObject):
    """
    Simple thumbs-up/thumbs-down feedback for predictions

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.feedback.SimpleFeedback()
    >>> my_obj.to_dict()
    {'className': 'SimpleFeedback', 'params': {}}
    """

    def __init__(self):
        super().__init__()

    def to_dict(self) -> dict:
        """
        Return the object as a dictionary
        """
        return {
            'className': 'SimpleFeedback',
            'params': dict()
        }
