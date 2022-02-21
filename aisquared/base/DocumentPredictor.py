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
        f"""
        Parameters
        ----------
        model_path : str or file-like
            The path to the model on local disk
        vocabulary : dict
            Dictionary of token : integer pairs
        sequence_length : int
            Sequence length to use
        name : str
            The name of the model
        task_type : str (default 'classification')
            Either 'classification' or 'regression', corresponding to the type of model
        prediction_key : str (default 'className')
            The prediction key to retrieve
        label_map : list or None (default None)
            Label map for classification use cases
        min_value : float or None (default None)
            Value to map 0 to in regression use cases
        max_value : float or None (default None)
            Value to map 1 to in regression use cases
        include_probability : bool (default False)
            Whether to include predicted probability in classification use cases
        probability_key : str (default 'probability')
            Key to use to retrieve probabilities
        tokenize_words : bool (default True)
            Whether to tokenize words
        tokenize_sentences : bool (default False)
            Whether to tokenize sentences
        remove_digits : bool (default True)
            Whether to remove digits from text
        remove_punctuation : bool (default True)
            Whether to remove punctuation from text
        lowercase : bool (default True)
            Whether to lowercase all text
        uppercase : bool (default False)
            Whether to uppercase all text
        start_character : int (default 1)
            The character to use to mark the beginning of text
        oov_character : int (default 2)
            The character to use to mark unrecognized vocabulary
        max_vocab : int or None (default None)
            Maximum vocabulary integer to use. If None, all vocabulary is used
        pad_character : int (default 0)
            Character to use for padding
        pad_location : str (default 'post')
            Where to apply padding
        truncate_location : str (default 'post')
            Where to apply truncation
        words : list or None (default None)
            List of words or list of list of words to highlihgt when rendering
        documents : list or None (default None)
            List of document URLs or list of list of document URLs to recommend when rendering
        underline_color : str (default {COLORS[-1]})
            Color to use when underlining words
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
        analytic = LocalModel(model_path, input_type = 'text')

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
        """
        Compile the configuration to a .air file
        """
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
