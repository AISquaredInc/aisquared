# AISquared

This package contains utilities to interact with the AI Squared technology stack, particularly with developing and deploying models to the AI Squared Browser Extension.

## Installation

This package is not (yet) available through [Pypi](https://pypi.org), though that is on the development roadmap. For the time being, installation requires downloading and installing the source code directly, which can be done using the following commands

```bash
# clone the repository and cd into it
git clone https://github.com/AISquaredInc/aisquared
cd aisquared

# install dependencies
pip install -r requirements.txt

# install the package
pip install .
```

## Capabilities

The `aisquared` package includes two subpackages, the `aisquared.preprocessing` package and the `aisquared.postprocessing` package. The preprocessing package includes utilities to configure preprocessing steps for data before it is fed into the model, and the postprocessing package contains utilities to configure postprocessing of model output after prediction. Objects within these two classes are then fed into top-level utilities to fully configure and prepare a model for deployment.

This package is currently in a state of constant development, so it is very likely that breaking changes will be made often. We will work to create stable releases in the future.

### Preprocessing

The `aisquared.preprocessing` subpackage contains `PreProcStep` objects, which are then fed into either the `ImagePreprocessor` or `TabularPreprocessor` classes. The `PreProcStep` classes are:

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

### Postprocessing

The `aisquared.postprocessing` subpackage contains classes for configuring processing model predictions. The following classes are present in this package to support different predictive cases. The following classes are contained within this package:

- `BinaryClassification`
  - The `BinaryClassification` class helps configure output for a binary classification task. To configure this class, a label map must be provided, and a threshold value for detection can optionally be provided as well.
- `MulticlassClassification`
  - The `MulticlassClassification` class helps configure output for a multiclass classification task. To configure this class, a label map must be provided.
- `ObjectDetection`
  - The `ObjectDetection` class helps configure output for object detection tasks. To configure this class, a label map must be provided, and a threshold value for detection can optionally be provided as well.
- `Regression`
  - The `Regression` class helps configure output for regression tasks. To configure this class, a minimum and maximum value must be provided, to which the output values of 0 and 1 will be mapped.


### Final Configuration and Model Creation

Once preprocessing and postprocessing objects have been created, these objects can then be passed to the `aisquared.ModelConfiguration` class. This class utilizes the objects passed to it to build the entire model configuration automatically.

Finally, the `aisquared.create_air_model` takes in a `ModelConfiguration` class and an existing Keras model to create a model file compatible with the AI Squared extension and with the `.air` file extension.
