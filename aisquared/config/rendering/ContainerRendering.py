from aisquared.base import BaseObject, POSITIONS, STATIC_POSITIONS, DEFAULT_CONTAINER_RENDERING_CSS, CONTAINER_RENDERING_CSS_FILE
import platform
import json
import os


class ContainerRendering(BaseObject):
    """
    Rendering for a container

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.rendering.ContainerRendering(
        'my container',
        'myContainerID',
        "[data-id='tabpanel-general']"
    )
    >>> my_obj.to_dict()
    {'className': 'ContainerRendering',
    'label': 'my container',
    'params': {'id': 'myContainerID',
    'width': 'auto',
    'height': 'auto',
    'display': 'flex',
    'xOffset': '0',
    'yOffset': '0',
    'position': 'absolute',
    'orientation': 'column',
    'querySelector': "[data-id='tabpanel-general']",
    'staticPosition': None}}

    """

    def __init__(
        self,
        label: str,
        id: str,
        query_selector: str,
        position: str = 'absolute',
        static_position: str = None,
        width: str = 'auto',
        height: str = 'auto',
        display: str = 'flex',
        xOffset: str = '0',
        yOffset: str = '0',
        orientation: str = 'column',
        css_params: dict = None
    ):
        """
        Parameters
        ----------
        label : str
            The label for the object
        id : str
            The id for the object
        query_selector : str
            Query selector for which panel to place the container in
        position : str (default 'absolute')
            The position to place the container in, either 'absolute' or 'static'
        static_position : str or None (default None)
            If `position` is 'static', must be provided, either 'prepend' or 'append'
        width : str (default 'auto')
            The width of the rendering
        height : str (default 'auto')
            The height of the rendering
        display : str (default 'flex')
            The type of display
        xOffset : str (default '0')
            The x offset of the rendering
        yOffset : str (default '0')
            The y offset of the rendering
        orientation : str (default 'column')
            The orientation of the rendering
        css_params : dict or None (default None)
            Additional CSS parameters
        """
        super().__init__()
        self.label = label
        self.id = id
        self.query_selector = query_selector
        self.position = position
        self.static_position = static_position
        self.width = width
        self.height = height
        self.display = display
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.orientation = orientation

        if css_params is None:
            if os.path.exists(CONTAINER_RENDERING_CSS_FILE):
                with open(CONTAINER_RENDERING_CSS_FILE, 'r') as f:
                    self.css_params = json.load(f)
            else:
                self.css_params = DEFAULT_CONTAINER_RENDERING_CSS

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def query_selector(self):
        return self._query_selector

    @query_selector.setter
    def query_selector(self, value):
        self._query_selector = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, value):
        self._display = value

    @property
    def xOffset(self):
        return self._xOffset

    @xOffset.setter
    def xOffset(self, value):
        self._xOffset = value

    @property
    def yOffset(self):
        return self._yOffset

    @yOffset.setter
    def yOffset(self, value):
        self._yOffset = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if value not in POSITIONS:
            raise ValueError(
                f'position must be one of {POSITIONS}, got {value}')
        self._position = value

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value

    @property
    def static_position(self):
        return self._static_position

    @static_position.setter
    def static_position(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError('If not None, static_position must be str')
            if value not in STATIC_POSITIONS:
                raise ValueError(
                    f'static_position must be one of {STATIC_POSITIONS}, got {value}')
        else:
            if self.position == 'static':
                raise ValueError(
                    'If position is "static", static_position must be provided')

        self._static_position = value

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'ContainerRendering',
            'label': self.label,
            'params': {
                'id': self.id,
                'width': self.width,
                'height': self.height,
                'display': self.display,
                'xOffset': self.xOffset,
                'yOffset': self.yOffset,
                'position': self.position,
                'orientation': self.orientation,
                'querySelector': self.query_selector,
                'position': self.position,
                'staticPosition': self.static_position,
                'style': self.css_params['style']
            }
        }
