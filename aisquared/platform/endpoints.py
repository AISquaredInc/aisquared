endpoints = {
    'login': 'api/v1/auth/login',                     # For login
    'upload_model': 'upload/v1/models',               # For uploading model
    'model': 'api/v1/models',                         # For getting, deleting,
    # sharing, or listing
    # model users

    'feedback': 'api/v1/feedback',                    # For model and
    # prediction feedback
    'user': 'userservice/v1/user',                    # For creating, updating,
    # deleting, or
    # getting a user
    'group': 'groupservice/v1/group',                 # For creating, deleting,
    # or updating groups

    'group_membership': 'groupservice/v1/membership',  # For group user
    # membership operations
    'user_list': 'scim/v2/Users',                     # For listing users
    'group_list': 'scim/v2/Groups',                   # For listing groups
    'roles': 'groupservice/v1/role',                  # For listing roles
    'usage_metrics': 'api/v1/usage-metrics',          # For usage metrics
    'health': 'api/v1/health'                         # For health check
}
