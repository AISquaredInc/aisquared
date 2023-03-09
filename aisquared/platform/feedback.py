from .AISquaredAPIException import AISquaredAPIException
from .additional_utils import _check_results_length
from .NoResultsFoundError import NoResultsFoundError
from aisquared.base import ENDPOINTS
import pandas as pd
import requests


def _list_model_feedback(
        url: str,
        headers: dict,
        model_id: str,
        limit: int,
        as_df: bool
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    List feedback from a model

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    model_id : str
        The ID of the model
    limit : int
        The maximum number of feedback items to return
    as_df : bool
        Whether to return the data as a Pandas DataFrame
    """

    url = f'{url}/{ENDPOINTS["feedback"]}/models?modelId={model_id}&page=1&pageSize={limit}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

    if not resp.ok:
        if resp.status_code == 404:
            raise NoResultsFoundError('No Results Found')
        raise AISquaredAPIException(resp.json())

    if as_df:
        df = pd.DataFrame(resp.json()['data']['modelFeedback'])
        _check_results_length(df)
        return df
    return resp.json()['data']


def _list_prediction_feedback(
        url: str,
        headers: dict,
        prediction_id: str,
        as_df: bool
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    List prediction feedback for a prediction ID

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    prediction_id : str
        The prediction ID
    as_df : bool
        Whether to return the data as a Pandas DataFrame
    """

    url = f'{url}/{ENDPOINTS["feedback"]}/predictions?modelId={prediction_id}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())

    if as_df:
        df = pd.DataFrame(resp.json()['data'])
        _check_results_length(df)
        return df
    return resp.json()['data']


def _list_model_prediction_feedback(
        url: int,
        headers: dict,
        model_id: str,
        as_df: bool
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    List prediction feedback from a model

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    model_id : str
        The ID of the model
    as_df : bool
        Whether to return the data as a Pandas DataFrame
    """

    url = f'{url}/{ENDPOINTS["feedback"]}/predictions?modelId={model_id}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())

    if as_df:
        data = resp.json()['data']
        df = pd.concat([pd.json_normalize(v)
                       for v in data.values()]).reset_index(drop=True)
        _check_results_length(df)
        return df

    return resp.json()
