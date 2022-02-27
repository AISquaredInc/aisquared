from setuptools import setup
from aisquared import __version__

setup(
    name = 'aisquared',
    version = __version__,
    url = 'https://github.com/AISquaredInc/aisquared',
    packages = [
        'aisquared',
        'aisquared.base',
        'aisquared.remote',
        'aisquared.config',
        'aisquared.config.harvesting',
        'aisquared.config.preprocessing',
        'aisquared.config.analytic',
        'aisquared.config.postprocessing',
        'aisquared.config.rendering',
        'aisquared.config.feedback'
    ],
    author = 'The AI Squared Team',
    author_email = 'staff@squared.ai',
    description = 'Utilities for interacting with the AI Squared Technology Stack',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    license = 'AI Squared Developer License Agreement',
    license_files = 'LICENSE',
    install_requires = [
        'tensorflowjs',
        'boto3',
        'azure-storage-blob'
    ],
    classifiers = [
        'License :: Other/Proprietary License'
    ]
)
