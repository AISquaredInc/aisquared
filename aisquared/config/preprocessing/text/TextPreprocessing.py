from aisquared.base import BaseObject
from .Steps import Tokenize, RemoveCharacters, ConvertToCase, ConvertToVocabulary, PadSequences

ALLOWED_STEPS = (
    Tokenize,
    RemoveCharacters,
    ConvertToCase,
    ConvertToVocabulary,
    PadSequences
)

class TextPreprocessor(BaseObject):
    """
    Preprocessor object for natural language
    """
    def __init__(
            self,
            steps = None
    ):
        """
        Parameters
        ----------
        steps : list or None (default None)
            List of preprocessing steps for natural language
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
            'className' : 'TextPreprocessor',
            'steps' : self.step_dict
        }
