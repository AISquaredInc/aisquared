from aisquared.base import BaseObject


class ImageHarvester(BaseObject):
    """
    Object to harvest images

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.harvesting.ImageHarvester()
    >>> my_obj.to_dict()
    {'className': 'ImageHarvester', 'params': {'how' : 'all'}}

    """

    def __init__(
        self,
        how: str = 'all'
    ):
        """
        Parameters
        ----------
        how : str (default 'all')
            Which images to harvest (CURRENTLY ONLY SUPPORTS 'all')
        """
        super().__init__()
        self.how = how

    @property
    def how(self):
        return self._how

    @how.setter
    def how(self, value):
        if value != 'all':
            raise ValueError(
                "Currently the only value supported for how is 'all'")
        self._how = value

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'ImageHarvester',
            'params': {
                'how': self.how
            }
        }
