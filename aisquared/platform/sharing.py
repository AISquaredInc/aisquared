from .AISquaredAPIException import AISquaredAPIException
from .endpoints import ENDPOINTS
import pandas as pd
import requests


def _list_model_users(
        url,
        headers,
        model_id,
        as_df
):

    url = f'{url}/{ENDPOINTS["model"]}/{model_id}/users'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

    if resp.status_code != 200:
        raise AISquaredAPIException(resp.json())

    else:
        if as_df:
            return pd.DataFrame(resp.json()['data']).sort_values(by='shared', ascending=False).reset_index(drop=True)
        return resp.json()


def _model_share_with_user(
        url,
        headers,
        model_id,
        user_id,
        share
):

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

    if resp.status_code != 200:
        raise AISquaredAPIException(resp.json())
    return resp.ok


def _model_share_with_group(
        url,
        headers,
        model_id,
        group_id,
        share
):

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
