from setuptools import setup
from aisquared import __version__

setup(
    name = 'aisquared',
    version = __version__,
    url = 'https://github.com/AISquaredInc/aisquared',
    packages = [
        'aisquared',
        'aisquared.cli',
        'aisquared.base',
        'aisquared.remote',
        'aisquared.config',
        'aisquared.logging',
        'aisquared.serving',
        'aisquared.config.harvesting',
        'aisquared.config.preprocessing',
        'aisquared.config.preprocessing.text',
        'aisquared.config.preprocessing.image',
        'aisquared.config.preprocessing.tabular',
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
        'mlflow',
        'boto3',
        'azure-storage-blob',
        'flask',
        'waitress',
        'click',
        'numpy',
        'tensorflow',
        'mann',
        'scikit-learn'
    ],
    classifiers = [
        'License :: Other/Proprietary License'
    ],
    entry_points = {
        'console_scripts' : [
            'aisquared = aisquared.cli.cli:aisquared'
        ]
    }
)
