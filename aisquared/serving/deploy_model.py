from mlflow.tensorflow import load_model as load_tensorflow_model
from mlflow.sklearn import load_model as load_sklearn_model
from mlflow.pytorch import load_model as load_pytorch_model
from mlflow.keras import load_model as load_keras_model
from flask import Flask, request
import tensorflow as tf
import numpy as np
import waitress
import json


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
        custom_objects = custom_objects
    )

def deploy_model(
        saved_model,
        model_type,
        host = '127.0.0.1',
        port = 2244,
        custom_objects = None
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
    """
    if model_type not in _ALLOWED_TYPES:
        raise ValueError(f'model_type must be one of {_ALLOWED_TYPES}, got {model_type}')
    
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

    # Create the Flask app
    app = Flask(__name__)

    # Create the predict function
    @app.route('/predict', methods = ['POST'])
    def predict():
        data = request.get_json()
        to_predict = data['data']
        if model_type == 'mann':
            to_predict = [
                np.asarray(d) for d in to_predict
            ]
        elif model_type in ['tensorflow', 'keras', 'pytorch', 'sklearn']:
            to_predict = np.asarray(to_predict)
        return json.dumps({
            'predictions' : np.asarray(model.predict(to_predict)).tolist()
        })

    # run the app
    waitress.serve(
        app,
        host = host,
        port = port
    )