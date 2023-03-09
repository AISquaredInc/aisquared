"""
The aisquared.base package contains both some basic objects that are used across the aisquared package backend and some objects which are designed to facilitate simple use cases of the technology.
"""

from .BaseObject import BaseObject
from .rendering import LOCATIONS, COLORS, BADGES, WORD_LISTS, QUALIFIERS, POSITIONS, STATIC_POSITIONS
from .stages import ALLOWED_STAGES
from .harvesting import ALLOWED_INPUT_TYPES, ALLOWED_HOWS
from .preprocessing import ALLOWED_PADS
from .css import DEFAULT_CONTAINER_RENDERING_CSS, DEFAULT_HTML_TAG_RENDERING_CSS, DEFAULT_TABLE_RENDERING_CSS, TABLE_RENDERING_CSS_FILE, HTML_TAG_RENDERING_CSS_FILE, CONTAINER_RENDERING_CSS_FILE, DIRECTORY
from .platform import CLIENT_CONFIG_FILE
from .endpoints import ENDPOINTS
