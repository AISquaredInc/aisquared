# AISquared

This package contains utilities to interact with the AI Squared technology stack, particularly with developing and deploying models to the AI Squared Browser Extension.

## Installation

This package is not (yet) available through [Pypi](https://pypi.org), though that is on the development roadmap. For the time being, installation requires downloading and installing the source code directly, which can be done using the following commands

```bash
# clone the repository and cd into it
git clone https://github.com/AISquaredInc/aisquared
cd aisquared

# install the package
pip install .
```

Alternatively, the latest version of the software can be installed directly from GitHub using the following command

```bash
pip install git+https://github.com/AISquaredInc/aisquared
```

## Capabilities

This package is currently in a state of constant development, so it is very likely that breaking changes will be made often. We will work to create stable releases in the future.

The `aisquared` package currently contains one subpackage, the `aisquared.config` package. This package holds objects for building the configuration files that need to be included with converted model files for use within the AI Squared Extension. The contents of the config subpackage contain both pre- and postprocessing steps to use with the model. The following will explain the functionality of the config package:

### Config

The `aisquared.config` subpackage contains the following objects:

- `ModelConfiguration`
  - The `ModelConfiguration` object is the final object to be used to create the configuration file. It takes as input a list of preprocessing steps, a list of postprocessing steps, a list of input shapes for all inputs within the model, an optional MLFlow URI, an optional MLFlow user, and an optional MLFlow token
- `ImagePreprocessor`
  - The `ImagePreprocessor` class takes in preprocessing steps (defined below) which define preprocessing steps for images.
- `TabularPreprocessor`
  - The `TabularPreprocessor` class takes in preprocessing steps (defined below) which define preprocessing steps for tabular data.
- `LanguagePreprocessor`
  - TEXT
- `Regression`
  - TEXT
- `BinaryClassification`
  - TEXT
- `MulticlassClassification`
  - TEXT
- `ObjectDetection`
  - TEXT

### Preprocessing Steps

The `aisquared.config.preprocessing` subpackage contains `PreProcStep` objects, which are then fed into either the `ImagePreprocessor` or `TabularPreprocessor` classes. The `PreProcStep` classes are:

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

These step objects can then be placed within either the `TabularPreprocessor` or the `ImagePreprocessor` objects. For the `TabularPreprocessor`, the `ZScore`, `MinMax`, and `OneHot` Steps are supported. For the `ImagePreprocessor`, the `AddValue`, `SubtractValue`, `MultiplyValue`, `DivideValue`, `ConvertToColor`, and `Resize` Steps are supported.

In addition to the `TabularPreprocessor` and `ImagePreprocessor` objects, there is also a `LanguagePreprocessor` object for interacting with and preprocessing text. This object is still under development and its interface is subject to change.

### Final Configuration and Model Creation

Once preprocessing and postprocessing objects have been created, these objects can then be passed to the `aisquared.ModelConfiguration` class. This class utilizes the objects passed to it to build the entire model configuration automatically.

Finally, the `aisquared.create_air_model` takes in a `ModelConfiguration` class and an existing Keras model to create a model file compatible with the AI Squared extension and with the `.air` file extension.
