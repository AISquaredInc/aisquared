import pytest
import aisquared


def test_analytic_init():
    with pytest.raises(TypeError):
        aisquared.config.analytic.LocalAnalytic()
        aisquared.config.analytic.LocalModel()
        aisquared.config.analytic.DeployedAnalytic()
        aisquared.config.analytic.DeployedModel()
        aisquared.config.analytic.S3Connector()

        aisquared.config.analytic.LocalModel('test', 'foo')

    aisquared.config.analytic.LocalAnalytic(
        'test',
        'cv'
    )
    aisquared.config.analytic.LocalModel(
        'test',
        'text'
    )
    aisquared.config.analytic.DeployedAnalytic(
        'test',
        'tabular'
    )
    aisquared.config.analytic.DeployedModel(
        'test',
        'cv'
    )
    aisquared.config.analytic.ReverseMLWorkflow(
        'bucket',
        'filename',
        'column',
        10
    )
