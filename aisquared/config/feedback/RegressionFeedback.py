from aisquared.base import BaseObject


class RegressionFeedback(BaseObject):
    """
    Feedback for regression

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.feedback.RegressionFeedback()
    >>> my_obj.to_dict()
    {'className': 'RegressionFeedback', 'params': {}}

    """

    def __init__(self):
        super().__init__()

    def to_dict(self) -> dict:
        """
        Return the object as a dictionary
        """
        return {
            'className': 'RegressionFeedback',
            'params': dict()
        }
