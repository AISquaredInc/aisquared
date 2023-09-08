from aisquared.base import BaseObject


class CustomRendering(BaseObject):

    def __init__(
            self,
            id: str,
            content_html: str,
            content_script: str,
            content_style: str,
            query_selector: str = None,

    ):
        super().__init__()
        self.id = id
        self.content_html = content_html
        self.content_script = content_script
        self.content_style = content_style
        self.query_selector = query_selector

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, str):
            raise TypeError('id must be str')
        self._id = value

    @property
    def content_html(self):
        return self._content_html

    @content_html.setter
    def content_html(self, value):
        if not isinstance(value, str):
            raise TypeError('content_html must be str')
        self._content_html = value

    @property
    def content_script(self):
        return self._content_script

    @content_script.setter
    def content_script(self, value):
        if not isinstance(value, str):
            raise TypeError('content_script must be str')
        self._content_script = value

    @property
    def query_selector(self):
        return self._query_selector

    @query_selector.setter
    def query_selector(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError('query_selector must be str or None')
        self._query_selector = value

    @property
    def content_style(self):
        return self._content_style

    @content_style.setter
    def content_style(self, value):
        if not isinstance(value, str):
            raise TypeError('content_style must be str')
        self._content_style = value

    def to_dict(self):
        return {
            'className': 'CustomRendering',
            'params': {
                'id': self.id,
                'querySelector': self.query_selector,
                'contentHtml': self.content_html,
                'contentScript': self.content_script,
                'contentStyle': self.content_style
            }
        }
