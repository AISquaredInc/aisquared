from aisquared.base import BaseObject


class AddValue(BaseObject):
    """
    Preprocessing step to add a value to all pixels in an image
    """

    def __init__(
            self,
            value
    ):
        """
        Parameters
        ----------
        value : int or float
            The value to add
        """
        super().__init__()
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('value must be int or float')
        self._value = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'Add',
            'params': {
                'value': self.value
            }
        }


class SubtractValue(BaseObject):
    """
    Preprocessing step to subtract a value from all pixels in an image
    """

    def __init__(
            self,
            value
    ):
        """
        Parameters
        ----------
        value : int or float
            The value to subtract
        """
        super().__init__()
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('value must be int or float')
        self._value = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'Subtract',
            'params': {
                'value': self.value
            }
        }


class MultiplyValue(BaseObject):
    """
    Preprocessing step to multiply all pixels in an image by a value
    """

    def __init__(
            self,
            value
    ):
        """
        Parameters
        ----------
        value : int or float
            The value to multiply all pixels by
        """
        super().__init__()
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('value must be int or float')
        self._value = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'Multiply',
            'params': {
                'value': self.value
            }
        }


class DivideValue(BaseObject):
    """
    Preprocessing step to divide all pixels in an image by a value
    """

    def __init__(
            self,
            value
    ):
        """
        Parameters
        ----------
        value : int or float
            The value to divide all pixels by
        """
        super().__init__()
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('value must be int or float')
        self._value = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'Divide',
            'params': {
                'value': self.value
            }
        }


class ConvertToColor(BaseObject):
    """
    Preprocessing step to convert images to a color scheme
    """

    def __init__(self, color):
        """
        Parameters
        ----------
        color : str
            Either 'RGB' or 'B+W', each corresponding to RGB or grayscale color schemes, respectively
        """
        super().__init__()
        self.color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise TypeError('color must be string')
        if value not in ['RGB', 'B+W']:
            raise ValueError('color must be one of `RGB` or `B+W`')
        self._color = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'ConvertToColor',
            'params': {
                'color': self.color
            }
        }


class Resize(BaseObject):
    """
    Preprocessing step to resize an image
    """

    def __init__(
            self,
            size,
            method='bilinear',
            preserve_aspect_ratio=False
    ):
        """
        Parameters
        ----------
        size : list
            List of two integer values, supplied as [`height`, `width`], to resize images to
        method : str (default 'bilinear')
            The method to use for resizing. Must be one of 'bilinear', 'lanczos3', 'lanczos5', 'bicubic', 'gaussian',
            'nearest', or 'mitchellcubic'
        preserve_aspect_ratio : bool (default False)
            Whether to preserve aspect ratio when resizing
        """
        super().__init__()
        self.size = size
        self.method = method
        self.preserve_aspect_ratio = preserve_aspect_ratio

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if not isinstance(value, list):
            raise TypeError('size must be a list')
        if len(value) != 2 or not all([isinstance(val, int) for val in value]):
            raise ValueError('size must be a list of two integers')
        self._size = value

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        allowed_methods = [
            'bilinear',
            'lanczos3',
            'lanczos5',
            'bicubic',
            'gaussian',
            'nearest',
            'area',
            'mitchellcubic'
        ]
        if value not in allowed_methods:
            raise ValueError(f'method must be one of {allowed_methods}')
        self._method = value

    @property
    def preserve_aspect_ratio(self):
        return self._preserve_aspect_ratio

    @preserve_aspect_ratio.setter
    def preserve_aspect_ratio(self, value):
        if not isinstance(value, bool):
            raise TypeError('preserve_aspect_ratio must be bool')
        self._preserve_aspect_ratio = value

    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'Resize',
            'params': {
                'size': self.size,
                'method': self.method,
                'preserveAspectRatio': self.preserve_aspect_ratio
            }
        }
