import pytest
import aisquared


def test_binary_feedback():
    with pytest.raises(TypeError):
        aisquared.config.feedback.BinaryFeedback()
    with pytest.raises(ValueError):
        aisquared.config.feedback.BinaryFeedback(['foo', 'bar', 'baz'])

    feedback = aisquared.config.feedback.BinaryFeedback(
        ['foo', 'bar']
    )
    assert feedback.to_dict() == {
        'className': 'BinaryFeedback',
        'params': {
            'labelMap': ['foo', 'bar']
        }
    }


def test_multiclass_feedback():
    feedback = aisquared.config.feedback.MulticlassFeedback(
        ['foo', 'bar', 'baz']
    )
    assert feedback.to_dict() == {
        'className': 'MulticlassFeedback',
        'params': {
            'labelMap': ['foo', 'bar', 'baz']
        }
    }


def test_regression_feedback():
    feedback = aisquared.config.feedback.RegressionFeedback()
    assert feedback.to_dict() == {
        'className': 'RegressionFeedback',
        'params': dict()
    }


def test_simple_feedback():
    feedback = aisquared.config.feedback.SimpleFeedback()
    assert feedback.to_dict() == {
        'className': 'SimpleFeedback',
        'params': dict()
    }


def test_qualitative_feedback():
    feedback = aisquared.config.feedback.QualitativeFeedback()

    with pytest.raises(ValueError):
        feedback.add_question(
            'test',
            'test'
        )
        feedback.add_question(
            'test',
            'singleChoice'
        )

    feedback.add_question(
        'test',
        'singleChoice',
        ['foo', 'bar', 'baz']
    )

    feedback.add_question(
        'test',
        'multiChoice',
        ['foo', 'bar', 'baz']
    )

    feedback.add_question(
        'test',
        'text'
    )

    assert feedback.to_dict() == {
        'className': 'QualitativeFeedback',
        'params': {
            'questions': [
                {
                    'question': 'test',
                    'answerType': 'singleChoice',
                    'choices': ['foo', 'bar', 'baz']
                },
                {
                    'question': 'test',
                    'answerType': 'multiChoice',
                    'choices': ['foo', 'bar', 'baz']
                },
                {
                    'question': 'test',
                    'answerType': 'text'
                }
            ]
        }
    }


def test_model_feedback():
    feedback = aisquared.config.feedback.ModelFeedback()

    with pytest.raises(ValueError):
        feedback.add_question(
            'test',
            'test'
        )
        feedback.add_question(
            'test',
            'singleChoice'
        )

    feedback.add_question(
        'test',
        'singleChoice',
        ['foo', 'bar', 'baz']
    )

    feedback.add_question(
        'test',
        'multiChoice',
        ['foo', 'bar', 'baz']
    )

    feedback.add_question(
        'test',
        'text'
    )

    assert feedback.to_dict() == {
        'className': 'ModelFeedback',
        'params': {
            'questions': [
                {
                    'question': 'test',
                    'answerType': 'singleChoice',
                    'choices': ['foo', 'bar', 'baz']
                },
                {
                    'question': 'test',
                    'answerType': 'multiChoice',
                    'choices': ['foo', 'bar', 'baz']
                },
                {
                    'question': 'test',
                    'answerType': 'text'
                }
            ]
        }
    }
