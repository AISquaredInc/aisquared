from aisquared.base import BaseObject


class DoughnutChartRendering(BaseObject):

    def __init__(
        self,
        label,
        id,
        chart_name,
        chart_colors,
        chart_labels,
        container_id,
        prediction_name_key,
        prediction_value_key,
        prediction_name_value,
        width='auto',
        height='auto',
        xOffset='0',
        yOffset='0',

    ):
        super().__init__()
        self.label = label
        self.id = id
        self.chart_name = chart_name
        self.chart_colors = chart_colors
        self.chart_labels = chart_labels
        self.container_id = container_id
        self.prediction_name_key = prediction_name_key
        self.prediction_value_key = prediction_value_key
        self.prediction_name_value = prediction_name_value
        self.width = width
        self.height = height
        self.xOffset = xOffset
        self.yOffset = yOffset

    def to_dict(self):
        return {
            'className': 'DoughnutChartRendering',
            'label': self.label,
            'params': {
                'id': self.id,
                'chartName': self.chart_name,
                'chartColors': self.chart_colors,
                'chartLabels': self.chart_labels,
                'containerId': self.container_id,
                'predictionNameKey': self.prediction_name_key,
                'predictionValueKey': self.prediction_value_key,
                'predictionNameValue': self.prediction_name_value,
                'width': self.width,
                'height': self.height,
                'xOffset': self.xOffset,
                'yOffset': self.yOffset
            }
        }
