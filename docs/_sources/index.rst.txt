.. aisquared documentation master file, created by
   sphinx-quickstart on Thu Jan  5 08:00:19 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: images/aisquared.png
   :width: 400
   :align: center

|
|

Welcome to the documentation for the `aisquared` python package!
================================================================

This package contains utilities to interact with the AI Squared technology stack, particularly with developing and deploying models to the AI Squared Platform or other applications developed through the AI Squared JavaScript SDK.

**Current Production Version:** ``0.3.7``

:download:`View this Documentation in PDF Format <./_build/latex/aisquared.pdf>`.

|

Installation
************

This package is available through `Pypi <https://pypi.org>`_ and can be installed by running the following command:

.. code-block:: bash
   
   pip install aisquared

Alternatively, the latest version of the software can be installed directly from GitHub using the following command:

.. code-block:: bash
   
   pip install git+https://github.com/AISquaredInc/aisquared

.. toctree::
   :maxdepth: 4
   :caption: Documentation
   
   modules

Changelog
*********

- Version 0.1.3
   - Added `flags` parameter to `TextHarvester` using regular expression harvesting
   - Deleted `model_feedback` parameter in `ModelConfiguration` object and included functionality in `feedback_steps` parameter
   - Changed `format` parameter to `header` for both deployed analytics
   - Added feedback and stages to `DocumentPredictor` and `ImagePredictor` objects
   - Non-API changes for `ALLOWED_STAGES`
   - Fixed bugs preventing Windows users from importing the package
   - Updated `ModelConfiguration` to include `url` parameter
   - Changed default tokenization string
- Version 0.2.0
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
- Version 0.2.1
   - Added the `S3Connector` class to the `analytics` subpackage, which allows download of an analytic directly from S3
   - Updated the documentation and added the `docs` subdirectory for hosting the documentation on GitHub Pages
- Version 0.2.2
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
   - Changed the required imports for the package to streamline installation process, and created two installation options `aisquared` and `aisquared[full]`
- Version 0.2.3
   - Added functionality to add custom preprocessing and postprocessing functions to the model deployment pipeline
   - Added `all` parameter to `LocalAnalytic` class
   - Changed under-the-hood functionality of `mimic_model` function in line with updates to `BeyondML`
   - Altered the `ReverseMLWorkflow` analytic
   - Added the `BarChartRendering`, `ContainerRendering`, `DashboardReplacementRendering`, `DoughnutChartRendering`, `HTMLTagRendering`, `LineChartRendering`, `PieChartRendering`, `SOSRendering`, and `TableRendering` rendering classes
   - Added the `QueryParameterHarvester` harvester class
   - Added the `limit` parameter to the TextHarvester class
- Version 0.3.0
   - Added type hinting to documentation strings
   - Revamped documentation to use Sphinx
- Version 0.3.1
   - Changed Python type hints to allow for backwards compatibility with older versions of Python
- Version 0.3.2
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
- Version 0.3.3
   - Updated functionality of the `AISquaredPlatformClient` to interact directly with the platform ALB
   - Changed function names in support of change from MANN to BeyondML
   - Added documentation surrounding global configuration objects
   - Removed redundant additional dependencies
- Version 0.3.4
   - Added support for custom CSS strings to appropriate rendering classes
   - Refactored `AISquaredPlatformClient` to import functions from support files
   - Fixed documentation errors for the documentation site
   - Checked whether responses returned OK status code rather than 200
   - Moved `CustomObject` to `aisquared.config` from `aisquared.base`
   - Changed endpoint used to list platform users
   - Fixed response behaviors where no data was returned from `AISquaredPlatformClient`
- Version 0.3.5
   - Changed `file_name` parameter in `ReverseMLWorkflow` to `file_names`
   - Added `documentation_link` parameter to `ModelConfiguration` class
- Version 0.3.6
   - Fixed issue with type checking for `ModelConfiguration` Rendering classes
   - Restricted TensorFlow version to below `2.12.0` to prevent import issues
   - Added `position` parameter to `WordRendering` class
   - Changed default CSS styling for rendering classes
   - Changed name of all `processor` classes to `processer`
- Version 0.3.7
   - Changed schema of the `DeployedAnalytic` class to include API key management
   - Changed JSON schema of Preprocesser classes
   - Allowed .keras files to be saved and loaded with the `ModelConfiguration` and `GraphConfiguration` APIs into `.air` files
   - Relaxed TensorFlow requirements enforced in version `0.3.6`
