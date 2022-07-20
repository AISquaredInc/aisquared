import pytest
import aisquared


def test_base_notimplemented():
    obj = aisquared.base.BaseObject()
    with pytest.raises(NotImplementedError):
        obj.to_dict()


def test_stages():
    assert aisquared.base.ALLOWED_STAGES == [
        'experimental',
        'staging',
        'production'
    ]


def test_locations():
    assert aisquared.base.LOCATIONS == [
        None,
        'top',
        'bottom',
        'left',
        'right',
        'topright',
        'topleft',
        'bottomright',
        'bottomleft'
    ]


def test_badges():
    assert aisquared.base.BADGES == [
        'circle',
        'square',
        'star',
        'underline'
    ]


def test_word_lists():
    assert aisquared.base.WORD_LISTS == [
        'input',
        'result'
    ]


def test_qualifiers():
    assert aisquared.base.QUALIFIERS == [
        'gt',
        'lt',
        'gte',
        'lte',
        'in',
        'ne',
        'nin'
    ]
