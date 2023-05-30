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
        ['filename1.csv'],
        'name',
        input_type='text',
        filter_type='static',
        filter_by_columns=[{
            'inputType': 'static',
            'columnName': 'status',
            'columnValue': 'pending'
        }],
        period=1
    )
