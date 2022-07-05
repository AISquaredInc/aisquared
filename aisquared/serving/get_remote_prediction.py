import numpy as np
import requests
import json


def get_remote_prediction(
    data,
    host='127.0.0.1',
    port=2244
):
    """
    Send data to use for prediction

    Parameters
    ----------
    data : dict, str, np.ndarray, or list
        The data to be predicted on
    host : str (default '127.0.0.1')
        The host to use
    port : int (default '2244')
        The port to use

    Notes
    -----
    - If data is a dictionary, it is expected to already be
      correctly formatted
    - If data is a string, it is expected to already be
      correctly formatted

    Returns
    -------
    predictions : list
        The predictions from the deployed model
    """
    # Setup the url and headers
    url = f'http://{host}:{port}/predict'
    headers = {
        'Content-Type': 'application/json'
    }

    # Format the data
    if isinstance(data, dict):
        data = json.dumps(data)
    elif isinstance(data, str):
        data = data
    elif isinstance(data, np.ndarray):
        data = json.dumps(
            {
                'data': data.tolist()
            }
        )
    elif isinstance(data, list):
        data = json.dumps(
            {
                'data': data
            }
        )

    # Make the request
    with requests.session() as sess:
        resp = sess.post(
            url,
            data=data,
            headers=headers
        )

    if resp.status_code != 200:
        return resp
    else:
        return resp.json()['predictions']
