from aisquared.base import BaseObject, DEFAULT_CHART_RENDERING_CSS, CHART_RENDERING_CSS_FILE
import json
import os


class BarChartRendering(BaseObject):

    """
    Rendering class for rendering a Bar Chart

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.rendering.BarChartRendering(
        'my_label',
        'my_id',
        'my_bar_chart',
        'my_container_id',
        'name',
        'value',
        'name_value',
        True,
        'circle'
    )
    >>> my_obj.to_dict()
    {'className': 'BarChartRendering',
        'label': 'my_label',
        'params': {'id': 'my_id',
        'chartName': 'my_bar_chart',
        'containerId': 'my_container_id',
        'displayLegend': True,
        'legendIcon': 'circle',
        'width': 'auto',
        'height': 'auto',
        'xOffset': '0',
        'yOffset': '0',
        'datasource': [{'labels': None,
            'labelsKey': None,
            'consolidateRows': True,
            'predictionNameKey': 'name',
            'predictionValueKey': 'value',
            'predictionNameValue': 'name_value'}]}}
    """

    def __init__(
        self,
        label: str,
        id: str,
        chart_name: str,
        container_id: str,
        prediction_name_key: str,
        prediction_value_key: str,
        prediction_name_value: str,
        display_legend: bool,
        legend_icon: str,
        labels_key: str = None,
        width: str = 'auto',
        height: str = 'auto',
        xOffset: str = '0',
        yOffset: str = '0',
        labels: list = None,
        consolidate_rows: bool = True,
        css_params: dict = None
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
        labels_key : str
            The key to use for the labels
        width : str (default 'auto')
            The width of the chart
        height : str (default 'auto')
            The height of the chart
        xOffset : str (default '0')
            The offset on the x axis
        yOffset : str (default '0')
            The offset on the y axis
        labels : list of str or None (default None)
            Labels, if hard-coded
        consolidate_rows : bool (default True)
            Whether to consolidate rows in the data
        css_params: dict or None (default None)
            Additional CSS parameters

        """
        super().__init__()
        self.label = label
        self.id = id
        self.chart_name = chart_name
        self.labels = labels
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
        self.consolidate_rows = consolidate_rows
        self.labels_key = labels_key

        if css_params is None:
            if os.path.exists(CHART_RENDERING_CSS_FILE):
                with open(CHART_RENDERING_CSS_FILE, 'r') as f:
                    self.css_params = json.load(f)
            else:
                self.css_params = DEFAULT_CHART_RENDERING_CSS

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'BarChartRendering',
            'label': self.label,
            'params': {
                'id': self.id,
                'chartName': self.chart_name,
                'containerId': self.container_id,
                'displayLegend': self.display_legend,
                'legendIcon': self.legend_icon,
                'width': self.width,
                'height': self.height,
                'xOffset': self.xOffset,
                'yOffset': self.yOffset,
                'datasource': [
                    {
                        'labels': self.labels,
                        'labelsKey': self.labels_key,
                        'consolidateRows': self.consolidate_rows,
                        'predictionNameKey': self.prediction_name_key,
                        'predictionValueKey': self.prediction_value_key,
                        'predictionNameValue': self.prediction_name_value,
                    }
                ],
                'style': self.css_params['style']
            }
        }
