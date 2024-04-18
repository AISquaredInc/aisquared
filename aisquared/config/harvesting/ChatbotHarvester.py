from aisquared.base import BaseObject


class ChatbotHarvester(BaseObject):
    """
    Harvesting for a chatbot
    """

    def __init__(
            self,
            title,
            harvest_history=False,
            input_type='text',
            features=None,
            max_length=None
    ):
        """
        Parameters
        ----------
        title : str
            The title for the chat conversation
        harvest_history : bool (default False)
            Whether to harvest chat history or just the last sent text
        input_type : str (default 'text')
            The input type (should not be changed)
        features : default None
            Should not be changed
        max_length : default None
            Should not be changed
        """
        super().__init__()
        self.title = title
        self.harvest_history = harvest_history
        self.input_type = input_type
        self.features = features
        self.max_length = max_length

    def to_dict(self):
        """
        Return the configuration object as a dictionary
        """
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
