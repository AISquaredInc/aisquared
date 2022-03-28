from .BaseObject import BaseObject
from .rendering import LOCATIONS, COLORS, BADGES, WORD_LISTS
from .ImagePredictor import ImagePredictor
from .DocumentPredictor import DocumentPredictor
ALLOWED_STAGES = [
    'experimental',
    'staging',
    'production'
]