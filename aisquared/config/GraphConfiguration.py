from aisquared.base import BaseObject, CustomObject, ALLOWED_STAGES
import tensorflowjs as tfjs
import tensorflow as tf
import shutil
import json
import os

LOCAL_CLASSES = ['LocalModel', 'LocalAnalytic', 'CustomObject']


class GraphConfiguration(BaseObject):
    """
    Configuration object for deploying a set of processing steps and/or analytics as a dependency graph
    """

    def __init__(
            self,
            name,
            stage=ALLOWED_STAGES[0],
            version=None,
            description='',
            mlflow_uri=None,
            mlflow_user=None,
            mlflow_token=None,
            owner=None,
            url='*',
            auto_run=False
    ):
        """
        Parameters
        ----------
        name : str
            The name of the deployed analytic
        stage : str (default 'experimental')
            The stage of the model, from 'experimental', 'staging', 'production'
        version : str or None (default None)
            Version of the analytic
        description : str (default '')
            The description of the analytic
        mlflow_uri : str or None (default None)
            MLFlow URI to use, if applicable
        mlflow_user : str or None (default None)
            MLFlow user to use, if applicable
        mlflow_token : str or None (default None)
            MLFlow token to use, if applicable
        owner : str or None (default None)
            The owner of the model
        url : str (default '*')
            URL or URL pattern to match
        auto_run : bool (default False)
            Whether to automatically run this file when on a valid page
        """
        super().__init__()
        self.name = name
        self.stage = stage
        self.version = version
        self.description = description
        self.mlflow_uri = mlflow_uri
        self.mlflow_user = mlflow_user
        self.mlflow_token = mlflow_token
        self.owner = owner
        self.url = url
        self.auto_run = auto_run
        self.nodes = []

    # name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    # stage
    @property
    def stage(self):
        return self._stage

    @stage.setter
    def stage(self, value):
        if value not in ALLOWED_STAGES:
            raise ValueError(
                f'stage must be one of {ALLOWED_STAGES}, got {value}')
        self._stage = value

    # version
    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = str(value) if value is not None else value

    # description
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = str(value)

    # mlflow_uri
    @property
    def mlflow_uri(self):
        return self._mlflow_uri

    @mlflow_uri.setter
    def mlflow_uri(self, value):
        self._mlflow_uri = value

    # mlflow_user
    @property
    def mlflow_user(self):
        return self._mlflow_user

    @mlflow_user.setter
    def mlflow_user(self, value):
        self._mlflow_user = value

    # mlflow_token
    @property
    def mlflow_token(self):
        return self._mlflow_token

    @mlflow_token.setter
    def mlflow_token(self, value):
        self._mlflow_token = value

    # owner
    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        self._owner = str(value) if value is not None else value

    # url
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if not isinstance(value, str):
            raise ValueError('url must be string')
        self._url = value

    # auto_run
    @property
    def auto_run(self):
        return self._auto_run

    @auto_run.setter
    def auto_run(self, value):
        if not isinstance(value, bool):
            raise TypeError('auto_run must be Boolean valued')
        self._auto_run = value

    def add_node(self, step, dependencies=None):
        """
        Add a node to the configuration graph

        Parameters
        ----------
        step : aisquared configuration step
            The step to add
        dependencies : int, list of int, or None
            The ids of nodes which must be run before the
            added node

        Returns
        -------
        node_id : int
            The integer id of the node that is added
        """
        if not isinstance(step, BaseObject):
            raise TypeError(
                'Each node in the configuration graph should be an aisquared configuration step')
        if not (isinstance(dependencies, int) or dependencies is None):
            if not isinstance(dependencies, list) or not all([isinstance(dep, int) for dep in dependencies]):
                raise ValueError(
                    'dependencies must be integer or list of integers')

        id = len(self.nodes)
        self.nodes.append(
            {
                'id': id,
                'dependencies': dependencies,
                'step': step.to_dict()
            }
        )
        return id

    def get_filenames(self):
        """
        Get filenames for all models in the configuration
        """
        filenames = []
        for node in self.nodes:
            if node['step']['className'] in LOCAL_CLASSES:
                filenames.append(node['step']['params']['path'])
        return filenames

    def to_dict(self):
        """
        Get the object as a dictionary
        """
        return {
            'className': 'GraphConfiguration',
            'params': {
                'name': self.name,
                'stage': self.stage,
                'version': self.version,
                'description': self.description,
                'mlflowUri': self.mlflow_uri,
                'mlflowUser': self.mlflow_user,
                'mlflowToken': self.mlflow_token,
                'owner': self.owner,
                'url': self.url,
                'autoRun': self.auto_run
            },
            'nodes': self.nodes
        }

    def compile(self, filename=None, dtype=None):
        """
        Compile the object into a '.air' file, which can then be dragged and dropped into applications using the AI Squared JavaScript SDK

        Parameters
        ----------
        filename : path-like or None (default None)
            Filename to compile to. If None, defaults to '{NAME}.air', where {NAME} is the name of the analytic
        dtype : str or None (default None)
            The datatype to use for the model weights when using a Keras model. If None, defaults to 'float32'
        """
        if filename is None:
            filename = self.name + '.air'

        if dtype is None:
            dtype_map = None
        else:
            dtype_map = {dtype: '*'}

        dirname = os.path.join('.', os.path.splitext(filename)[0])

        # write the object as json config
        os.makedirs(dirname, exist_ok=True)
        with open(os.path.join(dirname, 'config.json'), 'w') as f:
            json.dump(self.to_dict(), f)

        # go through the files and copy them/make them tfjs files
        filenames = self.get_filenames()
        if len(filenames) != 0:
            for f in filenames:
                if os.path.splitext(f)[-1] == 'h5':
                    model = tf.keras.models.load_model(f)
                    model_dir = os.path.join(dirname, os.path.split(f)[-1])
                    tfjs.converters.save_keras_model(
                        model, model_dir, quantization_dtype_map=dtype_map)
                else:
                    shutil.copy(f, dirname)

        # go through the entire directory of dirname, grab all files, and make
        # the archive file
        shutil.make_archive(filename, 'zip', dirname)

        # Move the archive file to just have .air
        shutil.move(filename + '.zip', filename)

        # Remove the temp directory
        shutil.rmtree(dirname, ignore_errors=True)
