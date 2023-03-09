"""
The aisquared.serving package contains utilities to serve models to a local REST endpoint.

Here is an example of how to serve a simple keras model using these utilities:

>>> # Assume model is already trained and stored in memory as model
>>> from aisquared import serving
>>> serving.save_keras_model(model, 'my_model')
>>> serving.deploy_model(
    'my_model',
    'keras',
    additional_functions_file = '<optional file containing `preprocess` and `postprocess` functions, if applicable>'
)
App created successfullly. Serving and awaiting requests

And to retrieve predictions from the model:

>>> # From a separate terminal, assume data is already loaded
>>> from aisquared import serving
>>> serving.get_remote_predictions(data) # Do not need to change host or port if predicting from the same machine
*predictions*
"""

try:
    from mlflow.tensorflow import save_model as save_tensorflow_model
    from mlflow.sklearn import save_model as save_sklearn_model
    from mlflow.pytorch import save_model as save_pytorch_model
    from mlflow.keras import save_model as save_keras_model
except ImportError:
    pass

from .deploy_model import deploy_model, load_beyondml_model, load_keras_model, load_pytorch_model, load_sklearn_model, load_tensorflow_model
from .get_remote_prediction import get_remote_prediction
