from aisquared.base import BaseObject


class DashboardReplacementRendering(BaseObject):
    """
    Rendering for dashboard replacement
    """

    def __init__(
        self,
        anchor_selector,
        where_replace='',
        label=''
    ):
        """
        Parameters
        ----------
        anchor_selector : str
            The anchor selector
        where_replace : str (default '')
            Where to replace
        label : str (default '')
            The label for the rendering
        """
        super().__init__()
        self.anchor_selector = anchor_selector
        self.where_replace = where_replace
        self.label = label

    @property
    def anchor_selector(self):
        return self._anchor_selector

    @anchor_selector.setter
    def anchor_selector(self, value):
        self._anchor_selector = value

    @property
    def where_replace(self):
        return self._where_replace

    @where_replace.setter
    def where_replace(self, value):
        self._where_replace = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'DashboardReplacementRendering',
            'label': self.label,
            'params': {
                'anchorSelector': self.anchor_selector,
                'whereReplace': self.where_replace
            }
        }
