from aisquared.base import BaseObject, DEFAULT_HTML_TAG_RENDERING_CSS, HTML_TAG_RENDERING_CSS_FILE
import platform
import json
import os


class HTMLTagRendering(BaseObject):
    """
    Rendering for HTML tags

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.rendering.HTMLTagRendering(
        'my HTML tag',
        'MyHTMLTagRenderingID',
        'MyContainerID',
        '<p>Example Text</p>',
        'extra_tag',
        'append',
        'name_key',
        'value_key',
        'name_value'
    )
    >>> my_obj.to_dict()
    {'className': 'HTMLTagRendering',
    'label': 'my HTML tag',
    'params': {'id': 'MyHTMLTagRenderingID',
    'containerId': 'MyContainerID',
    'htmlContent': '<p>Example Text</p>',
    'extraContentTag': 'extra_tag',
    'injectionAction': 'append',
    'predictionNameKey': 'name_key',
    'predictionValueKey': 'value_key',
    'predictionNameValue': 'name_value',
    'content': ''}}

    """

    def __init__(
        self,
        label: str,
        id: str,
        container_id: str,
        html_content: str,
        extra_content_tag: str,
        injection_action: str,
        prediction_name_key: str,
        prediction_value_key: str,
        prediction_name_value: str,
        content: str = '',
        css_params: dict = None
    ):
        """
        Parameters
        ----------
        label : str
            The label for the HTML tag
        id : str
            The ID for the HTML tag
        container_id : str
            The ID of the container
        html_content : str
            HTML to render
        extra_content_tag : str
            Any extra content tags to render
        injection_action : str
            The injection action
        prediction_name_key : str
            The key for the prediction name
        prediction_value_key : str
            The key for the prediction value
        prediction_name_values : str
            The value for the prediction name
        content : str (default '')
            The content
        css_params : dict or None (default None)
            Additional CSS parameters
        """
        super().__init__()
        self.label = label
        self.id = id
        self.container_id = container_id
        self.html_content = html_content
        self.extra_content_tag = extra_content_tag
        self.injection_action = injection_action
        self.prediction_name_key = prediction_name_key
        self.prediction_value_key = prediction_value_key
        self.prediction_name_value = prediction_name_value
        self.content = content

        if css_params is None:
            if os.path.exists(HTML_TAG_RENDERING_CSS_FILE):
                with open(HTML_TAG_RENDERING_CSS_FILE, 'r') as f:
                    self.css_params = json.load(f)
            else:
                self.css_params = DEFAULT_HTML_TAG_RENDERING_CSS
        else:
            if css_params.get('style'):
                self.css_params = css_params
            else:
                self.css_params = {'style': css_params}

    def to_dict(self) -> dict:
        """
        Return the configuration object as a dictionary
        """
        return {
            'className': 'HTMLTagRendering',
            'label': self.label,
            'params': {
                'id': self.id,
                'containerId': self.container_id,
                'htmlContent': self.html_content,
                'extraContentTag': self.extra_content_tag,
                'injectionAction': self.injection_action,
                'predictionNameKey': self.prediction_name_key,
                'predictionValueKey': self.prediction_value_key,
                'predictionNameValue': self.prediction_name_value,
                'content': self.content,
                'style': self.css_params['style']
            }
        }
