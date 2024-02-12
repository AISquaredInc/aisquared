from aisquared.base import BaseObject


class ChatRendering(BaseObject):

    def __init__(
            self,
            return_key,
            prediction_value_key=None,
            sender_name='You',
            responder_name='Chatbot'
    ):
        super().__init__()
        self.return_key = return_key
        self.prediction_value_key = prediction_value_key
        self.sender_name = sender_name
        self.responder_name = responder_name

    @property
    def return_key(self):
        return self._return_key

    @return_key.setter
    def return_key(self, value):
        self._return_key = value

    @property
    def prediction_value_key(self):
        return self._prediction_value_key

    @prediction_value_key.setter
    def prediction_value_key(self, value):
        self._prediction_value_key = value

    @property
    def sender_name(self):
        return self._sender_name

    @sender_name.setter
    def sender_name(self, value):
        self._sender_name = value

    @property
    def responder_name(self):
        return self._responder_name

    @responder_name.setter
    def responder_name(self, value):
        self._responder_name = value

    def to_dict(self):
        return {
            'className': 'ChatRendering',
            'params': {
                'returnKey': self.return_key,
                'predictionValueKey': self.prediction_value_key,
                'senderName': self.sender_name,
                'responderName': self.responder_name
            }
        }
