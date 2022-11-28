try:
    from mlflow.tensorflow import load_model as load_tensorflow_model
    from mlflow.sklearn import load_model as load_sklearn_model
    from mlflow.pytorch import load_model as load_pytorch_model
    from mlflow.keras import load_model as load_keras_model
except ImportError:
    pass

try:
    from flask import Flask, request, Response
except ImportError:
    pass

import tensorflow as tf
import numpy as np

try:
    import waitress
except ImportError:
    pass

try:
    import torch
except ImportError:
    pass

from importlib import import_module
import json
import os

_ALLOWED_TYPES = [
    'tensorflow',
    'sklearn',
    'pytorch',
    'keras',
    'mann'
]


def load_mann_model(model, custom_objects):
    """
    Load a MANN model with custom objects
    """
    return tf.keras.models.load_model(
        model,
        custom_objects=custom_objects
    )


def deploy_model(
        saved_model,
        model_type,
        host='127.0.0.1',
        port=2244,
        custom_objects=None,
        additional_functions_file=None
):
    """
    Deploy a model to a Flask server on the specified host

    Parameters
    ----------
    saved_model : Path-like
        The path to the saved model directory or model file
    model_type : str
        The type of model
    host : str (default '127.0.0.1')
        The host to deploy to
    port : int (default 2244)
        The port to deploy to
    custom_objects : dict or None (default None)
        Any custom objects to load when using a MANN model
    additional_functions_file : file-like or None (default None)
        File name containing additional functions (which have to be named `preprocess` and `postprocess`, if created)
        that are used during the prediction process
    """
    if model_type not in _ALLOWED_TYPES:
        raise ValueError(
            f'model_type must be one of {_ALLOWED_TYPES}, got {model_type}')

    if model_type == 'tensorflow':
        model = load_tensorflow_model(saved_model)
    elif model_type == 'sklearn':
        model = load_sklearn_model(saved_model)
    elif model_type == 'pytorch':
        model = load_pytorch_model(saved_model)
    elif model_type == 'keras':
        model = load_keras_model(saved_model)
    elif model_type == 'mann':
        model = load_mann_model(saved_model, custom_objects)

    # Import preprocessing and postprocessing steps, if provided
    if additional_functions_file:
        file_name = os.path.splitext(
            os.path.basename(additional_functions_file))[0]
        dir_name = os.path.dirname(os.path.abspath(additional_functions_file))
        module = import_module(file_name, dir_name)

        try:
            preprocess = module.preprocess
        except AttributeError:
            preprocess = None

        try:
            postprocess = module.postprocess
        except AttributeError:
            postprocess = None

    # Create the Flask app
    app = Flask(__name__)

    # Create the predict function
    @app.route('/predict', methods=['POST'])
    def predict():

        # try to get the data
        try:
            data = request.get_json()
            to_predict = data['data']
            if preprocess:
                to_predict = preprocess(to_predict)
        except Exception:
            return Response(
                'Data appears to be incorrectly formatted',
                400
            )

        # try to get the data correctly formatted for prediction
        try:
            if model_type == 'mann':
                to_predict = [
                    np.asarray(d) for d in to_predict
                ]
            elif model_type in ['tensorflow', 'keras', 'pytorch', 'sklearn']:
                to_predict = np.asarray(to_predict)
        except Exception:
            return Response(
                'Data passed could not be correctly converted to numpy array for prediction',
                400
            )

        # try to return the actual predictions
        try:
            if model_type != 'pytorch':
                predictions = np.asarray(model.predict(to_predict)).tolist()
            elif model_type == 'pytorch':
                predictions = model(torch.Tensor(to_predict)
                                    ).detach().numpy().tolist()

            if postprocess:
                try:
                    predictions = postprocess(predictions)
                except Exception as e:
                    print(e)
            return json.dumps({
                'predictions': predictions
            })

        except Exception:
            return Response(
                'Error in performing prediction',
                400
            )

    # run the app
    print('App created successfully. Serving and awaiting requests.')
    waitress.serve(
        app,
        host=host,
        port=port
    )
