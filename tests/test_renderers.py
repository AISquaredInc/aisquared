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
            'thresholdKey': None,
            'thresholdValue': None
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
            'thresholdKey': None,
            'thresholdValue': None
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
            'thresholdKey': None,
            'thresholdValue': None
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
            'thresholdKey': None,
            'thresholdValue': None
        }
    }


def test_bar_chart_rendering():
    renderer = aisquared.config.rendering.BarChartRendering(
        label='test',
        id='test',
        chart_name='test',
        chart_colors=['blue', 'red'],
        chart_labels=['label1', 'label2'],
        container_id='test',
        prediction_name_key='',
        prediction_value_key='',
        prediction_name_value=''
    )
    assert renderer.to_dict() == {
        'className': 'BarChartRendering',
        'label': 'test',
        'params': {
            'id': 'test',
            'chartName': 'test',
            'chartColors': ['blue', 'red'],
            'chartLabels': ['label1', 'label2'],
            'containerId': 'test',
            'predictionNameKey': '',
            'predictionValueKey': '',
            'predictionNameValue': '',
            'width': 'auto',
            'height': 'auto',
            'xOffset': '0',
            'yOffset': '0'
        }
    }


def test_line_chart_rendering():
    renderer = aisquared.config.rendering.LineChartRendering(
        label='test',
        id='test',
        chart_name='test',
        chart_colors=['blue', 'red'],
        chart_labels=['label1', 'label2'],
        container_id='test',
        prediction_name_key='',
        prediction_value_key='',
        prediction_name_value=''
    )
    assert renderer.to_dict() == {
        'className': 'LineChartRendering',
        'label': 'test',
        'params': {
            'id': 'test',
            'chartName': 'test',
            'chartColors': ['blue', 'red'],
            'chartLabels': ['label1', 'label2'],
            'containerId': 'test',
            'predictionNameKey': '',
            'predictionValueKey': '',
            'predictionNameValue': '',
            'width': 'auto',
            'height': 'auto',
            'xOffset': '0',
            'yOffset': '0'
        }
    }


def test_doughnut_chart_rendering():
    renderer = aisquared.config.rendering.DoughnutChartRendering(
        label='test',
        id='test',
        chart_name='test',
        chart_colors=['blue', 'red'],
        chart_labels=['label1', 'label2'],
        container_id='test',
        prediction_name_key='',
        prediction_value_key='',
        prediction_name_value='',
        display_legend=True,
        legend_icon='circle'
    )
    assert renderer.to_dict() == {
        'className': 'DoughnutChartRendering',
        'label': 'test',
        'params': {
            'id': 'test',
            'chartName': 'test',
            'chartColors': ['blue', 'red'],
            'chartLabels': ['label1', 'label2'],
            'containerId': 'test',
            'predictionNameKey': '',
            'predictionValueKey': '',
            'predictionNameValue': '',
            'displayLegend': True,
            'legendIcon': 'circle',
            'width': 'auto',
            'height': 'auto',
            'xOffset': '0',
            'yOffset': '0'
        }
    }


def test_pie_chart_rendering():
    renderer = aisquared.config.rendering.PieChartRendering(
        label='test',
        id='test',
        chart_name='test',
        chart_colors=['blue', 'red'],
        chart_labels=['label1', 'label2'],
        container_id='test',
        prediction_name_key='',
        prediction_value_key='',
        prediction_name_value='',
        display_legend=True,
        legend_icon='circle'
    )
    assert renderer.to_dict() == {
        'className': 'PieChartRendering',
        'label': 'test',
        'params': {
            'id': 'test',
            'chartName': 'test',
            'chartColors': ['blue', 'red'],
            'chartLabels': ['label1', 'label2'],
            'containerId': 'test',
            'predictionNameKey': '',
            'predictionValueKey': '',
            'predictionNameValue': '',
            'displayLegend': True,
            'legendIcon': 'circle',
            'width': 'auto',
            'height': 'auto',
            'xOffset': '0',
            'yOffset': '0'
        }
    }


def test_container_rendering():
    renderer = aisquared.config.rendering.ContainerRendering(
        label='test',
        id='test',
        query_selector='test'
    )
    assert renderer.to_dict() == {
        'className': 'ContainerRendering',
        'label': 'test',
        'params': {
            'id': 'test',
            'width': 'auto',
            'height': 'auto',
            'display': 'flex',
            'xOffset': '0',
            'yOffset': '0',
            'position': '',
            'orientation': 'column',
            'querySelector': 'test'
        }
    }


def test_dashboard_replacement_rendering():
    renderer = aisquared.config.rendering.DashboardReplacementRendering(
        'test'
    )
    assert renderer.to_dict() == {
        'className': 'DashboardReplacementRendering',
        'label': '',
        'params': {
            'anchorSelector': 'test',
            'whereReplace': ''
        }
    }


def test_html_tag_rendering():
    renderer = aisquared.config.rendering.HTMLTagRendering(
        label='test',
        id='test',
        container_id='test',
        html_content='test',
        extra_content_tag='test',
        injection_action='test',
        prediction_name_key='test',
        prediction_value_key='test',
        prediction_name_value='test',
    )

    assert renderer.to_dict() == {
        'className': 'HTMLTagRendering',
        'label': 'test',
        'params': {
            'id': 'test',
            'containerId': 'test',
            'htmlContent': 'test',
            'extraContentTag': 'test',
            'injectionAction': 'test',
            'predictionNameKey': 'test',
            'predictionValueKey': 'test',
            'predictionNameValue': 'test',
            'content': ''
        }
    }


def test_sos_rendering():
    renderer = aisquared.config.rendering.SOSRendering(True)
    assert renderer.to_dict() == {
        'className': 'SOSRendering',
        'label': '',
        'params': {
            'canToggle': True
        }
    }


def test_table_rendering():
    renderer = aisquared.config.rendering.TableRendering(
        label='test',
        id='test',
        container_id='test',
        prediction_name_key='test',
        prediction_value_key='test',
        prediction_name_values=['name1', 'name2']
    )
    assert renderer.to_dict() == {
        'className': 'TableRendering',
        'label': 'test',
        'params': {
            'id': 'test',
            'containerId': 'test',
            'predictionNameKey': 'test',
            'predictionValueKey': 'test',
            'predictionNameValues': ['name1', 'name2'],
            'tableName': ''
        }
    }
