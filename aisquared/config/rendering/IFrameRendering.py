from .RenderingObject import RenderingObject


class IFrameRendering(RenderingObject):
    """
    Object which dictates how to render IFrames into the webpage

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.renderingIFrameRendering('http://example-page.com', '600px', '100%')
    >>> my_obj.to_dict()
    {'className': 'IFrameRendering',
    'params': {'src': 'http://example-page.com',
    'width': '600px',
    'height': '100%',
    'isOverlay': True,
    'position': 'right',
    'querySelector': None}}
    """

    def __init__(
            self,
            src: str,
            width: str,
            height: str,
            is_overlay: bool = True,
            position: str = 'right',
            query_selector: str = None
    ):
        """
        Parameters
        ----------
        src : str
            The URL of the page to embed
        width : str
            The width of the page. Accepts CSS string values (100px, 100%, 100vw)
        height : str
            The height of the page. Accepts CSS string values (100px, 100%, 100vw)
        is_overlay : bool (default True)
            Whether to overlay onto the existing page or not
        position : str (default 'right')
            One of 'top', 'right', 'bottom', or 'left'. If `is_overlay` is True, must be provided
        query_selector : str or None (default None)
            Query selector string to determine where to embed IFrame. If `is_overlay` is False, must be provided
        """

        super().__init__()
        self.src = src
        self.width = width
        self.height = height
        self.is_overlay = is_overlay
        self.position = position
        self.query_selector = query_selector

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, value):
        if not isinstance(value, str):
            raise TypeError('src must be string')
        self._src = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if not isinstance(value, str):
            raise TypeError('width must be string')
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if not isinstance(value, str):
            raise TypeError('height must be string')
        self._height = value

    @property
    def is_overlay(self):
        return self._is_overlay

    @is_overlay.setter
    def is_overlay(self, value):
        if not isinstance(value, bool):
            raise TypeError('is_overlay must be bool')
        self._is_overlay = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError('position must be str or None')
        if value is None and self.is_overlay:
            raise ValueError('position must be provided if is_overlay is True')
        self._position = value

    @property
    def query_selector(self):
        return self._query_selector

    @query_selector.setter
    def query_selector(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError('query_selector must be str or None')
        if value is None and not self.is_overlay:
            raise ValueError(
                'query_selector must be provided if is_overlay is False')
        self._query_selector = value

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'IFrameRendering',
            'params': {
                'src': self.src,
                'width': self.width,
                'height': self.height,
                'isOverlay': self.is_overlay,
                'position': self.position,
                'querySelector': self.query_selector
            }
        }
