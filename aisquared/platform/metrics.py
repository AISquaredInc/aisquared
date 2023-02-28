from .AISquaredAPIException import AISquaredAPIException
from .additional_utils import _check_results_length
from aisquared.base import ENDPOINTS
import pandas as pd
import requests


def _list_user_usage_metrics(
        url,
        headers,
        user_id,
        period,
        as_df
):
    url = f'{url}/{ENDPOINTS["usage_metrics"]}?period={period}&entityId={user_id}&entity=user&action=run'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())

    if as_df:
        return pd.DataFrame(resp.json()['data']['plotXYData'])

    return resp.json()


def _list_model_usage_metrics(
        url,
        headers,
        model_id,
        period,
        as_df
):
    url = f'{url}/{ENDPOINTS["usage_metrics"]}?period={period}&entity=model&entityId={model_id}&action=run'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

        if not resp.ok:
            raise AISquaredAPIException(resp.json())

        if as_df:
            return pd.DataFrame(resp.json()['data']['plotXYData'])

        return resp.json()
