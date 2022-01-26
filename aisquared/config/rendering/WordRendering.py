import json
import warnings

ALLOWED_DECORATIONS = (
    'underline',
    'highlight',
    'badge'
)

ALLOWED_COLORS = (
    'blue',
    'red',
    'green',
    'yellow',
    'orange',
    'purple',
    'pink',
    'black',
    'grey',
    'white'
)

ALLOWED_SHAPES = (
    'star',
    'circle',
    'square'
)

class WordRendering:
    
    def __init__(
        self,
        decoration = ALLOWED_DECORATIONS[0],
        color = ALLOWED_COLORS[0],
        shape = None,
        word_list = None
    ):
        self.decoration = decoration
        self.color = color
        self.shape = shape
        self.word_list = word_list

    @property
    def decoration(self):
        return self._decoration
    @decoration.setter
    def decoration(self, value):
        if value not in ALLOWED_DECORATIONS:
            raise ValueError(f'decoration must be one of {ALLOWED_DECORATIONS}, got {value}')
        self._decoration = value

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        self._color = value

    @property
    def shape(self):
        return self._shape
    @shape.setter
    def shape(self, value):
        if value is not None:
            if value not in ALLOWED_SHAPES:
                raise ValueError(f'shape must be one of {ALLOWED_SHAPES}, got {value}')
            if self.decoration != ALLOWED_DECORATIONS[-1]:
                warnings.warn('shape parameter will not be used unless badge decoration is specified')
        self._shape = value

    @property
    def word_list(self):
        return self._word_list
    @word_list.setter
    def word_list(self, value):
        self._word_list = value

    def to_dict(self):
        return {
            'className' : 'WordRendering',
            'params' : {
                'decoration' : self.decoration,
                'color' : self.color,
                'shape' : self.shape,
                'wordList' : self.word_list
            }
        }

    def to_json(self):
        return json.dumps(self.to_dict())
