# AISquared

This package contains utilities to interact with the AI Squared technology stack, particularly with developing and deploying models to the AI Squared Browser Extension or other applications developed through the AI Squared JavaScript SDK.

## Installation

This package is available through [Pypi](https://pypi.org) and can be installed by running the following command:

```bash
pip install aisquared
```

Alternatively, the latest version of the software can be installed directly from GitHub using the following command

```bash
pip install git+https://github.com/AISquaredInc/aisquared
```

## Capabilities

This package is currently in a state of constant development, so it is likely that breaking changes can be made at any time.  We will work diligently to document changes and make stable releases in the future.

The `aisquared` package currently contains one subpackage, the `aisquared.config` package. This package holds objects for building the configuration files that need to be included with converted model files for use within the AI Squared Extension. The contents of the config subpackage contain both pre- and postprocessing steps as well as rendering objects to use with the model. The following will explain the functionality of the config package:

### Config

The `aisquared.config` subpackage contains the following objects:

- `ModelConfiguration`
  - The `ModelConfiguration` object is the final object to be used to create the configuration file. It takes as input a list of preprocessing steps, a list of postprocessing steps, a list of input shapes for all inputs within the model, an optional MLFlow URI, an optional MLFlow user, and an optional MLFlow token
- `ImagePreprocessor`
  - The `ImagePreprocessor` class takes in preprocessing steps (defined below) which define preprocessing steps for images.
- `TabularPreprocessor`
  - The `TabularPreprocessor` class takes in preprocessing steps (defined below) which define preprocessing steps for tabular data.
- `TextPreprocessor`
  - The `TextPreprocessor` class takes in preprocessing steps (defined below) which define preprocessing steps for text data.
- `Regression`
  - The `Regression` object is a postprocessing class for models which perform regression. Since it is common to train regression models by scaling regression outputs to values between 0 and 1, this class is designed to convert output values between 0 and 1 to their original values, corresponding to `min` and `max` when the class is instantiated.
- `BinaryClassification`
  - The `BinaryClassification` object is a postprocessing class for models which perform binary classification. The class is instantiated with a label map and a cutoff value used to identify when the positive class (class 1) is identified.
- `MulticlassClassification`
  - The `MulticlassClassification` object is a postprocessing class for models which perform multiclass classification. The class is instantiated with a label map only.
- `ObjectDetection`
  - The `ObjectDetection` object is a postprocessing class for models which perform object detection. The class is instantiated with a label map and a cutoff value for identification.
- `ImageRendering`
  - The `ImageRendering` object is a rendering class for rendering single predictions on images.
- `ObjectRendering`
  - The `ObjectRendering` object is a rendering class for rendering object detection predictions on images.
- `WordRendering`
  - The `WordRendering` object is a rendering class for rendering highlights, underlines, or badges on individual words.
- `PopOutNLPRendering`
  - The `PopOutNLPRendering` object is a rendering class for rendering document predictions.

### Preprocessing Steps

The `aisquared.config.preprocessing` subpackage contains `PreProcStep` objects, which are then fed into the `ImagePreprocessor`, `TabularPreprocessor`, and `TextPreprocessor` classes. The `PreProcStep` classes are:

- `ZScore`
  - This class configures standard normalization procedures for tabular data
- `MinMax`
  - This class configures Min-Max scaling procedures for tabular data
- `OneHot`
  - This class configures One Hot encoding for columns of tabular data
- `AddValue`
  - This class configures adding values to pixels in image data
- `SubtractValue`
  - This class configures subtracting values to pixels in image data
- `MultiplyValue`
  - This class configures multiplying pixel values by a value in image data
- `DivideValue`
  - This class configures dividing pixel values by a value in image data
- `ConvertToColor`
  - This class configures converting images to the specified color scheme
- `Resize`
  - This class configures image resize procedures
- `Tokenize`
  - This class configures how text will be tokenized
- `RemoveCharacters`
  - This class configures which characters should be removed from text
- `ConvertToCase`
  - This class configures which case - upper or lower - text should be converted to
- `ConvertToVocabulary`
  - This class configures how text tokens should be converted to vocabulary integers
- `PadSequences`
  - This class configures how padding should occur given a sequence of text tokens converted to a sequence of integers

These step objects can then be placed within the `TabularPreprocessor`, `ImagePreprocessor`, or `TextPreprocessor` objects. For the `TabularPreprocessor`, the `ZScore`, `MinMax`, and `OneHot` Steps are supported. For the `ImagePreprocessor`, the `AddValue`, `SubtractValue`, `MultiplyValue`, `DivideValue`, `ConvertToColor`, and `Resize` Steps are supported. For the `TextPreprocessor`, the `Tokenize`, `RemoveCharacters`, `ConvertToCase`, `ConvertToVocabulary`, and `PadSequences` Steps are supported

### Final Configuration and Model Creation

Once preprocessing, postprocessing, and rendering objects have been created, these objects can then be passed to the `aisquared.config.ModelConfiguration` class. This class utilizes the objects passed to it to build the entire model configuration automatically.

Finally, the `aisquared.create_air_model` takes in a `ModelConfiguration` class and an existing Keras model to create a model file compatible with the AI Squared extension and with the `.air` file extension.
