from setuptools import setup
from aisquared import __version__

setup(
    name = 'aisquared',
    version = __version__,
    url = 'https://github.com/AISquaredInc/aisquared',
    packages = ['aisquared', 'aisquared.config', 'aisquared.config.preprocessing', 'aisquared.config.postprocessing'],
    author = 'The AI Squared Team',
    author_email = 'staff@squared.ai',
    descritption = 'Utilities for interacting with the AI Squared Technology Stack',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    license = 'AI Squared Developer License Agreement',
    license_files = 'LICENSE',
    install_requires = [
        'tensorflowjs'
    ],
    classifiers = [
        'License :: Other/Proprietary License'
    ]
)
