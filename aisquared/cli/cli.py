from aisquared.serving import deploy_model, get_remote_prediction
from mann.utils import get_custom_objects
import click
import json

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
