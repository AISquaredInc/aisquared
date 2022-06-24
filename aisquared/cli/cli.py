from aisquared.serving import deploy_model, get_remote_prediction
from aisquared.remote import AWSClient, AzureClient
from mann.utils import get_custom_objects
import click
import json

_ALLOWED_CLIENTS = ['aws', 'azure']

def _get_client(client_type):
    
    # Normalize the client type name
    client_type = client_type.lower()
    
    # Create the client
    if client_type == 'aws':
        client = AWSClient()
    elif client_type == 'azure':
        client = AzureClient()
    
    return client

@click.group()
@click.pass_context
def aisquared(context):
    pass

@aisquared.command('deploy')
@click.argument('saved-model', type = click.Path(exists = True, file_okay = True, dir_okay = False))
@click.argument('model-type', type = str)
@click.option('--host', '-h', type = str, default = '127.0.0.1')
@click.option('--port', '-p', type = int, default = 2244)
def deploy(saved_model, model_type, host, port):
    """
    Deploy a model to a local endpoint
    """
    deploy_model(
        saved_model,
        model_type,
        host,
        port,
        get_custom_objects()
    )

@aisquared.command('predict')
@click.argument('data', type = click.Path(exists = True, file_okay = True, dir_okay = True))
@click.option('--host', '-h', type = str, default = '127.0.0.1')
@click.option('--port', '-p', type = int, default = 2244)
@click.option('--outfile', '-o', default = None, type = click.Path(exists = False, file_okay = True, dir_okay = False))
def predict(data, host, port, outfile):
    """
    Get predictions from a deployed model
    """
    # Load the json
    with open(data, 'r') as f:
        data = json.load(f)
    
    # Get the predictions
    predictions = get_remote_prediction(
        data,
        host,
        port
    )

    # Either print the predictions or write to the outfile
    if not outfile:
        print(predictions)
    else:
        with open(outfile, 'w') as f:
            json.dump(predictions, f)

@aisquared.group()
def airfiles():
    """
    Utilities for listing, downloading, uploading, and deleting .air files
    """
    pass

@airfiles.command('list')
@click.argument('client-type', type = click.Choice(_ALLOWED_CLIENTS, case_sensitive = False))
@click.option('--bucket', '-b', type = str, default = None)
@click.option('--detailed/--no-detailed', default = False)
def list_models(client_type, bucket, detailed):
    """
    List .air files in a specific bucket or container
    """

    # Create the client
    client = _get_client(client_type)

    # Print out the response
    models = client.list_models(
        bucket,
        detailed = detailed
    )
    if not detailed:
        print('\n'.join(models))
    else:
        print(models)

@airfiles.command('delete')
@click.argument('client-type', type = click.Choice(_ALLOWED_CLIENTS, case_sensitive = False))
@click.argument('model-name', type = str)
@click.option('--bucket', '-b', type = str, default = None)
def delete(client_type, model_name, bucket):
    """
    Delete an .air file
    """

    # Create the client
    client = _get_client(client_type)

    # Delete the model
    client.delete_model(
        model_name,
        bucket
    )

@airfiles.command('download')
@click.argument('client-type', type = click.Choice(_ALLOWED_CLIENTS, case_sensitive = False))
@click.argument('model-name', type = str)
@click.option('--bucket', '-b', type = str, default = None)
def download(client_type, model_name, bucket):
    """
    Download an .air file
    """

    # Create the client
    client = _get_client(client_type)

    # Download the model
    client.download_model(
        model_name,
        bucket
    )

@airfiles.command('upload')
@click.argument('client-type', type = click.Choice(_ALLOWED_CLIENTS, case_sensitive = False))
@click.argument('model-path', type = click.Path(exists = True, file_okay = True, dir_okay = False))
@click.option('--bucket', '-b', type = str, default = None)
@click.option('--overwrite/--no-overwrite', default = False)
def upload(client_type, model_path, bucket, overwrite):
    """
    Upload an .air file
    """

    # Create the client
    client = _get_client(client_type)

    # Upload the model
    client.upload_model(
        model_path,
        bucket,
        overwrite
    )
