from .Steps import ZScore, MinMax, OneHot, DropColumn
from aisquared.base import BaseObject

ALLOWED_STEPS = (
    ZScore,
    MinMax,
    OneHot,
    DropColumn
)


class TabularPreprocesser(BaseObject):
    """
    Preprocesser object for tabular data

    Example usage:

    Example usage:

    >>> import aisquared
    >>> preprocesser = aisquared.config.preprocessing.tabular.TabularPreprocesser()
    >>> preprocesser.add_step(
        aisquared.config.preprocessing.tabular.ZScore(
            [0, 1, 2],
            [0.2, 0.4, 0.6]
        )
    )
    """

    def __init__(
            self,
            steps: list = None
    ):
        """
        Parameters
        ----------
        steps : list or None (default None)
            List of preprocesser steps for tabular data
        """
        super().__init__()
        self.steps = None
        if steps is not None:
            for step in steps:
                self.add_step(step)

    def add_step(self, step):
        """
        Add a step to the preprocesser object
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
            'className': 'TabularPreprocessor',
            'steps': [
                step.to_dict() for step in self.steps
            ]
        }
