from .AISquaredAPIException import AISquaredAPIException
from .endpoints import endpoints
import pandas as pd
import requests
import json

def _list_models(
        url,
        headers,
        as_df = True
):
    url = f'{url}/{endpoints["model"]}?userOnly=true'
    
    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers = headers
        )
    if resp.status_code != 200:
        raise AISquaredAPIException(json.dumps(resp.json()))
    
    else:
        if as_df:
            df = pd.DataFrame(resp.json()['data']['models'])
            df['name'] = df.config.apply(lambda c : c['params']['name'])
            new_cols = ['name', 'id']
            new_cols += [c for c in df.columns if c not in new_cols]
            return df[new_cols]
        
        return resp.json()['data']['models']

def _upload_model(
        url,
        headers,
        model_file
):
    url = f'{url}/{endpoints["upload_model"]}'

    with open(model_file, 'rb') as f:

        with requests.Session() as sess:
            resp = sess.post(
                url,
                headers = headers,
                files = {'model' : f}
        )
    
    if resp.status_code != 200:
        raise AISquaredAPIException(resp.json())
    
    return resp.json()['data']['id']

def _get_model(
        url,
        headers,
        model_id
):
    
    url = f'{url}/{endpoints["model"]}/{model_id}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers = headers
        )
    
    if resp.status_code != 200:
        raise AISquaredAPIException(resp.json())
    
    return resp.json()['data']

def _delete_model(
        url,
        headers,
        model_id
):
    
    url = f'{url}/{endpoints["model"]}/{model_id}'

    with requests.Session() as sess:
        resp = sess.delete(
            url,
            headers = headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())

    return resp.ok
