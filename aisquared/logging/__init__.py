"""
The aisquared.logging subpackage contains utilities for performing experiments within aisquared.

This functionality is inhereted from MLFlow. Please see the MFLow documentatation at https://mlflow.org.
"""

try:
    from mlflow import *
except ImportError:
    pass
