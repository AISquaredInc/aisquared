from aisquared.config import ModelConfiguration
from aisquared.config.harvesting import ImageHarvester
from aisquared.config.preprocessing import ImagePreprocessor, Resize, ConvertToColor, DivideValue
from aisquared.config.analytic import LocalModel
from aisquared.config.postprocessing import BinaryClassification, MulticlassClassification, Regression
from aisquared.config.rendering import ImageRendering
from aisquared.base import COLORS, LOCATIONS

class ImagePredictor(ModelConfiguration):

    def __init__(
        self,
        model_path,
        name,
        image_size = None,
        divide_value = 1,
        color = 'RGB',
        task_type = 'classification',
        label_map = None,
        min_value = None,
        max_value = None,
        include_probability = False,
        box_color = COLORS[-1],
        font_color = COLORS[-4],
        version = None,
        description = '',
        mlflow_uri = None,
        mlflow_user = None,
        mlflow_token = None
    ):
        
        # Harvester
        harvester = ImageHarvester()
        
        # Preprocesser
        steps = []
        if image_size is not None:
            steps.append(
                Resize(image_size)
            )
        steps.append(DivideValue(divide_value))
        steps.append(ConvertToColor(color))
        
        preprocesser = ImagePreprocessor(steps)

        # Model
        analytic = LocalModel(model_path)

        # Postprocessing
        if task_type == 'classification':
            if label_map is None:
                raise ValueError('If classification is specified, label_map must be provided')
            if len(label_map) == 2:
                postprocesser = BinaryClassification(label_map)
            else:
                postprocesser = MulticlassClassification(label_map)
        elif task_type == 'regression':
            if min_value is None or max_value is None:
                raise ValueError('If regression is specified, min_value and max_value must also be specified')
            postprocesser = Regression(min_value, max_value)

        # Rendering
        renderer = ImageRendering(
            color = box_color,
            include_probability = include_probability,
            font_color = font_color
        )

        # Super init
        super().__init__(
            name,
            harvester,
            preprocesser,
            analytic,
            postprocesser,
            renderer,
            version,
            description,
            mlflow_uri,
            mlflow_user,
            mlflow_token
        )
