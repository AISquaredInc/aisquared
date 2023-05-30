from typing import Type
import pytest
import aisquared


def test_postprocesser_init():
    with pytest.raises(TypeError):
        aisquared.config.postprocessing.BinaryClassification(
            ['zero', 'one'],
            0
        )
        aisquared.config.postprocessing.ObjectDetection(
            ['zero', 'one'],
            0
        )
        aisquared.config.postprocessing.Regression(
            min='test'
        )
        aisquared.config.postprocessing.Regression(
            max='test'
        )
        aisquared.config.postprocessing.Regression(
            round='test'
        )

    with pytest.raises(ValueError):
        aisquared.config.postprocessing.BinaryClassification(
            ['zero', 'one'],
            -0.5
        )
        aisquared.config.postprocessing.ObjectDetection(
            ['zero', 'one'],
            -0.5
        )
        aisquared.config.postprocessing.MulticlassClassification(
            ['zero', 'one']
        )

    aisquared.config.postprocessing.BinaryClassification(
        ['zero', 'one']
    )
    aisquared.config.postprocessing.ObjectDetection(
        ['zero', 'one']
    )
    aisquared.config.postprocessing.MulticlassClassification(
        ['zero', 'one', 'two']
    )
    aisquared.config.postprocessing.Regression(
        12,
        24,
        round=True
    )
