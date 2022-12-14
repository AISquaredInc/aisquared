from aisquared.base import BaseObject


class TableRendering(BaseObject):
    """
    Class for rendering tables
    """

    def __init__(
        self,
        label,
        id,
        container_id,
        prediction_name_key,
        prediction_value_key,
        prediction_name_values,
        table_name='',
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
        """

        super().__init__()
        self.label = label
        self.id = id
        self.container_id = container_id
        self.prediction_name_key = prediction_name_key
        self.prediction_value_key = prediction_value_key
        self.prediction_name_values = prediction_name_values
        self.table_name = table_name

    def to_dict(self):
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
                'tableName': self.table_name
            }
        }
