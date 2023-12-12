from aisquared.base import BaseObject, DEFAULT_TABLE_RENDERING_CSS, TABLE_RENDERING_CSS_FILE
import platform
import json
import os


class TableRendering(BaseObject):
    """
    Class for rendering tables

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.rendering.TableRendering(
        'my table',
        'MyTableID',
        'MyContainerID',
        'name_key',
        'value_key',
        'name_values'
    )
    >>> my_obj.to_dict()
    {'className': 'TableRendering',
    'label': 'my table',
    'params': {'id': 'MyTableID',
    'containerId': 'MyContainerID',
    'predictionNameKey': 'name_key',
    'predictionValueKey': 'value_key',
    'predictionNameValues': 'name_values',
    'tableName': ''}}

    """

    def __init__(
        self,
        label: str,
        id: str,
        container_id: str,
        prediction_name_key: str,
        prediction_value_key: str,
        prediction_name_values: str,
        table_name: str = '',
        css_params: dict = None
    ):
        """
        Parameters
        ----------
        label : str
            Label for the table
        id : str
            ID for the table
        container_id : str
            The ID for the container
        prediction_name_key : str
            The key to use for the prediction name
        prediction_value_key : str
            The key to use for the prediction value
        prediction_name_values : list of str
            The name of the values for the prediction
        css_params : dict or None (default None)
            Additional CSS parameters
        """

        super().__init__()
        self.label = label
        self.id = id
        self.container_id = container_id
        self.prediction_name_key = prediction_name_key
        self.prediction_value_key = prediction_value_key
        self.prediction_name_values = prediction_name_values
        self.table_name = table_name

        if css_params is None:
            if os.path.exists(TABLE_RENDERING_CSS_FILE):
                with open(TABLE_RENDERING_CSS_FILE, 'r') as f:
                    self.css_params = json.load(f)
            else:
                self.css_params = DEFAULT_TABLE_RENDERING_CSS
        else:
            if css_params.get('style'):
                self.css_params = css_params
            else:
                self.css_params = {'style': css_params}

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'TableRendering',
            'label': self.label,
            'params': {
                'id': self.id,
                'containerId': self.container_id,
                'predictionNameKey': self.prediction_name_key,
                'predictionValueKey': self.prediction_value_key,
                'predictionNameValues': self.prediction_name_values,
                'tableName': self.table_name,
                'style': self.css_params['style']
            }
        }
