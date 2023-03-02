from .AISquaredAPIException import AISquaredAPIException
from .additional_utils import _check_results_length
from aisquared.base import ENDPOINTS
import pandas as pd
import requests


def _list_model_users(
        url: str,
        headers: dict,
        model_id: str,
        as_df: bool
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    List users of a model

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

    url = f'{url}/{ENDPOINTS["model"]}/{model_id}/users'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())

    else:
        if as_df:
            df = pd.DataFrame(resp.json()['data'])
            _check_results_length(df)
            return df.sort_values(by='shared', ascending=False).reset_index(drop=True)

        return resp.json()


def _model_share_with_user(
        url: str,
        headers: dict,
        model_id: str,
        user_id: str,
        share: bool
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Share or unshare a model with a user

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    model_id : str
        The ID of the model
    user_id : str
        The ID for the user
    share : bool
        Whether to share (share = True) or unshare (share = False) a model with a user
    """

    url = f'{url}/{ENDPOINTS["model"]}/{model_id}/users/{user_id}'

    with requests.Session() as sess:
        if share:
            resp = sess.put(
                url,
                headers=headers
            )
        else:
            resp = sess.delete(
                url,
                headers=headers
            )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.ok


def _model_share_with_group(
        url: str,
        headers: dict,
        model_id: str,
        group_id: str,
        share: bool
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Share or unshare a model with a group

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    model_id : str
        The ID of the model
    group_id : str
        The ID for the user
    share : bool
        Whether to share (share = True) or unshare (share = False) a model with a group
    """

    url = f'{url}/{ENDPOINTS["model"]}/{model_id}/groups/{group_id}'

    with requests.Session() as sess:
        if share:
            resp = sess.put(
                url,
                headers=headers
            )
        else:
            resp = sess.delete(
                url,
                headers=headers
            )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.ok
