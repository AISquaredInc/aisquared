from aisquared.config import ModelConfiguration
import tensorflowjs as tfjs
import tensorflow as tf
import zipfile
import shutil
import json
import os

def create_air_model(config, model, filename = 'model.air'):
    """Create an air model from a configuration object and a model
    
    Parameters
    ----------
    config : ModelConfiguration object, dict, or str
        The configuration for the model
    model : TensorFlow Keras model
        The model to be converted to air format
    filename : pathlike object (default 'model.air')
        The name of the file to output

    Raises
    ------
    TypeError
        - Raises TypeError if any parameters are not of expected types
    ValueError
        - Raises ValueError if file or directory with same basename as passed filename exists
    """
    # Get the config as a JSON string
    if isinstance(config, ModelConfiguration):
        config = config.to_json()
    elif isinstance(config, dict):
        config = json.dumps(config)
    elif isinstance(config, str):
        config = json.dumps(json.loads(config))
    else:
        raise TypeError(f'Unsupported config type {type(config)}')

    # Check dtype as Keras model
    if not isinstance(model, tf.keras.models.Model):
        raise TypeError('model must be TensorFlow Keras model')

    # Create the directory that will be zipped together
    dirname = os.path.splitext(filename)[0]
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    else:
        raise ValueError('Files may already exist that would be overwritten by this operation. Consider using a different file name or moving existing files')
    
    # Convert the model and put it in the directory
    tfjs.converters.save_keras_model(
        model,
        dirname
    )

    # Put the config in the directory as well
    with open(os.path.join(dirname, 'config.json'), 'w') as f:
        json.dump(json.loads(config), f)

    # Write the zipfile
    with zipfile.ZipFile(filename, 'w') as myzip:
        for f in os.listdir(dirname):
            myzip.write(os.path.join(dirname, f))

    # Delete directory and contents
    shutil.rmtree(dirname, ignore_errors = True)
