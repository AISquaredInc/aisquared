"""
The aisquared.base package contains both some basic objects that are used across the aisquared package backend and some objects which are designed to facilitate simple use cases of the technology.
"""

from .BaseObject import BaseObject
from .rendering import LOCATIONS, COLORS, BADGES, WORD_LISTS, QUALIFIERS, POSITIONS, STATIC_POSITIONS
from .stages import ALLOWED_STAGES
from .harvesting import ALLOWED_INPUT_TYPES, ALLOWED_HOWS
from .preprocessing import ALLOWED_PADS
from .css import DEFAULT_CONTAINER_RENDERING_CSS, DEFAULT_HTML_TAG_RENDERING_CSS, DEFAULT_TABLE_RENDERING_CSS, TABLE_RENDERING_CSS_FILE, HTML_TAG_RENDERING_CSS_FILE, CONTAINER_RENDERING_CSS_FILE, DEFAULT_CHART_RENDERING_CSS, CHART_RENDERING_CSS_FILE, DIRECTORY
from .platform import CLIENT_CONFIG_FILE
from .endpoints import ENDPOINTS

from aisquared.config.harvesting import ImageHarvester, TextHarvester, InputHarvester, QueryParameterHarvester, ChatbotHarvester
from aisquared.config.preprocessing.tabular import TabularPreprocesser
from aisquared.config.preprocessing.image import ImagePreprocesser
from aisquared.config.preprocessing.text import TextPreprocesser
from aisquared.config.analytic import DeployedAnalytic, DeployedModel, LocalModel, LocalAnalytic, ReverseMLWorkflow, OnnxModel
from aisquared.config.postprocessing import BinaryClassification, MulticlassClassification, ObjectDetection, Regression
from aisquared.config.rendering import ImageRendering, ObjectRendering, DocumentRendering, WordRendering, FilterRendering, ContainerRendering, HTMLTagRendering, DoughnutChartRendering, TableRendering, BarChartRendering, LineChartRendering, DashboardReplacementRendering, PieChartRendering, SOSRendering, TextRendering, CustomRendering, ChatRendering  # , DashboardRendering
from aisquared.config.feedback import SimpleFeedback, BinaryFeedback, MulticlassFeedback, RegressionFeedback, ModelFeedback, QualitativeFeedback
from aisquared.config.CustomObject import CustomObject

HARVESTING_CLASSES = (
    ImageHarvester,
    TextHarvester,
    InputHarvester,
    QueryParameterHarvester,
    ChatbotHarvester,
    CustomObject
)

PREPROCESSING_CLASSES = (
    TabularPreprocesser,
    ImagePreprocesser,
    TextPreprocesser,
    CustomObject
)

ANALYTIC_CLASSES = (
    DeployedAnalytic,
    DeployedModel,
    LocalModel,
    LocalAnalytic,
    ReverseMLWorkflow,
    OnnxModel,
    CustomObject
)

POSTPROCESSING_CLASSES = (
    BinaryClassification,
    MulticlassClassification,
    ObjectDetection,
    Regression,
    CustomObject
)

RENDERING_CLASSES = (
    ObjectRendering,
    ImageRendering,
    DocumentRendering,
    WordRendering,
    FilterRendering,
    ContainerRendering,
    HTMLTagRendering,
    DoughnutChartRendering,
    TableRendering,
    BarChartRendering,
    LineChartRendering,
    DashboardReplacementRendering,
    PieChartRendering,
    SOSRendering,
    TextRendering,
    CustomRendering,
    CustomObject,
    ChatRendering
    # DashboardRendering
)

FEEDBACK_CLASSES = (
    ModelFeedback,
    SimpleFeedback,
    BinaryFeedback,
    MulticlassFeedback,
    RegressionFeedback,
    QualitativeFeedback,
    CustomObject
)

LOCAL_CLASSES = (
    LocalModel,
    LocalAnalytic,
    OnnxModel,
    CustomObject
)
