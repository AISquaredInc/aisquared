from aisquared.config.harvesting import TextHarvester
from aisquared.config.preprocessing import TextPreprocessor, Tokenize, RemoveCharacters, ConvertToCase, ConvertToVocabulary, PadSequences
from aisquared.config.analytic import LocalModel
from aisquared.config.postprocessing import BinaryClassification, MulticlassClassification, Regression
from aisquared.config.rendering import DocumentRendering
from aisquared.base import COLORS

import aisquared.config.ModelConfiguration

class DocumentPredictor():

    def __init__(
        self,
        model_path,
        vocabulary,
        sequence_length,
        name,
        task_type = 'classification',
        prediction_key = 'className',
        label_map = None,
        min_value = None,
        max_value = None,
        include_probability = False,
        probability_key = 'probability',
        tokenize_words = True,
        tokenize_sentences = False,
        remove_digits = True,
        remove_punctuation = True,
        lowercase = True,
        uppercase = False,
        start_character = 1,
        oov_character = 2,
        max_vocab = None,
        pad_character = 0,
        pad_location = 'post',
        truncate_location = 'post',
        words = None,
        documents = None,
        underline_color = COLORS[-1],
        version = None,
        description = '',
        mlflow_uri = None,
        mlflow_user = None,
        mlflow_token = None
    ):

        # Harvester
        harvester = TextHarvester()
        
        # Preprocesser
        steps = []
        if remove_digits or remove_punctuation:
            steps.append(RemoveCharacters(remove_digits, remove_punctuation))
        if lowercase or uppercase:
            steps.append(ConvertToCase(lowercase))
        if tokenize_words or tokenize_sentences:
            steps.append(Tokenize(tokenize_sentences, tokenize_words))
        steps.append(ConvertToVocabulary(vocabulary, start_character, oov_character, max_vocab))
        steps.append(PadSequences(pad_character, sequence_length, pad_location, truncate_location))
        preprocesser = TextPreprocessor(steps)

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
        renderer = DocumentRendering(
            prediction_key,
            words,
            documents,
            include_probability,
            probability_key,
            underline_color
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
