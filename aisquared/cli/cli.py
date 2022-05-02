from aisquared.serving import deploy_model
from mann.utils import get_custom_objects
import click

@click.group()
@click.pass_context
def aisquared(context):
    pass

@aisquared.command('deploy')
@click.argument('saved-model', type = click.Path(exists = True, file_okay = True, dir_okay = True))
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