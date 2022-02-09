from .Steps import ZScore, MinMax, OneHot, DropColumn
from aisquared.base import BaseObject

ALLOWED_STEPS = (
    ZScore,
    MinMax,
    OneHot,
    DropColumn
)

class TabularPreprocessor(BaseObject):
    """
    Preprocessor object for tabular data
    """
    def __init__(
            self,
            steps = None
    ):
        """
        Parameters
        ----------
        steps : list or None (default None)
            List of preprocessor steps for tabular data
        """
        super().__init__()
        self.steps = None
        if steps is not None:
            for step in steps:
                self.add_step(step)

    def add_step(self, step):
        """
        Add a step to the preprocessor object
        """
        if not isinstance(step, ALLOWED_STEPS):
            raise TypeError(f'Each step must be one of {ALLOWED_STEPS}')
        if self.steps is None:
            self.steps = [step]
        else:
            self.steps = self.steps + [step]

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'TabularPreprocessor',
            'steps' : [
                step.to_dict() for step in self.steps
            ]
        }
