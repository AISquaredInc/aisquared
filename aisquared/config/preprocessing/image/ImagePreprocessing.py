from aisquared.base import BaseObject
from .Steps import AddValue, SubtractValue, MultiplyValue, DivideValue, ConvertToColor, Resize

ALLOWED_STEPS = (
    AddValue,
    SubtractValue,
    MultiplyValue,
    DivideValue,
    ConvertToColor,
    Resize
)


class ImagePreprocesser(BaseObject):
    """
    Preprocesser object for image data

    Example usage:

    >>> import aisquared
    >>> preprocesser = aisquared.config.preprocessing.image.ImagePreprocesser()
    >>> preprocesser.add_step(
        aisquared.config.preprocessing.image.AddValue(255.0)
    )
    """

    def __init__(
            self,
            steps: list = None
    ):
        """
        Parameters
        ----------
        steps : list
            List of preprocessing steps for image data
        """
        super().__init__()
        self.steps = None
        if steps is not None:
            for step in steps:
                self.add_step(step)

    @property
    def step_dict(self):
        if self.steps is None:
            return self.steps
        else:
            return [
                step.to_dict() for step in self.steps
            ]

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

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'ImagePreprocessor',
            'steps': self.step_dict
        }
