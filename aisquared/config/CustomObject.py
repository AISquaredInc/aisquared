from aisquared.base import BaseObject


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

    def __init__(self, class_name: str, top_level_kwargs: dict = None, **kwargs):
        """
        Parameters
        ----------
        class_name : str
            The name for the class
        top_level_kwargs : dict or None (default None)
            Any top-level keyword arguments to place above the `params` dictionary
        **kwargs : additional keyword arguments
            Other parameters to be used
        """
        super().__init__()
        self.class_name = class_name
        self.params = kwargs
        self.path = kwargs.get('path')
        self.top_level_kwargs = top_level_kwargs

    def to_dict(self) -> dict:
        """
        Get the object as a dictionary
        """
        config = {
            'className': self.class_name,
            'params': self.params
        }
        if isinstance(self.top_level_kwargs, dict):
            for k, v in self.top_level_kwargs.items():
                config[k] = v
        return config
