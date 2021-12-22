import json

class MulticlassClassification:
    """
    Postprocessing configuration object for multiclass classification
    """
    def __init__(
            self,
            label_map,
            keywords = None,
            documents = None
    ):
        """
        Parameters
        ----------
        label_map : list
            A list of values to map the output of the model to
        keywords : list of list of strings or None (default None)
            List of list of keywords corresponding to the top keywords for every class
        documents : list of list of strings or None (default None)
            List of list of document URLs corresponding to the top documents for every class
        """
        self.label_map = label_map
        self.keywords = keywords
        self.documents = documents

    @property
    def label_map(self):
        return self._label_map
    @label_map.setter
    def label_map(self, value):
        if not isinstance(value, list):
            raise ValueError('label_map must be a list')
        if len(value) <= 2:
            raise ValueError('For multiclass classification, the label map must have more than two values. If there are only two values, use the `BinaryClassification` class')
        self._label_map = value

    @property
    def keywords(self):
        return self._keywords
    @keywords.setter
    def keywords(self, value):
        if value is not None:
            if not isinstance(value, list) or not all([isinstance(val, list) for val in value]) or not all([isinstance(v, str) for val in value for v in val]):
                raise TypeError('keywords should be list of list of str')
            if len(value) != len(self.label_map):
                raise ValueError('Length of keywords should be the same as number of classes')
        self._keywords = value

    @property
    def documents(self):
        return self._documents
    @documents.setter
    def documents(self, value):
        if value is not None:
            if not isinstance(value, list) or not all([isinstance(val, list) for val in value]) or not all([isinstance(v, str) for val in value for v in val]):
                raise TypeError('documents should be list of list of str')
            if len(value) != len(self.label_map):
                raise ValueError('Length of documents should be the same as number of classes')
        self._documents = value
        
    def to_dict(self):
        """
        Get the configuration object as a dictionary
        """
        return {
            'className' : 'MulticlassClassification',
            'params' : {
                'labelMap' : self.label_map,
                'keywords' : self.keywords,
                'documents' : self.documents
            }
        }

    def to_json(self):
        """
        Get the configuration object as a JSON string
        """
        return json.dumps(self.to_dict())
        
