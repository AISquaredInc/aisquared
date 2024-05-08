# AISquared

[![Documentation](https://badgen.net/badge/icon/Documentation?icon=chrome&label)](https://aisquaredinc.github.io/aisquared/index.html)
[![PyPI version](https://badge.fury.io/py/aisquared.svg)](https://badge.fury.io/py/aisquared)
![Tests](https://github.com/aisquaredinc/aisquared/actions/workflows/python-package.yml/badge.svg)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

This package contains utilities to interact with the AI Squared technology stack, particularly with developing and deploying models to the AI Squared Platform or other applications developed through the AI Squared JavaScript SDK.

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

The `aisquared` package currently contains five subpackages, the `aisquared.config` package, the `aisquared.base` subpackage, the `aisquared.logging` subpackage, the `aisquared.serving` subpackage, and the `aisquared.platform` package. The `config` package holds objects for building the configuration files that need to be included with converted model files for use within the AI Squared Extension. The contents of the config subpackage contain both pre- and postprocessing steps as well as harvesting, analytic, rendering, and feedback objects to use with the model. The following will explain the functionality of the config package:

### `aisquared.config`

The `aisquared.config` subpackage contains the following objects:

- `ModelConfiguration`
  - The `ModelConfiguration` object is the final object to be used to create the configuration file. It takes as input a list of harvesting steps, list of preprocessing steps, a list of analytics, a list of postprocessing steps, a list of rendering steps, an optional MLFlow URI, an optional MLFlow user, and an optional MLFlow token
- `GraphConfiguration`
  - The `GraphConfiguration object is another method for creating configuration files. Instead of taking a predefined set of steps, it allows the developer to add steps to create a directed acyclic graph

#### `aisquared.config.harvesting`

The `aisquared.config.harvesting` subpackage contains the following objects:

- `ImageHarvester`
  - The `ImageHarvester` class indicates the harvesting of images within the DOM to perform prediction on
- `TextHarvester`
  - The `TextHarvester` class indicates the harvesting of text within the DOM to perform prediction on
- `InputHarvester`
  - The `InputHarvester` class configures harvesting of different kinds of user-defined inputs
- `QueryParameterHarvester`
  - The `QueryParameterHarvester` class configures harvesting based on query parameters

#### `aisquared.config.preprocessing`

The `aisquared.config.preprocessing` subpackage contains the following objects:

- `ImagePreprocessor`
  - The `ImagePreprocessor` class takes in preprocessing steps (defined below) which define preprocessing steps for images.
- `TabularPreprocessor`
  - The `TabularPreprocessor` class takes in preprocessing steps (defined below) which define preprocessing steps for tabular data.
- `TextPreprocessor`
  - The `TextPreprocessor` class takes in preprocessing steps (defined below) which define preprocessing steps for text data.

#### `aisquared.config.analytic`

The `aisquared.config.analytic` subpackage contains the following objects:

- `LocalAnalytic`
  - The `LocalAnalytic` class indicates the use of an analytic or lookup table from a local file
- `LocalModel`
  - The `LocalModel` class indicates the use of a model from a local file
- `DeployedAnalytic`
  - The `DeployedAnalytic` class indicates the use of an analytic or lookup table from a remote resource
- `DeployedModel`
  - The `DeployedModel` class indicates the use of a model deployed to a remote resource
- `ReverseMLWorkflow`
  - The `ReverseMLWorkflow` class indicates the use of a Reverse ML Workflow, pulling predictions from a remote source

#### `aisquared.config.postprocessing`

The `aisquared.config.postprocessing` subpackage contains the following objects:

- `Regression`
  - The `Regression` object is a postprocessing class for models which perform regression. Since it is common to train regression models by scaling regression outputs to values between 0 and 1, this class is designed to convert output values between 0 and 1 to their original values, corresponding to `min` and `max` when the class is instantiated.
- `BinaryClassification`
  - The `BinaryClassification` object is a postprocessing class for models which perform binary classification. The class is instantiated with a label map and a cutoff value used to identify when the positive class (class 1) is identified.
- `MulticlassClassification`
  - The `MulticlassClassification` object is a postprocessing class for models which perform multiclass classification. The class is instantiated with a label map only.
- `ObjectDetection`
  - The `ObjectDetection` object is a postprocessing class for models which perform object detection. The class is instantiated with a label map and a cutoff value for identification.

#### `aisquared.config.rendering`

The `aisquared.config.rendering` subpackage contains the following objects:

- `ImageRendering`
  - The `ImageRendering` object is a rendering class for rendering single predictions on images.
- `ObjectRendering`
  - The `ObjectRendering` object is a rendering class for rendering object detection predictions on images.
- `WordRendering`
  - The `WordRendering` object is a rendering class for rendering highlights, underlines, or badges on individual words.
- `DocumentRendering`
  - The `DocumentRendering` object is a rendering class for rendering document predictions.
- `BarChartRendering`
  - The `BarChartRendering` object is a rendering class for rendering bar charts.
- `ContainerRendering`
  - The `ContainerRendering` object is a rendering class for rendering containers.
- `DashboardReplacementRendering`
  - The `DashboardReplacementRendering` object is a rendering class for rendering complete dashboard replacements
- `DoughnutChartRendering`
  - The `DoughnutChartRendering` object is a class for rendering doughnut charts
- `FilterRendering`
  - The `FilterRendering` object is a class for pass data in a model chain
- `HTMLTagRendering`
  - The `HTMLTagRendering` object is a class for rendering HTML tags
- `PieChartRendering`
  - The `PieChartRendering` object is a class for rendering pie charts
- `SOSRendering`
  - The `SOSRendering` object is a class for rendering SOS dashboards
- `TableRendering`
  - The `TableRendering` object is a class for rendering tables

#### `aisquared.config.feedback`

The `aisquared.config.feedback` subpackage contains the following objects:

- `SimpleFeedback`
  - The `SimpleFeedback` object is a feedback object for simple thumbs up/thumbs down for predictions
- `BinaryFeedback`
  - The `BinaryFeedback` object is a feedback object for binary classification use cases
- `MulticlassFeedback`
  - The `MulticlassFeedback` object is a feedback object for multiclass classification use cases
- `RegressionFeedback`
  - The `RegressionFeedback` object is a feedback object for regression use cases
- `ModelFeedback`
  - The `ModelFeedback` object is a feedback object for configuring feedback for the model directly, rather than its predictions
- `QualitativeFeedback`
  - The `QualitativeFeedback` object is a feedback object for configuring questions asked about each individual prediction the model makes

#### Preprocessing Steps

The `aisquared.config.preprocessing` subpackage contains `PreProcStep` objects, which are then fed into the `ImagePreprocessor`, `TabularPreprocessor`, and `TextPreprocessor` classes. The `PreProcStep` classes are:

- `tabular.ZScore`
  - This class configures standard normalization procedures for tabular data
- `tabular.MinMax`
  - This class configures Min-Max scaling procedures for tabular data
- `tabular.OneHot`
  - This class configures One Hot encoding for columns of tabular data
- `tabular.DropColumn`
  - This class configures dropping columns
- `image.AddValue`
  - This class configures adding values to pixels in image data
- `image.SubtractValue`
  - This class configures subtracting values to pixels in image data
- `image.MultiplyValue`
  - This class configures multiplying pixel values by a value in image data
- `image.DivideValue`
  - This class configures dividing pixel values by a value in image data
- `image.ConvertToColor`
  - This class configures converting images to the specified color scheme
- `image.Resize`
  - This class configures image resize procedures
- `text.Tokenize`
  - This class configures how text will be tokenized
- `text.RemoveCharacters`
  - This class configures which characters should be removed from text
- `text.ConvertToCase`
  - This class configures which case - upper or lower - text should be converted to
- `text.ConvertToVocabulary`
  - This class configures how text tokens should be converted to vocabulary integers
- `text.PadSequences`
  - This class configures how padding should occur given a sequence of text tokens converted to a sequence of integers

These step objects can then be placed within the `TabularPreprocessor`, `ImagePreprocessor`, or `TextPreprocessor` objects. For the `TabularPreprocessor`, the `ZScore`, `MinMax`, and `OneHot` Steps are supported. For the `ImagePreprocessor`, the `AddValue`, `SubtractValue`, `MultiplyValue`, `DivideValue`, `ConvertToColor`, and `Resize` Steps are supported. For the `TextPreprocessor`, the `Tokenize`, `RemoveCharacters`, `ConvertToCase`, `ConvertToVocabulary`, and `PadSequences` Steps are supported

#### Final Configuration and Model Creation

Once harvesting, preprocessing, analytic, postprocessing, and rendering objects have been created, these objects can then be passed to the `aisquared.config.ModelConfiguration` class. This class utilizes the objects passed to it to build the entire model configuration automatically.

Once the `ModelConfiguration` object has been created with the required parameters, the `.compile()` method can be used to create a file with the `.air` extension that can be loaded into an application which utilizes the AI Squared JavaScript SDK.

### `aisquared.base`

The `aisquared.base` subpackage contains base utilities not designed to be directly called by the end user.

### `aisquared.platform`

The `aisquared.platform` subpackage contains classes and utilities for interacting with the AI Squared Platform. It primarily contains the `AISquaredPlatformClient` with the following capabilities:

- The ability to securely log in to an instance of the AI Squared Platform
- The ability to check whether the connection is healthy
- The ability to list `.air` files deployed to the platform
- The ability to retrieve the configuration for a `.air` file deployed in the platform
- The ability to delete a `.air` file deployed in the platform
- The ability to list users who have a `.air` file shared with them
- The ability to share a `.air` file with users
- The ability to unshare a `.air` file with users
- The ability to list all users of the platform
- The ability to list all groups in the platform
- The ability to list all users in a group in the platform

### `aisquared.serving` (requires installing aisquared\[full\])

The `aisquared.serving` subpackage contains utilities for serving models locally or remotely using [MLflow](https://mlflow.org) or locally using [Flask](https://flask.palletsprojects.com/en/2.1.x/).

### `aisquared.logging` (requires installing aisquared\[full\])

The `aisquared.logging` subpackage is powered by [MLflow](https://mlflow.org), a powerful open-source platform for the machine learning lifecycle. The `logging` subpackage inherits nearly all functionality from mlflow, so we highly recommend users refer to the [MLflow documentation site](https://mlflow.org/docs/latest/index.html) for additional information.

In this subpackage, we have additionally added implementations of individual functions to save TensorFlow, Keras, Scikit-Learn, and PyTorch models in a format that can be deployed quickly using MLflow.

## Contributing

AI Squared welcomes feedback and contributions to this repository! We use GitHub for issue tracking, so feel free to place your input there. For any issues you would like to keep confidential, such as any confidential security issues, or if you would like to contribute directly to this project, please reach out to pythonsdk@squared.ai and we will get back to you as soon as possible.

## Changes

Below are a list of additional features, bug fixes, and other changes made for each version.

## Version 0.1.3
- Added `flags` parameter to `TextHarvester` using regular expression harvesting
- Deleted `model_feedback` parameter in `ModelConfiguration` object and included functionality in `feedback_steps` parameter
- Changed `format` parameter to `header` for both deployed analytics
- Added feedback and stages to `DocumentPredictor` and `ImagePredictor` objects
- Non-API changes for `ALLOWED_STAGES`
- Fixed bugs preventing Windows users from importing the package
- Updated `ModelConfiguration` to include `url` parameter
- Changed default tokenization string

## Version 0.2.0
- Moved preprocessing steps under subpackages for specific kinds of preprocessing steps
- Cleaned up documentation to render within programmatic access environments
- Added `aisquared.logging` subpackage
- Created `InputHarvester`
  - Allows for harvesting of input text, images, and tabular data
- Created the `aisquared.serving` subpackage, specifically the `deploy_model` and `get_remote_prediction` functions
- Created the `GraphConfiguration` class
- Added `auto-run` parameter to `ModelConfiguration` and `GraphConfiguration` classes
- Created the `aisquared` CLI with the following commands:
  - `aisquared deploy`, which deploys a model locally
  - `aisquared predict`, which predicts using a local JSON file
  - `aisquared airfiles`, which contains the subcommands `list`, `delete`, `download`, and `upload`
- Changed all classes within `aisquared.config.analytic` to accept `'tabular'` as an `input_type`
- Removed `aisquared.logging` and `aisquared.remote` from top-level imports
- Added `round` parameter to Regression postprocesser
- Removed `DocumentPredictor` and `ImagePredictor` classes
- Removed `ChainRendering` class
- Created `FilterRendering` class
- Altered `QUALIFIERS`
- Added advanced rendering parameters to rendering objects
- Removed `logging` and `remote` subpackages from top-level `aisquared` import

## Version 0.2.1
- Added the `S3Connector` class to the `analytics` subpackage, which allows download of an analytic directly from S3
- Updated the documentation and added the `docs` subdirectory for hosting the documentation on GitHub Pages

## Version 0.2.2
- Fixed bug in `to_dict` method within `ObjectRendering` class
- Fixed bug in name of `MultiplyValue` step
- Fixed bug in datatype checking for text harvester
- Added `body_only` parameter to `TextHarvester`
- Added `'underline'` to possible badges
- Added `threshold_key` and `threshold_values` to relevant rendering classes
- Added `Trim` text preprocessing class
- Added `CustomObject` in the base package to allow for creation of custom classes
- Added keyword harvesting capabilities
- Added `utils` subpackage with capabilities to mimic a trained sklearn model
- Small documentation changes
- Changed the required imports for the package to streamline installation process, and created two installation options
`aisquared` and `aisquared[full]`

## Version 0.2.3
- Added functionality to add custom preprocessing and postprocessing functions to the model deployment pipeline
- Added `all` parameter to `LocalAnalytic` class
- Changed under-the-hood functionality of `mimic_model` function in line with updates to `BeyondML`
- Altered the `ReverseMLWorkflow` analytic
- Added the `BarChartRendering`, `ContainerRendering`, `DashboardReplacementRendering`, `DoughnutChartRendering`, `HTMLTagRendering`, `LineChartRendering`, `PieChartRendering`, `SOSRendering`, and `TableRendering` rendering classes
- Added the `QueryParameterHarvester` harvester class
- Added the `limit` parameter to the TextHarvester class


## Version 0.3.0
- Added type hinting to documentation strings
- Revamped documentation to use Sphinx

## Version 0.3.1
- Changed Python type hints to allow for backwards compatibility with older versions of Python

## Version 0.3.2
- Added functionality to the `AISquaredPlatformClient`
- Added `top_level_kwargs` parameter to the `CustomObject` class
- Added `DashboardRendering` class
- Removed 'px' from default values in ImageRendering and ObjectRendering classes
- Added functionality for creating, updating, and deleting users to `AISquaredPlatformClient`
- Added functionality for creating, updating, and delting groups to `AISquaredPlatformClient`
- Fixed bug related to requiring `auto_run` parameter to be string (fix involves casting as string)
- Altered schemas for different "Chart" Rendering classes to conform to JavaScript standards
- Streamlined the `ModelConfiguration` class to allow a more functional interface to build `.air` files
- Updated `ContainerRendering` class with parameters for `position` and `static_position`
- Updated across-the-board functionality of the `AISquaredPlatformClient`

## Version 0.3.3
- Updated functionality of the `AISquaredPlatformClient` to interact directly with the platform ALB
- Changed function names in support of change from MANN to BeyondML
- Added documentation surrounding global configuration objects
- Removed redundant additional dependencies

## Version 0.3.4
- Added support for custom CSS strings to appropriate rendering classes
- Refactored `AISquaredPlatformClient` to import functions from support files
- Fixed documentation errors for the documentation site
- Checked whether responses returned OK status code rather than 200
- Moved `CustomObject` to `aisquared.config` from `aisquared.base`
- Changed endpoint used to list platform users
- Fixed response behaviors where no data was returned from `AISquaredPlatformClient`

## Version 0.3.5
- Changed `file_name` parameter in `ReverseMLWorkflow` to `file_names`
- Added `documentation_link` parameter to `ModelConfiguration` class

## Version 0.3.6
- Fixed issue with type checking for `ModelConfiguration` Rendering classes
- Restricted TensorFlow version to below `2.12.0` to prevent import issues
- Added `position` parameter to `WordRendering` class
- Changed default CSS styling for rendering classes
- Changed name of all `processor` classes to `processer`

## Version 0.3.7
- Changed schema of the `DeployedAnalytic` class to include API key management
- Changed JSON schema of Preprocesser classes
- Allowed .keras files to be saved and loaded with the `ModelConfiguration` and `GraphConfiguration` APIs into `.air` files
- Relaxed TensorFlow requirements enforced in version `0.3.6`

## Version 0.3.8
- Created `ChatbotHarvester` class
- Created `TextRendering` class
- Changed location of reference lists of classes to clean up code
- Updated class schemas to ensure compliance with expectations
- Updated test cases

## Version 0.3.9
- Added `CustomRendering` class
- Changed to full import of `CustomObject` in `aisquared.base` subpackage

## Version 0.3.10
- Added `DatabricksClient` to the `aisquared.platform` subpackage

## Version 0.3.11
- Updated `DeployedModel` class configuration to conform to AIRJS
- Updated `DatabricksClient` class to include `update_job` function
- Updated custom CSS fields in rendering classes
- Reconfigured `ReverseMLWorkflow` class
- Added `'User-Agent'` to headers for `AISquaredPlatformClient` and `DatabricksClient`
- Added `llmlink` as a dependency to the 'full' installation of `aisquared` and added it as a top-level package

## Version 0.3.12
- Updated `DeployedModel` class to support more abstract API calls
- Updated `ChatbotHarvester`, `DeployedAnalytic`, and `ChatRendering` classes
- Updated `ModelConfiguration` class with `warnings` and `documentURL`
- Updated `DeployedAnalytic` class with more general support for API calls, `DeployedModel` to be deprecated
- Created `ONNXModel` class to support ONNX models

## Version 0.3.13
- Removed TensorFlow from base dependencies due to issues with running `aisquared` on Mac ARM devices