from aisquared.base import BaseObject


class PieChartRendering(BaseObject):
    """
    Rendering class for rendering a Pie Chart
    """

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
        display_legend,
        legend_icon,
        width='auto',
        height='auto',
        xOffset='0',
        yOffset='0',

    ):
        """
        Parameters
        ----------
        label : str
            The label for the chart
        id : str
            The ID for the chart
        chart_name : str
            The name for the chart
        chart_colors : list of str
            List of colors to use
        chart_labels : list of str
            List of labels to use
        container_id : str
            The ID of the container to use
        prediction_name_key : str
            The key to use for the prediction name
        prediction_value_key : str
            The key to use for the prediction value
        prediction_name_value : str
            The value to use for the prediction name
        display_legend : bool
            Whether to display the chart legend
        legend_icon : str
            The legend icon to display
        width : str (default 'auto')
            The width of the chart
        height : str (default 'auto')
            The height of the chart
        xOffset : str (default '0')
            The offset on the x axis
        yOffset : str (default '0')
            The offset on the y axis
        """
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
        self.display_legend = display_legend
        self.legend_icon = legend_icon
        self.width = width
        self.height = height
        self.xOffset = xOffset
        self.yOffset = yOffset

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'PieChartRendering',
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
                'displayLegend': self.display_legend,
                'legendIcon': self.legend_icon,
                'width': self.width,
                'height': self.height,
                'xOffset': self.xOffset,
                'yOffset': self.yOffset
            }
        }
