from .AISquaredAPIException import AISquaredAPIException
from .NoResultsFoundError import NoResultsFoundError
from .endpoints import endpoints
import pandas as pd
import requests

def _create_user(
        url,
        headers,
        user_name,
        given_name,
        family_name,
        email,
        role_id,
        active,
        middle_name,
        company_id,
        password
):
    json_data = {
        'active' : active,
        'userName' : user_name,
        'givenName' : given_name,
        'familyName' : family_name,
        'email' : email,
        'roleID' : role_id
    }

    if middle_name:
        json_data['middleName'] = middle_name
    if company_id:
        json_data['coompanyId'] = company_id
    if password:
        json_data['password'] = password

    url = f'{url}/{endpoints["user"]}'

    with requests.Session() as sess:
        resp = sess.post(
            url,
            json = json_data,
            headers = headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.json()

def _update_user(
        url,
        headers,
        user_id,
        user_name,
        given_name,
        family_name,
        email,
        role_id,
        active,
        middle_name,
        company_id,
        password
):
    json_data = {
        'active' : active,
        'userName' : user_name,
        'givenName' : given_name,
        'familyName' : family_name,
        'email' : email,
        'roleID' : role_id
    }

    if middle_name:
        json_data['middleName'] = middle_name
    if company_id:
        json_data['coompanyId'] = company_id
    if password:
        json_data['password'] = password

    url = f'{url}/{endpoints["user"]}/{user_id}'

    with requests.Session() as sess:
        resp = sess.put(
            url,
            headers = headers,
            json = json_data
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.ok

def _delete_user(
        url,
        headers,
        user_id
):
    url = f'{url}/{endpoints["user"]}/{user_id}'

    with requests.Session() as sess:
        resp = sess.delete(
            url,
            headers = headers
        )
    
    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.ok

def _get_user(
        url,
        headers,
        user_id
):
    url = f'{url}/{endpoints["user"]}/{user_id}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers = headers
        )
    
    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.json()

def _get_group(
        url,
        headers,
        group_id
):
    url = f'{url}/{endpoints["group"]}/{group_id}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers = headers
        )
    
    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.json()

def _create_group(
        url,
        headers,
        display_name,
        role_id
):
    url = f'{url}/{endpoints["group"]}'

    json_data = {
        'displayName' : display_name,
        'roleId' : role_id
    }

    with requests.Session() as sess:
        resp = sess.post(
            url,
            json = json_data,
            headers = headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.json()

def _delete_group(
        url,
        headers,
        group_id
):
    url = f'{url}/{endpoints["group"]}/{group_id}'

    with requests.Session() as sess:
        resp = sess.delete(
            url,
            headers = headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.ok

def _update_group(
        url,
        headers,
        group_id,
        display_name,
        role_id
):
    url = f'{url}/{endpoints["group"]}/{group_id}'

    json_data = {
        'displayName' : display_name,
        'roleId' : role_id
    }

    with requests.Session() as sess:
        resp = sess.put(
            url,
            json = json_data,
            headers = headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.ok

def _users_to_group(
        url,
        headers,
        group_id,
        user_ids,
        add
):
    url = f'{url}/{endpoints["group_memebership"]}'
    json_data = {
        'groupId' : group_id,
        'userIds' : user_ids
    }

    with requests.Session() as sess:
        if add:
            resp = sess.put(
                url,
                headers = headers,
                json = json_data
            )
        else:
            resp = sess.delete(
                url,
                headers = headers,
                json = json_data
            )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    return resp.ok

def _list_users(
        url,
        headers,
        max_count,
        as_df
):
    url = f'{url}/{endpoints["user_list"]}?count={max_count}&startIndex=1'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers = headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    
    if as_df:
        df = pd.json_normalize(resp.json()['Resources'])
        columns = ['id', 'userName', 'emails', 'active', 'groups', 'name.givenName', 'name.middleName', 'name.familyName']
        return df[columns]
    return resp.json()

def _list_groups(
        url,
        headers,
        max_count,
        as_df
):
    url = f'{url}/{endpoints["group_list"]}?count={max_count}&startIndex=1'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers = headers
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
        return pd.DataFrame({'id': ids, 'name': names, 'members': members})
    
    return resp.json()

def _list_group_users(
        url,
        headers,
        as_df,
        group_id
):
    url = f'{url}/{endpoints["group_list"]}/{group_id}'
    
    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers = headers
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

        return pd.DataFrame({'id': ids, 'displayName': names})
    return resp.json()

def _list_roles(
        url,
        headers,
        as_df
):
    
    url = f'{url}/{endpoints["roles"]}'

    with requests.Session() as sess:
        resp = sess.get(
            url,
            headers = headers
        )

    if not resp.ok:
        raise AISquaredAPIException(resp.json())
    
    if as_df:
        return pd.DataFrame(resp.json()['content'])
    return resp.json()['content']
