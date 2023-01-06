from .BaseObject import BaseObject


class CustomObject(BaseObject):
    """
    Custom class that allows the user to define custom classes for configuration

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.base.CustomObject(
        'MyClass',
        key1 = 'foo',
        key2 = 'bar'
        )
    >>> my_obj.to_dict()
    {'className': 'MyClass', 'params': {'key1': 'foo', 'key2': 'bar'}}
    )
    """

    def __init__(self, class_name: str, **kwargs):
        """
        Parameters
        ----------
        class_name : str
            The name for the class
        **kwargs : additional keyword arguments
            Other parameters to be used
        """
        super().__init__()
        self.class_name = class_name
        self.params = kwargs
        self.path = kwargs.get('path')

    def to_dict(self) -> dict:
        """
        Get the object as a dictionary
        """
        return {
            'className': self.class_name,
            'params': self.params
        }
