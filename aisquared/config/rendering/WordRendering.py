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
    """
    Object which dictates how words are rendered
    """

    def __init__(
        self,
        decoration = ALLOWED_DECORATIONS[0],
        color = ALLOWED_COLORS[0],
        shape = None,
        word_list = None
    ):
        f"""
        decoration : str (default {ALLOWED_DECORATIONS[0]})
            What kind of decoration to apply
        color : str or dict (default {ALLOWED_COLORS[0]})
            The color to apply with the decoration
        shape : str or None (default None)
            The shape to apply, if 'badge' is selected as the decoration value
        word_list : list, dict, string, or None (default None)
            A set of words to apply decoration to

        Notes
        -----
        - If 'decoration' is 'badge', then color is ignored
        - Shape is only utilized if 'decoration' is 'badge'
        - For word_list and color, per-class values can be supplied in a dictionary format where
          keys are the names of the classes and values are the color/word(s) to apply rendering to
        - If word_list is 'PREDICTION', then the rendering is applied based on the classes identified 
          from the prediction values
        """
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
        """Return the object as a dictionary"""
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
        """Return the object as a JSON string"""
        return json.dumps(self.to_dict())
