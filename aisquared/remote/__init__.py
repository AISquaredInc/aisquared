"""
The aisquared.remote package contains utilities for interacting with .air files stored in cloud
storage resources, specifically AWS S3 and Azure Blob Store
"""

from .aws import AWSClient
from .azure import AzureClient
