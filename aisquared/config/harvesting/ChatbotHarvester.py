from aisquared.base import BaseObject


class ChatbotHarvester(BaseObject):

    def __init__(
            self,
            title,
            harvest_history=False,
            input_type='text',
            features=None,
            max_length=None
    ):
        super().__init__()
        self.title = title
        self.harvest_history = harvest_history
        self.input_type = input_type
        self.features = features
        self.max_length = max_length

    def to_dict(self):
        return {
            'className': 'ChatbotHarvester',
            'params': {
                'title': self.title,
                'harvestHistory': self.harvest_history,
                'inputType': self.input_type,
                'features': self.features,
                'maxLength': self.max_length
            }
        }
