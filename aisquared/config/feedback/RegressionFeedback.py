from aisquared.base import BaseObject


class RegressionFeedback(BaseObject):
    """
    Feedback for regression
    """

    def __init__(self):
        super().__init__()

    def to_dict(self):
        """
        Return the object as a dictionary
        """
        return {
            'className': 'RegressionFeedback',
            'params': dict()
        }
