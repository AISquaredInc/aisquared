import pytest
import aisquared


def test_filter_rendering():
    with pytest.raises(TypeError):
        aisquared.config.rendering.FilterRendering()

    with pytest.raises(ValueError):
        aisquared.config.rendering.FilterRendering(
            source='test',
            key='test',
            qualifier='gt',
            value='test'
        )
        aisquared.config.rendering.FilterRendering(
            source='inputs',
            key='test',
            qualifier='test',
            value='test'
        )

    filter = aisquared.config.rendering.FilterRendering(
        source='inputs',
        key='test',
        qualifier='gt',
        value='test'
    )
    assert filter.to_dict() == {
        'className': 'FilterRendering',
        'params': {
            'source': 'inputs',
            'key': 'test',
            'qualifier': 'gt',
            'value': 'test'
        }
    }


def test_image_rendering():
    with pytest.raises(ValueError):
        aisquared.config.rendering.ImageRendering(
            placement='test'
        )

    image = aisquared.config.rendering.ImageRendering()

    assert image.to_dict() == {
        'className': 'ImageRendering',
        'params': {
            'color': 'blue',
            'thickness': '5px',
            'placement': 'bottomleft',
            'includeProbability': False,
            'badgeColor': 'white',
            'fontColor': 'black',
            'fontSize': '5px',
            'classes': None,
            'confidenceThreshold': None,
            'regressionThreshold': None
        }
    }


def test_object_rendering():
    with pytest.raises(ValueError):
        aisquared.config.rendering.ObjectRendering(
            color='test'
        )
        aisquared.config.rendering.ObjectRendering(
            placement='test'
        )
        aisquared.config.rendering.ObjectRendering(
            badge_color='test'
        )
        aisquared.config.rendering.ObjectRendering(
            font_color='test'
        )

    object = aisquared.config.rendering.ObjectRendering()

    assert object.to_dict() == {
        'className': 'ObjectRendering',
        'params': {
            'color': 'blue',
            'thickness': '5px',
            'placement': 'bottomleft',
            'includeProbability': False,
            'badgeColor': 'white',
            'fontColor': 'black',
            'fontSize': '5px'
        }
    }


def test_word_rendering():
    with pytest.raises(ValueError):
        aisquared.config.rendering.WordRendering(
            word_list='test'
        )
        aisquared.config.rendering.WordRendering(
            badge_shape='test'
        )

    word = aisquared.config.rendering.WordRendering()
    assert word.to_dict() == {
        'className': 'WordRendering',
        'params': {
            'wordList': 'input',
            'resultKey': None,
            'contentKey': None,
            'badgeShape': 'star',
            'badgeColor': 'blue',
            'classes': None,
            'confidenceThreshold': None,
            'regressionThreshold': None
        }
    }
    word = aisquared.config.rendering.WordRendering(badge_shape='underline')
    assert word.to_dict() == {
        'className': 'WordRendering',
        'params': {
            'wordList': 'input',
            'resultKey': None,
            'contentKey': None,
            'badgeShape': 'underline',
            'badgeColor': 'blue',
            'classes': None,
            'confidenceThreshold': None,
            'regressionThreshold': None
        }
    }


def test_document_rendering():
    document = aisquared.config.rendering.DocumentRendering()
    assert document.to_dict() == {
        'className': 'DocumentRendering',
        'params': {
            'predictionKey': 'className',
            'words': None,
            'documents': None,
            'includeProbability': False,
            'probabilityKey': 'probability',
            'underlineColor': 'blue',
            'classes': None,
            'confidenceThreshold': None,
            'regressionThreshold': None
        }
    }
