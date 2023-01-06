from setuptools import setup
from aisquared import __version__

with open('requirements.txt', 'r') as f:
    requirements = [line for line in f.read().splitlines() if line != '']
with open('additional_requirements.txt', 'r') as f:
    additional_requirements = [
        line for line in f.read().splitlines() if line != '']

setup(
    name='aisquared',
    version=__version__,
    url='https://github.com/AISquaredInc/aisquared',
    packages=[
        'aisquared',
        'aisquared.base',
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
        'aisquared.config.feedback',
        'aisquared.utils',
        'aisquared.platform'
    ],
    author='The AI Squared Team',
    author_email='staff@squared.ai',
    description='Utilities for interacting with the AI Squared Technology Stack',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='AI Squared Developer License Agreement',
    license_files='LICENSE',
    install_requires=requirements,
    extras_require={'full': additional_requirements},
    classifiers=[
        'License :: Other/Proprietary License'
    ]
)
