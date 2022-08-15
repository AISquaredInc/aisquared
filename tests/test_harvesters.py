import pytest
import aisquared


def test_image_harvester_init():
    harvester = aisquared.config.harvesting.ImageHarvester()
    assert harvester.to_dict() == {
        'className': 'ImageHarvester',
        'params': {
            'how': 'all'
        }
    }


def test_image_harvester_dtype():
    with pytest.raises(ValueError):
        harvester = aisquared.config.harvesting.ImageHarvester('not_all')


def test_text_harvester():
    harvester = aisquared.config.harvesting.TextHarvester()
    assert harvester.to_dict() == {
        'className': 'TextHarvester',
        'params': {
            'how': 'all',
            'regex': None,
            'flags': 'gu',
            'bodyOnly': False
        }
    }
    harvester = aisquared.config.harvesting.TextHarvester(
        how='regex',
        regex='test',
        body_only=True
    )
    assert harvester.to_dict() == {
        'className': 'TextHarvester',
        'params': {
            'how': 'regex',
            'regex': 'test',
            'flags': 'gu',
            'bodyOnly': True
        }
    }


def test_text_harvester_regex():
    harvester = aisquared.config.harvesting.TextHarvester(
        how='regex',
        regex='\D(\d{5})\D'
    )
    assert harvester.to_dict() == {
        'className': 'TextHarvester',
        'params': {
            'how': 'regex',
            'regex': '\D(\d{5})\D',
            'flags': 'gu',
            'bodyOnly': False
        }
    }


def test_input_harvester():
    harvester = aisquared.config.harvesting.InputHarvester()
    assert harvester.to_dict() == {
        'className': 'InputHarvester',
        'params': {
            'inputType': 'text',
            'maxLength': None,
            'features': None
        }
    }
    harvester = aisquared.config.harvesting.InputHarvester(
        'tabular',
        features=[
            {
                'name': 'age',
                'dtype': 'numeric'
            }
        ]
    )
    assert harvester.to_dict() == {
        'className': 'InputHarvester',
        'params': {
            'inputType': 'tabular',
            'maxLength': None,
            'features': [
                {
                    'name': 'age',
                    'dtype': 'numeric'
                }
            ]
        }
    }


def test_input_harvester_fails():
    with pytest.raises(ValueError):
        aisquared.config.harvesting.InputHarvester('foo')

        aisquared.config.harvesting.InputHarvester(
            max_length=-1
        )

        aisquared.config.harvesting.InputHarvester(
            'tabular', features=['test'])


def test_keyword_harvester():
    harvester = aisquared.config.harvesting.KeywordHarvester(
        ['foo', 'bar'],
        case_sensitive=True
    )
    assert harvester.to_dict() == {
        'className': 'KeywordHarvester',
        'params': {
            'keywords': ['foo', 'bar'],
            'caseSensitive': True
        }
    }
