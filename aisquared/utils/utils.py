from typing import Union
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin, TransformerMixin
from sklearn.metrics import classification_report, confusion_matrix, mean_squared_error
import tensorflow as tf
import numpy as np
import beyondml


def _print_report(true_data, orig_preds, mimic_preds, problem_type):
    print('ORIGINAL PERFORMANCE:')
    if problem_type == 'classification':
        print(confusion_matrix(true_data, orig_preds))
        print(classification_report(true_data, orig_preds))
    else:
        print(mean_squared_error(true_data, orig_preds, squared=False))
    print('\n\n')

    print('MIMIC PERFORMANCE:')
    print('\n')
    print('Relative to First Model:')
    if problem_type == 'classification':
        if mimic_preds.shape[1] == 1:
            print(confusion_matrix(orig_preds, (mimic_preds >= 0.5).astype(int)))
            print(classification_report(orig_preds,
                  (mimic_preds >= 0.5).astype(int)))
        else:
            print(confusion_matrix(orig_preds, mimic_preds.argmax(axis=1)))
            print(classification_report(orig_preds, mimic_preds.argmax(axis=1)))
    else:
        print(mean_squared_error(orig_preds, mimic_preds, squared=False))
        print(f'Standard deviation: {np.std(mimic_preds - orig_preds)}')
    print('\n')

    print('Relative to Original:')
    if problem_type == 'classification':
        if mimic_preds.shape[1] == 1:
            print(confusion_matrix(true_data, (mimic_preds >= 0.5).astype(int)))
            print(classification_report(
                true_data, (mimic_preds >= 0.5).astype(int)))
        else:
            print(confusion_matrix(true_data, mimic_preds.argmax(axis=1)))
            print(classification_report(true_data, mimic_preds.argmax(axis=1)))
    else:
        print(mean_squared_error(true_data, mimic_preds, squared=False))
        print(f'Standard deviation: {np.std(true_data - orig_preds)}')


def _get_cv_model(size, input_shape, num_outputs, output_activation):
    if size == 'small':
        num_blocks = 2
        num_hidden = 1
        hidden_size = 64
    elif size == 'medium':
        num_blocks = 4
        num_hidden = 2
        hidden_size = 128
    elif size == 'large':
        num_blocks = 6
        num_hidden = 4
        hidden_size = 256
    else:
        raise ValueError(
            f'size must be one of "small", "medium", "large", got {size}')

    input_layer = tf.keras.layers.Input(input_shape)
    x = tf.keras.layers.Conv2D(
        8, 3, padding='same', activation='relu')(input_layer)
    x = tf.keras.layers.Conv2D(8, 3, padding='same', activation='relu')(x)
    x = tf.keras.layers.MaxPool2D(strides=1)(x)

    for block_num in range(num_blocks - 1):
        x = tf.keras.layers.Conv2D(
            8 * (2 ** (block_num + 1)), 3, padding='same', activation='relu')(x)
        x = tf.keras.layers.Conv2D(
            8 * (2 ** (block_num + 1)), 3, padding='same', activation='relu')(x)
        x = tf.keras.layers.MaxPool2D(strides=1)(x)

    x = tf.keras.layers.Flatten()(x)
    for _ in range(num_hidden):
        x = tf.keras.layers.Dense(hidden_size, activation='relu')(x)

    output_layer = tf.keras.layers.Dense(
        num_outputs, activation=output_activation)(x)

    return tf.keras.models.Model(input_layer, output_layer)


def _get_embedding_model(size, vocab_size, input_shape, num_outputs, output_activation):

    if vocab_size is None:
        raise ValueError(
            'If NLP embedding model specified, must also specify vocab_size')

    if size == 'small':
        embedding_dim = 4
        num_hidden = 4
        hidden_size = 64
    elif size == 'medium':
        embedding_dim = 8
        num_hidden = 6
        hidden_size = 128
    elif size == 'large':
        embedding_dim = 16
        num_hidden = 8
        hidden_size = 256
    else:
        raise ValueError(
            f'size must be one of "small", "medium", "large", got {size}')

    input_layer = tf.keras.layers.Input(input_shape)
    x = tf.keras.layers.Embedding(vocab_size, embedding_dim)(input_layer)
    x = tf.keras.layers.Flatten()(x)
    for _ in range(num_hidden):
        x = tf.keras.layers.Dense(hidden_size, activation='relu')(x)
    output_layer = tf.keras.layers.Dense(
        num_outputs, activation=output_activation)(x)

    return tf.keras.models.Model(input_layer, output_layer)


def _get_fc_model(size, input_shape, num_outputs, output_activation):
    if size == 'small':
        num_hidden = 4
        hidden_size = 64
    elif size == 'medium':
        num_hidden = 6
        hidden_size = 128
    elif size == 'large':
        num_hidden = 8
        hidden_size = 256
    else:
        raise ValueError(
            f'size must be one of "small", "medium", "large", got {size}')

    input_layer = tf.keras.layers.Input(input_shape)
    for i in range(num_hidden):
        if i == 0:
            x = tf.keras.layers.Dense(
                hidden_size, activation='relu')(input_layer)
        else:
            x = tf.keras.layers.Dense(hidden_size, activation='relu')(x)
    output_layer = tf.keras.layers.Dense(
        num_outputs, activation=output_activation)(x)

    return tf.keras.models.Model(input_layer, output_layer)


def mimic_model(
    trained_model: BaseEstimator,
    nnet: tf.keras.models.Model,
    training_data: np.ndarray,
    test_data: np.ndarray,
    test_labels: np.ndarray,
    problem_type: str,
    loss: str,
    metrics: Union[str, list],
    optimizer: str,
    mimic_proba: bool = False,
    retention: float = 0.9,
    batch_size: int = 32,
    epochs: int = 100,
    starting_sparsification: int = 0,
    max_sparsification: int = 99,
    sparsification_rate: int = 5
) -> tf.keras.models.Model:
    """
    Train a sparse neural network to mimic a scikit-learn model

    Parameters
    ----------
    trained_model : sklearn model
        The model that is already trained
    nnet : TensorFlow keras Model
        The neural network to train to mimic the trained model
    training_data : array or array-like
        The input data that was used to train the trained model
    test_data : array or array-like
        The input data to be used for testing
    test_labels : array or array-like
        The output data used in testing
    problem_type : str
        The type of problem, either 'classification' or 'regression'
    loss : str or keras loss function
        The loss to use
    metrics : str, function or list of str, function
        Metrics to measure
    optimizer : str or keras optimizer
        The optimizer to use
    mimic_proba : bool (default False)
        For classification, mimic the probability outputs
    retention : float (default 0.9)
        The retention of performance to allow further pruning
    batch_size : int (default 32)
        The batch size to use while training
    epochs : int (default 100)
        The number of epochs (if early stopping is not met beforehand)
    starting_sparsification : int (default 0)
        The starting model sparsification
    max_sparsification : int (default 99)
        The maximum sparsification to allow
    sparsification_rate : int (default 5)
        The sparsification rate when invoked

    Returns
    -------
    nnet : TensorFlow keras Model
        The trained model
    """

    # Check problem type
    if problem_type not in ['classification', 'regression']:
        raise ValueError(
            'problem_type must be "classification" or "regression"')

    # Check that the model to mimic is a sklearn model
    if not isinstance(trained_model, BaseEstimator):
        raise TypeError(
            'Currently can only convert trained scikit-learn models')

    # Get the predictions
    if isinstance(trained_model, TransformerMixin):
        training_predictions = trained_model.transform(training_data)
        testing_predictions = trained_model.transform(test_data)
    elif isinstance(trained_model, (ClassifierMixin, RegressorMixin)):
        if isinstance(trained_model, ClassifierMixin) and mimic_proba:
            training_predictions = trained_model.predict_proba(training_data)
            testing_predictions = trained_model.predict(test_data)
        else:
            training_predictions = trained_model.predict(training_data)
            testing_predictions = trained_model.predict(test_data)
    else:
        raise TypeError(
            'trained_model is not a scikit-learn TransformerMixin, ClassifierMixin, or RegressorMixin')

    if problem_type == 'classification':
        cutoff = retention
    else:
        cutoff = mean_squared_error(
            test_labels, testing_predictions, squared=False) / retention

    # Add layer masks
    nnet = beyondml.tflow.utils.add_layer_masks(nnet)
    nnet = beyondml.tflow.utils.train_model(
        nnet,
        training_data,
        training_predictions,
        loss,
        metrics,
        optimizer,
        cutoff,
        batch_size,
        epochs,
        starting_sparsification,
        max_sparsification,
        sparsification_rate
    )

    nnet = beyondml.tflow.utils.remove_layer_masks(nnet)
    nnet_preds = nnet.predict(test_data)
    _print_report(test_labels, testing_predictions, nnet_preds, problem_type)
    return nnet


def get_model(
    model_type: str,
    input_shape: Union[int, tuple],
    num_outputs: int,
    output_activation: str,
    size: str = 'small',
    vocab_size: Union[None, int] = None
):
    """
    Get a pre-configured model for different use cases

    Parameters
    ----------
    model_type : str
        Either 'cv', 'nlp_embedding', or 'fc', defining the model type
    input_shape : int or tuple of int
        The input shape to the model
    num_outputs : int
        The output shape of the model
    output_activation : str or keras activation function
        The activation of the final layer of the model
    size : str (default 'small')
        One of either 'small', 'medium', or 'large'
    vocab_size : str or None (default None)
        Size of the vocab, if model_type is 'nlp_embedding'

    Returns
    -------
    model : TensorFlow Keras model
        The model
    """
    if model_type == 'cv':
        return _get_cv_model(size, input_shape, num_outputs, output_activation)
    elif model_type == 'nlp_embedding':
        return _get_embedding_model(size, vocab_size, input_shape, num_outputs, output_activation)
    elif model_type == 'fc':
        return _get_fc_model(size, input_shape, num_outputs, output_activation)
    else:
        raise ValueError(
            f'model_type must be one of "cv", "nlp_embedding", or "fc", got {model_type}')
