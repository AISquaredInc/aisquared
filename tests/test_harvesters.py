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
            'flags': 'gu'
        }
    }
    harvester = aisquared.config.harvesting.TextHarvester(
        how = 'regex',
        regex = 'test'
    )
    assert harvester.to_dict() == {
        'className': 'TextHarvester',
        'params': {
            'how': 'regex',
            'regex': 'test',
            'flags': 'gu'
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
            'flags': 'gu'
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
