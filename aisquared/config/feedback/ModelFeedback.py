from aisquared.base import BaseObject

ALLOWED_TYPES = ['singleChoice', 'multiChoice', 'text']
CHOICE_TYPES = ALLOWED_TYPES[:2]


def _create_question_dict(question, answer_type, choices):
    if answer_type in CHOICE_TYPES:
        return {
            'question': question,
            'answerType': answer_type,
            'choices': choices
        }

    # Since already checked for CHOICE_TYPES, must be 'text'
    elif answer_type in ALLOWED_TYPES:
        return {
            'question': question,
            'answerType': answer_type
        }
    else:
        raise ValueError(f'answer_type must be one of {ALLOWED_TYPES}')


class ModelFeedback(BaseObject):
    """
    Feedback object for questions and answers for an individual model.
    """

    def __init__(self):
        super().__init__()
        self.questions = []

    def add_question(
        self,
        question,
        answer_type='singleChoice',
        choices=[]
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

    def to_dict(self):
        """
        Return the object as a dictionary
        """
        return {
            'className': 'ModelFeedback',
            'params': {
                'questions': self.questions
            }
        }
