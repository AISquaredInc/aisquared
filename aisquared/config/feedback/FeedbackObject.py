from aisquared.base import BaseObject
from warnings import warn


class FeedbackObject(BaseObject):
    def __init__(self):
        super().__init__()
        warn('Warning! All FeedbackObjects are currently deprecated after version 0.3.13. Instead, feedback parameters should be added to the `ModelConfiguration` object directly')
