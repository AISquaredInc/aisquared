from .ModelFeedback import _create_question_dict
from aisquared.base import BaseObject


class QualitativeFeedback(BaseObject):
    """
    Feedback object for questions and answers for individual predictions.

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.feedback.QualitativeFeedback()
    >>> my_obj.add_question('Any additional feedback?', 'text')
    >>> my_obj.to_dict()
    {'className': 'QualitativeFeedback',
    'params': {'questions': [{'question': 'Any additional feedback?',
    'answerType': 'text'}]}}

    """

    def __init__(self):
        super().__init__()
        self.questions = []

    def add_question(
        self,
        question: str,
        answer_type: str = 'singleChoice',
        choices: list = []
    ):
        """
        Add a question to be asked.

        Parameters
        ----------
        question : str
            The question to be asked.
        answer_type : str (default 'singleChoice')
            One of either 'singleChoice', 'multiChoice', or 'text'
        choices : list (default [])
            The choices to be provided, if `answer_type` is 'singleChoice' or 'multiChoice'
        """
        if answer_type in ['singleChoice', 'multiChoice'] and choices == []:
            raise ValueError(
                'If singleChoice or multiChoice is indicated, choices must be provided')

        if answer_type not in ['singleChoice', 'multiChoice', 'text']:
            raise ValueError(
                'answer_type must be one of "singleChoice", "multiChoice", or "text"')

        self.questions.append(_create_question_dict(
            question, answer_type, choices))

    def to_dict(self) -> dict:
        """
        Return the object as a dictionary
        """
        return {
            'className': 'QualitativeFeedback',
            'params': {
                'questions': self.questions
            }
        }
