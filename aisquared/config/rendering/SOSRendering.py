from aisquared.base import BaseObject


class SOSRendering(BaseObject):
    """
    Rendering of an SOS dashboard
    """

    def __init__(
        self,
        can_toggle,
        label=''
    ):
        """
        Parameters
        ----------
        can_toggle : bool
            Whether the dashboard can be toggled on and off
        label : str (default '')
            The label for the rendering
        """
        super().__init__()
        self.can_toggle = can_toggle
        self.label = label

    @property
    def can_toggle(self):
        return self._can_toggle

    @can_toggle.setter
    def can_toggle(self, value):
        if not isinstance(value, bool) and value is not None:
            raise TypeError('can_toggle must be boolean or None')
        self._can_toggle = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        if not isinstance(value, str):
            raise TypeError('label must be str')
        self._label = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'SOSRendering',
            'label': self.label,
            'params': {
                'canToggle': self.can_toggle
            }
        }
