"""NOT MEANT TO BE CALLED BY THE END USER - configuration parameters for the different endpoints in the platform"""

ENDPOINTS = {
    'login': 'api/v1/auth/login',
    'upload_model': 'upload/v1/models',
    'model': 'api/v1/models',
    'feedback': 'api/v1/feedback',
    'user': 'userservice/v1/user',
    'group': 'groupservice/v1/group',
    'group_membership': 'groupservice/v1/membership',
    'user_list': 'scim/v2/Users',
    'group_list': 'scim/v2/Groups',
    'roles': 'groupservice/v1/role',
    'usage_metrics': 'api/v1/usage-metrics',
    'health': 'api/v1/health'
}
