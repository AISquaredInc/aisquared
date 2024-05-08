import os
import json
import pytest
import aisquared


def test_graphconfig(tmp_path):
    regex = '\D(\d{5})\D'
    analytic = {
        '11111': {
            'name': 'John Doe',
            'nbo': 1
        },
        '22222': {
            'name': 'Jane Doe',
            'nbo': 1
        },
        '33333': {
            'name': 'Alice',
            'nbo': 3
        },
        '44444': {
            'name': 'Bob',
            'nbo': 8
        }
    }
    with open(os.path.join(tmp_path, 'analytic.json'), 'w') as f:
        json.dump(analytic, f)

    harvester = aisquared.config.harvesting.TextHarvester('regex', regex)
    preproc = None
    analytic = aisquared.config.analytic.LocalAnalytic(
        os.path.join(tmp_path, 'analytic.json'), input_type='text')
    postproc = None
    rendering = aisquared.config.rendering.WordRendering()
    model_feedback = aisquared.config.feedback.ModelFeedback()
    model_feedback.add_question(
        'Is this model helpful?', 'singleChoice', ['yes', 'no'])
    prediction_feedback = aisquared.config.feedback.SimpleFeedback()
    feedback = prediction_feedback

    config = aisquared.config.GraphConfiguration('TextAnalytic')
    harvester_id = config.add_node(harvester)
    analytic_id = config.add_node(analytic, harvester_id)
    render_id = config.add_node(rendering, analytic_id)
    model_feedback_id = config.add_node(model_feedback, render_id)
    prediction_feedback_id = config.add_node(prediction_feedback, render_id)

    config.compile(os.path.join(tmp_path, 'TextAnalytic.air'))
    assert True
