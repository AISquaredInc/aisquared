from distutils.core import setup
from aisquared import __version__

setup(
    name = 'aisquared',
    version = __version__,
    packages = ['aisquared', 'aisquared.preprocessing', 'aisquared.postprocessing'],
    author = 'Jacob Renn',
    author_email = 'jacob.renn@squared.ai',
    descritption = 'Utilities for interacting with the AI Squared Technology Stack',
    long_description = open('README.md').read()
)
