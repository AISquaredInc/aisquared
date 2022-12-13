from aisquared.base import BaseObject


class TableRendering(BaseObject):

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

        super().__init__()
        self.label = label
        self.id = id
        self.container_id = container_id
        self.prediction_name_key = prediction_name_key
        self.prediction_value_key = prediction_value_key
        self.prediction_name_values = prediction_name_values
        self.table_name = table_name

    def to_dict(self):
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
