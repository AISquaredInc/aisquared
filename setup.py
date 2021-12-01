from setuptools import setup
from aisquared import __version__

with open('requirements.txt', 'r') as f:
    install_requires = [line for line in f.read().splitlines() if len(line) > 0]

setup(
    name = 'aisquared',
    version = __version__,
    url = 'https://github.com/AISquaredInc/aisquared',
    packages = ['aisquared', 'aisquared.preprocessing', 'aisquared.postprocessing'],
    author = 'The AI Squared Team',
    author_email = 'jacob.renn@squared.ai',
    descritption = 'Utilities for interacting with the AI Squared Technology Stack',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    install_requires = install_requires
)
