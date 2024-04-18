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
            'bodyOnly': False,
            'limit': None
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
            'bodyOnly': True,
            'limit': None
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
            'bodyOnly': False,
            'limit': None
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
    harvester = aisquared.config.harvesting.TextHarvester(
        how='keywords',
        keywords=['foo', 'bar'],
        flags='gui'
    )
    assert harvester.to_dict() == {
        'className': 'TextHarvester',
        'params': {
            'bodyOnly': False,
            'how': 'regex',
            'regex': 'foo|bar',
            'flags': 'gui',
            'limit': None
        }
    }


def test_queryparameter_harvester():
    harvester = aisquared.config.harvesting.QueryParameterHarvester(
        'test',
        '*',
        'test'
    )
    assert harvester.to_dict() == {
        'className': 'QueryParameterHarvester',
        'params': {
            'queryKeys': ['test'],
            'urlLocations': ['*'],
            'attributes': ['test']
        }
    }


def test_chatbot_harvester():
    harvester = aisquared.config.harvesting.ChatbotHarvester(
        'ChatBot',
        max_length=256
    )
    assert harvester.to_dict() == {
        'className': 'ChatbotHarvester',
        'params': {
            'title': 'ChatBot',
            'maxLength': 256,
            'inputType': 'text',
            'features': None,
            'harvestHistory': False
        }
    }
