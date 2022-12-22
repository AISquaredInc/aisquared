from aisquared.base import BaseObject


class ContainerRendering(BaseObject):
    """
    Rendering for a container
    """

    def __init__(
        self,
        label,
        id,
        query_selector,
        width='auto',
        height='auto',
        display='flex',
        xOffset='0',
        yOffset='0',
        position='',
        orientation='column'
    ):
        """
        Parameters
        ----------
        label : str
            The label for the object
        id : str
            The id for the object
        width : str (default 'auto')
            The width of the rendering
        height : str (default '75')
            The height of the rendering
        display : str (default 'flex')
            The type of display
        xOffset : str (default '0')
            The x offset of the rendering
        yOffset : str (default '0')
            The y offset of the rendering
        position : str (default '')
            The position of the rendering
        orientation : str (default 'column')
            The orientation of the rendering
        """
        super().__init__()
        self.label = label
        self.id = id
        self.query_selector = query_selector
        self.width = width
        self.height = height
        self.display = display
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.position = position
        self.orientation = orientation

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
        self._position = value

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value

    def to_dict(self):
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
                'querySelector': self.query_selector
            }
        }
