import os
import json
import pytest
import aisquared
import tensorflow as tf


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


def test_sentimentanalysis(tmp_path):
    input_layer = tf.keras.layers.Input(128)
    x = tf.keras.layers.Embedding(100, 2)(input_layer)
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(100, activation='relu')(x)
    output_layer = tf.keras.layers.Dense(1, activation='relu')(x)

    model = tf.keras.models.Model(input_layer, output_layer)
    model.save(os.path.join(tmp_path, 'model.keras'))

    harvester = aisquared.config.harvesting.TextHarvester()
    preproc = aisquared.config.preprocessing.text.TextPreprocesser(
        [
            aisquared.config.preprocessing.text.Tokenize(),
            aisquared.config.preprocessing.text.ConvertToVocabulary(
                {
                    'this': 3,
                    'is': 4,
                    'a': 5,
                    'test': 6
                }
            ),
            aisquared.config.preprocessing.text.PadSequences()
        ]
    )
    analytic = aisquared.config.analytic.LocalModel(
        os.path.join(tmp_path, 'model.keras'), input_type='text')
    postproc = aisquared.config.postprocessing.Regression()
    rendering = aisquared.config.rendering.DocumentRendering()
    feedback = aisquared.config.feedback.RegressionFeedback()

    config = aisquared.config.ModelConfiguration(
        'sentiment-analysis',
        harvester,
        preproc,
        analytic,
        postproc,
        rendering,
        feedback_steps=feedback,
        url='https://dynamics.microsoft.com/'
    )
    config.compile(os.path.join(tmp_path, 'sentiment-analysis.air'))
    assert True


def test_imageclassification(tmp_path):
    input_layer = tf.keras.layers.Input((30, 30, 3))
    x = tf.keras.layers.Flatten()(input_layer)
    x = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    model = tf.keras.models.Model(input_layer, x)
    model.save(os.path.join(tmp_path, 'test_model.keras'))

    harvester = aisquared.config.harvesting.InputHarvester('image')
    preprocesser = aisquared.config.preprocessing.image.ImagePreprocesser(
        [
            aisquared.config.preprocessing.image.Resize([30, 30]),
            aisquared.config.preprocessing.image.DivideValue(255)
        ]
    )
    analytic = aisquared.config.analytic.LocalModel(
        os.path.join(tmp_path, 'test_model.keras'), 'cv')
    postprocesser = aisquared.config.postprocessing.BinaryClassification(
        [
            'zero',
            'one'
        ]
    )
    renderer = aisquared.config.rendering.DocumentRendering()
    config = aisquared.config.ModelConfiguration(
        'InputHarvestTest',
        harvester,
        preprocesser,
        analytic,
        postprocesser,
        renderer
    )
    config.compile(os.path.join(tmp_path, config.name))
