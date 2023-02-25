from .AISquaredAPIException import AISquaredAPIException
from .NoResultsFoundError import NoResultsFoundError
from .endpoints import endpoints
import pandas as pd
import requests

def _list_model_feedback(
        url,
        headers,
        model_id,
        limit,
        as_df
):
    
    url = f'{url}/{endpoints["feedback"]}/models?modelId={model_id}&page=1&pageSize={limit}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers = headers
        )

    if not resp.ok:
        if resp.status_code == 404:
            raise NoResultsFoundError('No Results Found')
        raise AISquaredAPIException(resp.json())
    
    if as_df:
        return pd.DataFrame(resp.json()['data']['modelFeedback'])
    return resp.json()['data']

def _list_prediction_feedback(
        url,
        headers,
        prediction_id,
        as_df
):
    
    url = f'{url}/{endpoints["feedback"]}/predictions?modelId={prediction_id}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers = headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    
    if as_df:
        return pd.DataFrame(resp.json()['data'])
    return resp.json()['data']

def _list_model_prediction_feedback(
        url,
        headers,
        model_id,
        as_df
):
    
    url = f'{url}/{endpoints["feedback"]}/predictions?modelId={model_id}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers = headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    
    if as_df:
        data = resp.json()['data']
        return pd.concat([pd.json_normalize(v) for v in data.values()]).reset_index(drop=True)
    
    return resp.json()
