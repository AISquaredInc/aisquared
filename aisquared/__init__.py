"""
This package contains utilities to interact with the AI Squared technology stack, particularly with developing and deploying models to the AI Squared Browser Extension or other applications developed through the AI Squared JavaScript SDK.
"""

__version__ = '0.3.12'
__dev__ = True

import aisquared.config
import aisquared.base
import aisquared.platform

try:
    import aisquared.logging
    import aisquared.serving
    import aisquared.utils
    import llmlink
except ImportError:
    pass
