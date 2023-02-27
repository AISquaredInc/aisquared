endpoints = {
    'login': 'api/v1/auth/login',                     # For login
    'upload_model': 'upload/v1/models',               # For uploading model
    # For getting, deleting, sharing, or listing model users
    'model': 'api/v1/models',
    # For model and prediction feedback
    'feedback': 'api/v1/feedback',
    # For creating, updating, deleting, or getting a user
    'user': 'userservice/v1/user',
    # For creating, deleting, or updating groups
    'group': 'groupservice/v1/group',
    # For group user membership operations
    'group_membership': 'groupservice/v1/membership',
    'user_list': 'scim/v2/Users',                     # For listing users
    'group_list': 'scim/v2/Groups',                   # For listing groups
    'roles': 'groupservice/v1/role',                  # For listing roles
    'usage_metrics': 'api/v1/usage-metrics',          # For usage metrics
    'health': 'api/v1/health'                         # For health check
}
