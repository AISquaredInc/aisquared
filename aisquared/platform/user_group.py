from .AISquaredAPIException import AISquaredAPIException
from .additional_utils import _check_results_length
from aisquared.base import ENDPOINTS
import pandas as pd
import requests


def _create_user(
        url: str,
        headers: dict,
        user_name: str,
        given_name: str,
        family_name: str,
        email: str,
        role_id: str,
        active: bool,
        middle_name: str,
        company_id: str,
        password: str
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Create a user within the platform

    Parameters
    ----------
    user_name : str
        The display name of the user
    given_name : str
        The user's first name
    family_name : str
        The user's last name
    email : str
        The user's email
    role_id : str
        The ID of the role to be given to the user
    active : bool
        Whether the user is active
    middle_name : str or None
        The user's middle name
    company_id : str or None
        The user's company ID
    password : str or None
        The user's password
    """

    json_data = {
        'active': active,
        'userName': user_name,
        'givenName': given_name,
        'familyName': family_name,
        'email': email,
        'roleId': role_id
    }

    if middle_name:
        json_data['middleName'] = middle_name
    if company_id:
        json_data['coompanyId'] = company_id
    if password:
        json_data['password'] = password

    url = f'{url}/{ENDPOINTS["user"]}'

    with requests.Session() as sess:
        resp = sess.post(
            url,
            json=json_data,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.json()


def _update_user(
        url: str,
        headers: dict,
        user_id: str,
        user_name: str,
        given_name: str,
        family_name: str,
        email: str,
        role_id: str,
        active: bool,
        middle_name: str,
        company_id: str,
        password: str
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Update a user within the platform

    Parameters
    ----------
    user_name : str
        The display name of the user
    given_name : str
        The user's first name
    family_name : str
        The user's last name
    email : str
        The user's email
    role_id : str
        The ID of the role to be given to the user
    active : bool
        Whether the user is active
    middle_name : str or None
        The user's middle name
    company_id : str or None
        The user's company ID
    password : str or None
        The user's password
    """

    json_data = {
        'active': active,
        'userName': user_name,
        'givenName': given_name,
        'familyName': family_name,
        'email': email,
        'roleId': role_id
    }

    if middle_name:
        json_data['middleName'] = middle_name
    if company_id:
        json_data['coompanyId'] = company_id
    if password:
        json_data['password'] = password

    url = f'{url}/{ENDPOINTS["user"]}/{user_id}'

    with requests.Session() as sess:
        resp = sess.put(
            url,
            headers=headers,
            json=json_data
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.ok


def _delete_user(
        url: str,
        headers: dict,
        user_id: str
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Delete a user from the platform

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    user_id : string
        The id of the user you want to interact with
    """

    url = f'{url}/{ENDPOINTS["user"]}/{user_id}'

    with requests.Session() as sess:
        resp = sess.delete(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.ok


def _get_user(
        url: str,
        headers: dict,
        user_id: str
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Get information about a user from the platform

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    user_id : string
        The id of the user you want to interact with
    """

    url = f'{url}/{ENDPOINTS["user"]}/{user_id}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.json()


def _get_group(
        url=str,
        headers=dict,
        group_id=str
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Get information about a group from the platform

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    group_id : string
        The id of the group you want to interact with
    """

    url = f'{url}/{ENDPOINTS["group"]}/{group_id}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.json()


def _create_group(
        url: str,
        headers: dict,
        display_name: str,
        role_id: str
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Create a group within the platform

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    display_name : string
        The display name of the group
    group_id : string
        The role id for the group
    """

    url = f'{url}/{ENDPOINTS["group"]}'

    json_data = {
        'displayName': display_name,
        'roleId': role_id
    }

    with requests.Session() as sess:
        resp = sess.post(
            url,
            json=json_data,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.json()


def _delete_group(
        url: str,
        headers: dict,
        group_id: str
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Delete a group within the platform

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    group_id : string
        The id of the group
    """

    url = f'{url}/{ENDPOINTS["group"]}/{group_id}'

    with requests.Session() as sess:
        resp = sess.delete(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.ok


def _update_group(
        url: str,
        headers: dict,
        group_id: str,
        display_name: str,
        role_id: str
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Update a group within the platform

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    display_name : string
        The display name of the group
    role_id : string
        The role id for the group
    """

    url = f'{url}/{ENDPOINTS["group"]}/{group_id}'

    json_data = {
        'displayName': display_name,
        'roleId': role_id
    }

    with requests.Session() as sess:
        resp = sess.put(
            url,
            json=json_data,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.ok


def _users_to_group(
        url: str,
        headers: dict,
        group_id: str,
        user_ids: list,
        add: bool
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    Add or remove users to / from a group

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    group_id : str
        The group to add the users to
    user_ids : list of str
        The IDs of the users to add
    add : bool
        Whether to add a user to a group (add = True) or remove a user from a group (add = False)
    """

    url = f'{url}/{ENDPOINTS["group_membership"]}'
    json_data = {
        'groupId': group_id,
        'userIds': user_ids
    }

    with requests.Session() as sess:
        if add:
            resp = sess.put(
                url,
                headers=headers,
                json=json_data
            )
        else:
            resp = sess.delete(
                url,
                headers=headers,
                json=json_data
            )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.ok


def _list_users(
        url: str,
        headers: dict,
        max_count: int,
        as_df: bool
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    List all users

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    max_count : int
        The maximum number of users to return
    as_df : bool
        Whether to return the data as a Pandas DataFrame
    """

    url = f'{url}/{ENDPOINTS["user_list"]}?count={max_count}&startIndex=1'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())

    if as_df:
        df = pd.json_normalize(resp.json()['Resources'])
        _check_results_length(df)
        columns = ['id', 'userName', 'emails', 'active', 'groups',
                   'name.givenName', 'name.middleName', 'name.familyName']
        df = df[columns]

        # This is a change that should be fixed on the database side

        df['displayName'] = df['name.givenName'].astype(
            str) + ' ' + df['name.familyName']
        return df
    return resp.json()


def _list_groups(
        url: str,
        headers: dict,
        max_count: int,
        as_df: bool
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    List all groups

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    max_count : int
        The maximum number of users to return
    as_df : bool
        Whether to return the data as a Pandas DataFrame
    """

    url = f'{url}/{ENDPOINTS["group_list"]}?count={max_count}&startIndex=1'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())

    if as_df:
        resp = resp.json()
        ids = [i['id'] for i in resp['Resources']]
        names = [i['displayName'] for i in resp['Resources']]
        members = []

        members = [[(u['value'], u['display'])
                    for u in i['members'] if i != []] for i in resp['Resources']]
        df = pd.DataFrame({'id': ids, 'name': names, 'members': members})
        _check_results_length(df)
        return df

    return resp.json()


def _list_group_users(
    url: str,
    headers: dict,
    as_df: bool,
    group_id: str
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    List all users in a group

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    max_count : int
        The maximum number of users to return
    as_df : bool
        Whether to return the data as a Pandas DataFrame
    """

    url = f'{url}/{ENDPOINTS["group_list"]}/{group_id}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())

    if as_df:
        resp = resp.json()
        ids = []
        names = []
        for d in resp['members']:
            ids.append(d['value'])
            names.append(d['display'])

        df = pd.DataFrame({'id': ids, 'username': names})
        _check_results_length(df)
        return df

    return resp.json()


def _list_roles(
        url: str,
        headers: dict,
        as_df: bool
):
    """
    NOT MEANT TO BE CALLED BY THE END USER

    List roles

    Parameters
    ----------
    url : string
        The base url to format
    headers : dict
        The headers used for authentication within the AI Squared platform
    as_df : bool
        Whether to return the data as a Pandas DataFrame
    """

    url = f'{url}/{ENDPOINTS["roles"]}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers=headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())

    if as_df:
        df = pd.DataFrame(resp.json()['content'])
        _check_results_length(df)
        return df
    return resp.json()['content']
