from aisquared.base import BaseObject


class ReverseMLWorkflow(BaseObject):
    """
    Creation of a ReverseML Workflow to interact with remote data sources
    """

    def __init__(
        self,
        label: str,
        connector_type: str,
        connector_action: str = 'read',
        input_type: str = 'text',
        filter_type: str = 'input',
        file_names: list = [],
        bucket: str = '',
        filter_by_columns: list = [],
        all: bool = False,
        arn: str = '',
        host: str = '',
        path: str = '',
        port: str = '',
        role: str = '',
        soql: str = '',
        query: str = '',
        token: str = '',
        column: str = '',
        db_name: str = '',
        db_user: str = '',
        period: int = None,
        schema: str = '',
        secret: str = '',
        account: str = '',
        data_map: list = [],
        db_table: str = '',
        client_id: str = '',
        file_name: str = '',
        password: str = '',
        schedule: str = '',
        sync_keys: dict = {'source': '', 'destination': ''},
        warehouse: str = '',
        data_source: str = '',
        cluster_name: str = '',
        client_secret: str = '',
        organization: str = '',
        authentication_type: str = ''
    ):
        self.label = label
        self.connector_type = connector_type
        self.connector_action = connector_action
        self.input_type = input_type
        self.filter_type = filter_type
        self.file_names = file_names
        self.bucket = bucket
        self.filter_by_columns = filter_by_columns
        self.all = all
        self.arn = arn
        self.host = host
        self.path = path
        self.port = port
        self.role = role
        self.soql = soql
        self.query = query
        self.token = token
        self.column = column
        self.db_name = db_name
        self.db_user = db_user
        self.period = period
        self.schema = schema
        self.secret = secret
        self.account = account
        self.data_map = data_map
        self.db_table = db_table
        self.client_id = client_id
        self.file_name = file_name
        self.password = password
        self.schedule = schedule
        self.sync_keys = sync_keys
        self.warehouse = warehouse
        self.data_source = data_source
        self.cluster_name = cluster_name
        self.client_secret = client_secret
        self.organization = organization
        self.authentication_type = authentication_type

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'ReverseMLWorkflow',
            'label': self.label,
            'params': {
                'connectorType': self.connector_type,
                'connectorAction': self.connector_action,
                'inputType': self.input_type,
                'filterType': self.filter_type,
                'fileNames': self.file_names,
                'bucket': self.bucket,
                'filterByColumns': self.filter_by_columns,
                'all': self.all,
                'arn': self.arn,
                'host': self.host,
                'path': self.path,
                'port': self.port,
                'role': self.role,
                'soql': self.soql,
                'query': self.query,
                'token': self.token,
                'column': self.column,
                'dbName': self.db_name,
                'dbUser': self.db_user,
                'period': self.period,
                'schema': self.schema,
                'secret': self.secret,
                'account': self.account,
                'dataMap': self.data_map,
                'dbTable': self.db_table,
                'clientId': self.client_id,
                'fileName': self.file_name,
                'password': self.password,
                'schedule': self.schedule,
                'syncKeys': self.sync_keys,
                'warehouse': self.warehouse,
                'dataSource': self.data_source,
                'clusterName': self.cluster_name,
                'clientSecret': self.client_secret,
                'organization': self.organization,
                'authenticationType': self.authentication_type
            }
        }
