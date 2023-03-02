from .AISquaredAPIException import AISquaredAPIException
from .additional_utils import _check_results_length
from aisquared.base import ENDPOINTS
import pandas as pd
import requests
import json


def _list_models(
        url: str,
        headers: dict,
        as_df: bool
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Format a URL based on parameters for whether the user is interacting with the ALB or not

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    as_df : bool
        Whether to return the response as a dataframe object
    """

    url = f'{url}/{ENDPOINTS["model"]}?userOnly=true'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )
    if not resp.ok:
        raise AISquaredAPIException(json.dumps(resp.json()))

    else:
        if as_df:
            df = pd.DataFrame(resp.json()['data']['models'])
            _check_results_length(df)
            df['name'] = df.config.apply(lambda c: c['params']['name'])
            new_cols = ['name', 'id']
            new_cols += [c for c in df.columns if c not in new_cols]

            return df[new_cols]

        return resp.json()['data']['models']


def _upload_model(
        url: str,
        headers: dict,
        model_file: str
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Upload a model to the platform

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    model_file : path or path-like
        Whether to return the response as a dataframe object
    """

    url = f'{url}/{ENDPOINTS["upload_model"]}'

    with open(model_file, 'rb') as f:

        with requests.Session() as sess:
            resp = sess.post(
                url,
                headers=headers,
                files={'model': f}
            )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())

    return resp.json()['data']['id']


def _get_model(
        url: str,
        headers: dict,
        model_id: str
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Upload a model to the platform

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    model_id : string
        The id of the model you want to interact with
    """

    url = f'{url}/{ENDPOINTS["model"]}/{model_id}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())

    return resp.json()['data']


def _delete_model(
        url: str,
        headers: dict,
        model_id: str
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Upload a model to the platform

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    model_id : string
        The id of the model you want to interact with
    """

    url = f'{url}/{ENDPOINTS["model"]}/{model_id}'

    with requests.Session() as sess:
        resp = sess.delete(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())

    return resp.ok
