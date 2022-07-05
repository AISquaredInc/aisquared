from aisquared.base import BaseObject, ALLOWED_STAGES
from aisquared.config.harvesting import ImageHarvester, TextHarvester, InputHarvester
from aisquared.config.preprocessing.tabular import TabularPreprocessor
from aisquared.config.preprocessing.image import ImagePreprocessor
from aisquared.config.preprocessing.text import TextPreprocessor
from aisquared.config.analytic import DeployedAnalytic, DeployedModel, LocalModel, LocalAnalytic
from aisquared.config.postprocessing import BinaryClassification, MulticlassClassification, ObjectDetection, Regression
from aisquared.config.rendering import ImageRendering, ObjectRendering, DocumentRendering, WordRendering, FilterRendering
from aisquared.config.feedback import SimpleFeedback, BinaryFeedback, MulticlassFeedback, RegressionFeedback, ModelFeedback, QualitativeFeedback

import tensorflowjs as tfjs
import tensorflow as tf
import shutil
import json
import os

HARVESTING_CLASSES = (
    ImageHarvester,
    TextHarvester,
    InputHarvester
)

PREPROCESSING_CLASSES = (
    TabularPreprocessor,
    ImagePreprocessor,
    TextPreprocessor
)

ANALYTIC_CLASSES = (
    DeployedAnalytic,
    DeployedModel,
    LocalModel,
    LocalAnalytic
)

POSTPROCESSING_CLASSES = (
    BinaryClassification,
    MulticlassClassification,
    ObjectDetection,
    Regression
)

RENDERING_CLASSES = (
    ObjectRendering,
    ImageRendering,
    DocumentRendering,
    WordRendering,
    FilterRendering
)

FEEDBACK_CLASSES = (
    ModelFeedback,
    SimpleFeedback,
    BinaryFeedback,
    MulticlassFeedback,
    RegressionFeedback,
    QualitativeFeedback
)

LOCAL_CLASSES = (
    LocalModel,
    LocalAnalytic
)


class ModelConfiguration(BaseObject):
    """
    Configuration object for deploying a model or analytic
    """

    def __init__(
            self,
            name,
            harvesting_steps,
            preprocessing_steps,
            analytic,
            postprocessing_steps,
            rendering_steps,
            feedback_steps=None,
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
        harvesting_steps : None, Harvesting object or list of Harvesting objects
            Harvesters to use with the analytic
        preprocessing_steps : Preprocessing object or list of Preprocessing objects or None
            Preprocessers to use
        analytic : Analytic object or list of Analytic objects
            Analytics to use
        postprocessing_steps : Postprocessing object or list of Postprocessing objects or None
            Postprocessers to use
        rendering_steps : Rendering object or list of Rendering objects or None
            Renderers to use
        feedback_steps : None, Feedback object or list of Feedback objects or None (default None)
            Feedback steps to use
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
        self.harvesting_steps = harvesting_steps
        self.preprocessing_steps = preprocessing_steps
        self.analytic = analytic
        self.postprocessing_steps = postprocessing_steps
        self.rendering_steps = rendering_steps
        self.stage = stage
        self.feedback_steps = feedback_steps
        self.version = version
        self.description = description
        self.mlflow_uri = mlflow_uri
        self.mlflow_user = mlflow_user
        self.mlflow_token = mlflow_token
        self.owner = owner
        self.url = url
        self.auto_run = auto_run

    # name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    # harvesting_steps
    @property
    def harvesting_steps(self):
        return self._harvesting_steps

    @harvesting_steps.setter
    def harvesting_steps(self, value):
        harvesting_classes = HARVESTING_CLASSES + (ModelConfiguration,)
        if value is None:
            self._harvesting_steps = value
        elif isinstance(value, harvesting_classes):
            self._harvesting_steps = [value]
        elif isinstance(value, list) and all([isinstance(val, harvesting_classes) for val in value]):
            self._harvesting_steps = value
        elif isinstance(value, list) and all([isinstance(val, list) for val in value]) and all([isinstance(v, harvesting_classes) for val in value for v in val]):
            self._harvesting_steps = value
        else:
            raise ValueError(
                'harvesting_steps must be a None, single Harvester object, a list of Harvester objects, or a list of list of harvester objects')

    # preprocessing_steps
    @property
    def preprocessing_steps(self):
        return self._preprocessing_steps

    @preprocessing_steps.setter
    def preprocessing_steps(self, value):
        if value is None:
            self._preprocessing_steps = value
        elif isinstance(value, PREPROCESSING_CLASSES):
            self._preprocessing_steps = [value]
        elif isinstance(value, list) and all([isinstance(val, PREPROCESSING_CLASSES) for val in value]):
            self._preprocessing_steps = value
        elif isinstance(value, list) and all([isinstance(val, list) for val in value]) and all([isinstance(v, PREPROCESSING_CLASSES) for val in value for v in val]):
            self._preprocessing_steps = value
        elif value is None:
            self._preprocessing_steps = value
        else:
            raise ValueError(
                'preprocessing_steps must a single Preprocessor object, a list of Preprocessor objects, or a list of list of preprocessor objects')

    # analytic
    @property
    def analytic(self):
        return self._analytic

    @analytic.setter
    def analytic(self, value):
        if isinstance(value, ANALYTIC_CLASSES):
            self._analytic = [value]
        elif isinstance(value, list) and all([isinstance(val, ANALYTIC_CLASSES) for val in value]):
            self._analytic = value
        elif isinstance(value, list) and all([isinstance(val, list) for val in value]) and all([isinstance(v, ANALYTIC_CLASSES) for val in value for v in val]):
            self._analytic = value
        else:
            raise ValueError(
                'analytic must be a single Analytic object, a list of Analytic objects, or a list of list of Analtyic objects')

    # postprocessing_steps
    @property
    def postprocessing_steps(self):
        return self._postprocessing_steps

    @postprocessing_steps.setter
    def postprocessing_steps(self, value):
        if value is None:
            self._postprocessing_steps = value
        elif isinstance(value, POSTPROCESSING_CLASSES):
            self._postprocessing_steps = [value]
        elif isinstance(value, list) and all([isinstance(val, POSTPROCESSING_CLASSES) for val in value]):
            self._postprocessing_steps = value
        elif isinstance(value, list) and all([isinstance(val, list) for val in value]) and all([isinstance(v, POSTPROCESSING_CLASSES) for val in value for v in val]):
            self._postprocessing_steps = value
        elif value is None:
            self._postprocessing_steps = value
        else:
            raise ValueError(
                'postprocessing_steps must be a single Postprocessing object, a list of Postprocessing objects, or a list of list of Postprocessing objects')

    # rendering_steps
    @property
    def rendering_steps(self):
        return self._rendering_steps

    @rendering_steps.setter
    def rendering_steps(self, value):
        if isinstance(value, RENDERING_CLASSES) or value is None:
            self._rendering_steps = [value]
        elif isinstance(value, list) and all([isinstance(val, RENDERING_CLASSES) for val in value]):
            self._rendering_steps = value
        elif isinstance(value, list) and all([isinstance(val, list) for val in value]) and all([isinstance(v, RENDERING_CLASSES) for val in value for v in val]):
            self._rendering_steps = value
        else:
            raise ValueError(
                'rendering_steps must be a single Rendering object, a list of Rendering objects, a list of list of Rendering objects, or None')

    # feedback_steps
    @property
    def feedback_steps(self):
        return self._feedback_steps

    @feedback_steps.setter
    def feedback_steps(self, value):
        if value is None:
            self._feedback_steps = value
        elif isinstance(value, FEEDBACK_CLASSES):
            self._feedback_steps = [value]
        elif isinstance(value, list) and all([isinstance(val, FEEDBACK_CLASSES) for val in value]):
            self._feedback_steps = value
        elif isinstance(value, list) and all([isinstance(val, list) for val in value]) and all([isinstance(v, FEEDBACK_CLASSES) for val in value for v in val]):
            self._feedback_steps = value
        else:
            raise ValueError(
                'feedback_steps must be a single Feedback object, a list of Feedback objects, a list of list of Feedback objects, or None')

    # stage
    @property
    def stage(self):
        return self._stage

    @stage.setter
    def stage(self, value):
        if value not in ALLOWED_STAGES:
            raise ValueError(f'stage must be one of {ALLOWED_STAGES}')
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
        if not isinstance(value, str) and value is not None:
            raise ValueError('owner must be a string or None')
        self._owner = value

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

    # harvester_dict
    @property
    def harvester_dict(self):
        harvesting_classes = HARVESTING_CLASSES + (ModelConfiguration,)
        if self.harvesting_steps is None:
            return None
        elif isinstance(self.harvesting_steps, list) and all([isinstance(val, harvesting_classes) for val in self.harvesting_steps]):
            return [val.to_dict() for val in self.harvesting_steps]
        else:
            return [
                [v.to_dict() for v in val] for val in self.harvesting_steps
            ]

    # preprocessing_dict
    @property
    def preprocesser_dict(self):
        if self.preprocessing_steps is None:
            return self.preprocessing_steps
        elif isinstance(self.preprocessing_steps, list) and all([isinstance(val, PREPROCESSING_CLASSES) for val in self.preprocessing_steps]):
            return [val.to_dict() for val in self.preprocessing_steps]
        else:
            return [
                [v.to_dict() for v in val] for val in self.preprocessing_steps
            ]

    # analytic dict
    @property
    def analytic_dict(self):
        if isinstance(self.analytic, list) and all([isinstance(val, ANALYTIC_CLASSES) for val in self.analytic]):
            return [val.to_dict() for val in self.analytic]
        else:
            return [
                [v.to_dict() for v in val] for val in self.analytic
            ]

    # postprocesser_dict
    @property
    def postprocesser_dict(self):
        if self.postprocessing_steps is None:
            return self.postprocessing_steps
        elif isinstance(self.postprocessing_steps, list) and all([isinstance(val, POSTPROCESSING_CLASSES) for val in self.postprocessing_steps]):
            return [val.to_dict() for val in self.postprocessing_steps]
        else:
            return [
                [v.to_dict() for v in val] for val in self.postprocessing_steps
            ]

    # render_dict
    @property
    def render_dict(self):
        if self.rendering_steps[0] is None:
            return []
        elif isinstance(self.rendering_steps, list) and all([isinstance(val, RENDERING_CLASSES) for val in self.rendering_steps]):
            return [val.to_dict() for val in self.rendering_steps]
        else:
            return [
                [v.to_dict() for v in val] for val in self.rendering_steps
            ]

    # feedback_dict
    @property
    def feedback_dict(self):
        if self.feedback_steps is None:
            return self.feedback_steps
        elif isinstance(self.feedback_steps, list) and all([isinstance(val, FEEDBACK_CLASSES) for val in self.feedback_steps]):
            return [val.to_dict() for val in self.feedback_steps]
        else:
            return [
                [v.to_dict() for v in val] for val in self.feedback_steps
            ]

    def get_model_filenames(self):
        """
        Get filenames for all models in the configuration
        """
        filenames = []
        if isinstance(self.harvesting_steps[0], list):
            harvesting_list = [
                h for harvester in self.harvesting_steps for h in harvester]
        else:
            harvesting_list = self.harvesting_steps
        for harvester in harvesting_list:
            if isinstance(harvester, ModelConfiguration):
                filenames.extend(harvester.get_model_filenames())

        if isinstance(self.analytic[0], ANALYTIC_CLASSES):
            for a in self.analytic:
                if isinstance(a, LOCAL_CLASSES):
                    filenames.append(a.path)
        else:
            for analytic in self.analytic:
                for a in analytic:
                    if isinstance(a, LOCAL_CLASSES):
                        filenames.append(a.path)
        return filenames

    def to_dict(self):
        """
        Get the object as a dictionary
        """
        return {
            'className': 'ModelConfiguration',
            'params': {
                'name': self.name,
                'harvestingSteps': self.harvester_dict,
                'preprocessingSteps': self.preprocesser_dict,
                'analytics': self.analytic_dict,
                'postprocessingSteps': self.postprocesser_dict,
                'renderingSteps': self.render_dict,
                'feedbackSteps': self.feedback_dict,
                'stage': self.stage,
                'version': self.version,
                'description': self.description,
                'mlflowUri': self.mlflow_uri,
                'mlflowUser': self.mlflow_user,
                'mlflowToken': self.mlflow_token,
                'owner': self.owner,
                'url': self.url,
                'autoRun': self.auto_run
            }
        }

    def compile(self, filename=None, dtype=None):
        """
        Compile the object into a '.air' file, which can then be dragged and
        dropped into applications using the AI Squared JavaScript SDK

        Parameters
        ----------
        filename : path-like or None (default None)
            Filename to compile to. If None, defaults to '{NAME}.air', where {NAME} is the
            name of the analytic
        dtype : str or None (default None)
            The datatype to use for the model weights. If None, defaults to 'float32'
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
        filenames = self.get_model_filenames()
        if len(filenames) != 0:
            for f in filenames:
                if os.path.splitext(f)[-1] == '.h5':
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
