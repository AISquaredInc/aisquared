"""
The aisquared.base package contains both some basic objects that are used across the aisquared package backend and some objects which are designed to facilitate simple use cases of the technology.
"""

from .BaseObject import BaseObject
from .CustomObject import CustomObject
from .rendering import LOCATIONS, COLORS, BADGES, WORD_LISTS, QUALIFIERS, POSITIONS, STATIC_POSITIONS
from .stages import ALLOWED_STAGES
from .harvesting import ALLOWED_INPUT_TYPES, ALLOWED_HOWS
from .preprocessing import ALLOWED_PADS
