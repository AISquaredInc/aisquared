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
        print(confusion_matrix(orig_preds, mimic_preds.argmax(axis=1)))
        print(classification_report(orig_preds, mimic_preds.argmax(axis=1)))
    else:
        print(mean_squared_error(orig_preds, mimic_preds, squared=False))
        print(f'Standard deviation: {np.std(mimic_preds - orig_preds)}')
    print('\n')

    print('Relative to Original:')
    if problem_type == 'classification':
        print(confusion_matrix(true_data, mimic_preds.argmax(axis=1)))
        print(classification_report(true_data, mimic_preds.argmax(axis=1)))
    else:
        print(mean_squared_error(true_data, mimic_preds, squared=False))
        print(f'Standard deviation: {np.std(true_data - orig_preds)}')


def mimic_model(
    trained_model,
    nnet,
    training_data,
    test_data,
    test_labels,
    problem_type,
    loss,
    metrics,
    optimizer,
    retention=0.9,
    batch_size=32,
    epochs=100,
    starting_sparsification=0,
    max_sparsification=99,
    sparsification_rate=5
):

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
        training_predictions = trained_model.predict(training_data)
        testing_predictions = trained_model.predict(test_data)
    else:
        raise TypeError(
            'trained_model is not a scikit-learn TransformerMixin, ClassifierMixin, or RegressorMixin')

    if problem_type == 'classification':
        cutoff = retention
    else:
        cutoff = mean_squared_error(
            test_labels, testing_predictions, squared=False) * retention

    # Add layer masks
    nnet = beyondml.tflow.utils.add_layer_masks(nnet)
    nnet.compile(
        loss=loss,
        optimizer=optimizer,
        metrics=metrics
    )

    # Create the ActiveSparsification callback
    callback = beyondml.tflow.utils.ActiveSparsification(
        cutoff,
        starting_sparsification=starting_sparsification,
        max_sparsification=max_sparsification,
        sparsification_rate=sparsification_rate
    )

    nnet.fit(
        training_data,
        training_predictions,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[callback]
    )

    nnet = beyondml.tflow.utils.remove_layer_masks(nnet)
    nnet_preds = nnet.predict(test_data)
    _print_report(test_labels, testing_predictions, nnet_preds, problem_type)
    return nnet
