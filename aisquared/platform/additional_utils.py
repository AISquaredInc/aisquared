from .AISquaredAPIException import AISquaredAPIException
from .NoResultsFoundError import NoResultsFoundError
from aisquared.base import ENDPOINTS
import requests


def _test_connection(
        url
):
    url = f'{url}/{ENDPOINTS["health"]}'

    with requests.Session() as sess:
        resp = sess.get(
            url
        )

    if resp.ok:
        return resp.ok
    else:
        raise AISquaredAPIException(
            f'Connection could not be established. Status code {resp.status_code}')


def _check_results_length(
        df
):
    if df.shape[0] == 0:
        return NoResultsFoundError('No results found.')
