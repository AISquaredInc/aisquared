from aisquared.base import BaseObject

class QueryParameterHarvester(BaseObject):

    def __init__(
        self,
        query_keys,
        url_locations,
        attributes
    ):
        self.query_keys = query_keys,
        self.url_locations = url_locations,
        self.attributes = attributes

    def to_dict(self):
        return {
            'className' : 'QueryParameterHarvester',
            'params' : {
                'queryKeys' : self.query_keys,
                'urlLocations' : self.url_locations,
                'attributes' : self.attributes
            }
        }
