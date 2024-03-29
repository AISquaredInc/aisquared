from typing import Union
from aisquared.base import BaseObject


class QueryParameterHarvester(BaseObject):
    """
    Harvester for Query Parameters

    Example usage:

    >>> import aisquared
    >>> my_obj = aisquared.config.harvesting.QueryParameterHarvester(
        'test_key',
        'test_url',
        'test_attribute'
    )
    >>> my_obj.to_dict()
    {'className': 'QueryParameterHarvester',
    'params': {'queryKeys': ['test_key'],
    'urlLocations': ['test_url'],
    'attributes': ['test_attribute']}}

    """

    def __init__(
        self,
        query_keys: Union[str, list],
        url_locations: Union[str, list],
        attributes: Union[str, list]
    ):
        """
        Parameters
        ----------
        query_keys : list of str
            Keys to use in the query
        url_locations : list of str
            URL Locations to query from
        attributes : list of str
            Attributes for the query
        """
        self.query_keys = query_keys
        self.url_locations = url_locations
        self.attributes = attributes

    @property
    def query_keys(self):
        return self._query_keys

    @query_keys.setter
    def query_keys(self, value):
        if isinstance(value, str):
            value = [value]

        if not isinstance(value, list) or not all([isinstance(v, str) for v in value]):
            raise ValueError('query_keys must be list of strings')

        self._query_keys = value

    @property
    def url_locations(self):
        return self._url_locations

    @url_locations.setter
    def url_locations(self, value):
        if isinstance(value, str):
            value = [value]

        if not isinstance(value, list) or not all([isinstance(v, str) for v in value]):
            raise ValueError('url_locations must be list of strings')

        self._url_locations = value

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        if isinstance(value, str):
            value = [value]

        if not isinstance(value, list) or not all([isinstance(v, str) for v in value]):
            raise ValueError('attributes must be list of strings')

        self._attributes = value

    def to_dict(self) -> dict:
        """
        Get the configuration object as a dictionary
        """
        return {
            'className': 'QueryParameterHarvester',
            'params': {
                'queryKeys': self.query_keys,
                'urlLocations': self.url_locations,
                'attributes': self.attributes
            }
        }
