import json
from .Steps import AddValue, SubtractValue, MultitplyValue, DivideValue, ConvertToColor, Resize

ALLOWED_STEPS = (
    AddValue,
    SubtractValue,
    MultitplyValue,
    DivideValue,
    ConvertToColor,
    Resize
)

class ImagePreprocessor:
    """
    Preprocessor object for image data
    """
    def __init__(
            self,
            steps = None
    ):
        """
        Parameters
        ----------
        steps : list
            List of preprocessing steps for image data
        """
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
        Get the preprocessor object as a dictionary
        """
        return {
            'className' : 'ImagePreprocessor',
            'steps' : [
                step.to_dict() for step in self.steps
            ]
        }

    def to_json(self):
        """
        Get the preprocessor object as a JSON string
        """
        return json.dumps(self.to_dict())
