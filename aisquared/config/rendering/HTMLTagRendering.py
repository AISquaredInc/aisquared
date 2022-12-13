from aisquared.base import BaseObject


class HTMLTagRendering(BaseObject):

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
