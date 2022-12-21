from aisquared.base import BaseObject


class HTMLTagRendering(BaseObject):
    """
    Rendering for HTML tags
    """

    def __init__(
        self,
        label,
        id,
        container_id,
        html_content,
        extra_content_tag,
        injection_action,
        prediction_name_key,
        prediction_value_key,
        prediction_name_value,
        content=''
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

    def to_dict(self):
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
                'content': self.content
            }
        }
