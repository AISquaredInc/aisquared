from .AISquaredAPIException import AISquaredAPIException
from .NoResultsFoundError import NoResultsFoundError
from .endpoints import endpoints
import pandas as pd
import requests

def _test_connection(
        url
):
    url = f'{url}/{endpoints["health"]}'

    with requests.Session() as sess:
        resp = sess.get(
            url
        )

    if resp.ok:
        return resp.ok
    else:
        raise AISquaredAPIException(f'Connection could not be established. Status code {resp.status_code}')
