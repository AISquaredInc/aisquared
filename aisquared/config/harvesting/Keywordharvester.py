from aisquared.base import BaseObject


class KeywordHarvester(BaseObject):

    def __init__(self, keywords, case_sensitive=False):
        super().__init__()
        self.keywords = keywords
        self.case_sensitive = case_sensitive

    def to_dict(self):
        return {
            'className': 'KeywordHarvester',
            'params': {
                'keywords': self.keywords,
                'caseSensitive': self.case_sensitive
            }
        }
