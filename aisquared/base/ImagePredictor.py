from aisquared.config.harvesting import ImageHarvester
from aisquared.config.preprocessing import ImagePreprocessor, Resize, ConvertToColor, DivideValue
from aisquared.config.analytic import LocalModel
from aisquared.config.postprocessing import BinaryClassification, MulticlassClassification, Regression
from aisquared.config.rendering import ImageRendering
from aisquared.base import COLORS

import aisquared.config.ModelConfiguration

class ImagePredictor():

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
        f"""
        Parameters
        ----------
        model_path : str or file-like
            The path to the model on local disk
        name : str
            The name of the model
        image_size : list of ints or None (default None)
            The size to reshape images to
        divide_value : int or float (default 1)
            The value to divide all pixel values by
        color : str (default 'RGB')
            Either 'RGB' or 'B+W', the color scheme to convert all images to
        task_type : str (default 'classification')
            Either 'classification' or 'regression', corresponding to the type of model
        label_map : list or None (default None)
            Label map for classification use cases
        min_value : float or None (default None)
            Value to map 0 to in regression use cases
        max_value : float or None (default None)
            Value to map 1 to in regression use cases
        include_probability : bool (default False)
            Whether to include predicted probability in classification use cases
        box_color : str (default {COLORS[-1]})
            The color to make the box around images
        font_color : str (default {COLORS[-4]})
            The font color to use
        version : int or None (default None)
            The version of the analytic
        description : str (default '')
            Description of the analytic
        mlflow_uri : str or None (default None)
            The MLFlow URI to use
        mlflow_user : str or None (default None)
            The MLFlow user to use
        mlflow_token : str or None (default None)
            The MLFlow token to use
        """
        
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
        analytic = LocalModel(model_path, input_type = 'cv')

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

        # Init
        self.harvester = harvester
        self.preprocesser = preprocesser
        self.analytic = analytic
        self.postprocesser = postprocesser
        self.renderer = renderer
        self.name = name
        self.version = version
        self.description = description
        self.mlflow_uri = mlflow_uri
        self.mlflow_user = mlflow_user
        self.mlflow_token = mlflow_token

    def compile(self):
        aisquared.config.ModelConfiguration(
            self.name,
            self.harvester,
            self.preprocesser,
            self.analytic,
            self.postprocesser,
            self.renderer,
            self.version,
            self.description,
            self.mlflow_uri,
            self.mlflow_user,
            self.mlflow_token
        ).compile() 
