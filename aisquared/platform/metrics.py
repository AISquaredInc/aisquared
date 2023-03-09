from .AISquaredAPIException import AISquaredAPIException
from .additional_utils import _check_results_length
from aisquared.base import ENDPOINTS
import pandas as pd
import requests


def _list_user_usage_metrics(
        url: str,
        headers: dict,
        user_id: str,
        period: str,
        as_df: bool
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    List the usage of the platform by a user

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    user_id : str
        The ID of the user
    period : int
        The period to group metrics into (e.g. 'hourly')
    as_df : bool
        Whether to return the data as a Pandas DataFrame
    """

    url = f'{url}/{ENDPOINTS["usage_metrics"]}?period={period}&entityId={user_id}&entity=user&action=run'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())

    if as_df:
        df = pd.DataFrame(resp.json()['data']['plotXYData'])
        _check_results_length(df)
        return df

    return resp.json()


def _list_model_usage_metrics(
        url,
        headers,
        model_id,
        period,
        as_df
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    List the usage of a model

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    model_id : str
        The ID of the user
    period : int
        The period to group metrics into (e.g. 'hourly')
    as_df : bool
        Whether to return the data as a Pandas DataFrame
    """

    url = f'{url}/{ENDPOINTS["usage_metrics"]}?period={period}&entity=model&entityId={model_id}&action=run'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

        if not resp.ok:
            raise AISquaredAPIException(resp.json())

        if as_df:
            df = pd.DataFrame(resp.json()['data']['plotXYData'])
            _check_results_length(df)
            return df

        return resp.json()
