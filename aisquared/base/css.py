import platform
import json
import os

DEFAULT_CONTAINER_RENDERING_CSS = {
    'style': {
        'container': {
            'color': 'black',
            'margin': '0',
            'padding': '24px',
            'fontSize': '16px',
            'background': 'white',
            'borderRadius': '10px'
        }
    }
}

DEFAULT_HTML_TAG_RENDERING_CSS = {
    'style': {
        'content': {
            'border': "none",
            'margin': "0",
            'padding': "8px",
            'background': "transparent",
            'borderRadius': "0",
            'color': "#000000",
            'fontSize': '14px',
            'textAlign': 'left',
            'textDecoration': 'none',
            'textTransform': 'none',
            'fontWeight': 'bold',
            'width': 'auto',
            'height': 'auto',
        },
        'extraContent': {
            'border': "none",
            'margin': "0",
            'padding': "8px",
            'background': "transparent",
            'borderRadius': "0",
            'color': "#000000",
            'fontSize': '14px',
            'textAlign': 'left',
            'textDecoration': 'none',
            'textTransform': 'none',
            'fontWeight': 'bold',
            'width': 'auto',
            'height': 'auto',
        },
    }
}

DEFAULT_TABLE_RENDERING_CSS = {
    'style': {
        'container': {
            'border': "1px solid lightgray",
            'margin': "8px 0",
            'padding': "10px",
            'background': "#f3f3f3",
            'borderRadius': "10px",
            'color': "#000000",
            'fontSize': '14px',
            'textAlign': 'left',
            'fontFamily': 'Raleway, sans-serif',
        },
        'title': {
            'fontWeight': 'bold',
            'marginBottom': '4px',
        },
        'table': {
            'border': "1px solid lightgray",
            'textAlign': 'center',
            'textTransform': 'capitalize',
            'width': "100%",
            'fontFamily': 'Raleway, sans-serif',
        },
        'tableHeader': {
            'border': "1px solid lightgray",
            'padding': "4px",
            'fontWeight': 'bold',
            'textTransform': 'capitalize',
        },
        'tableBody': {
        },
        'tableRows': {
            'border': "1px solid lightgray",
        },
        'rowCells': {
            'border': "1px solid lightgray",
            'fontWeight': 'normal',
            'padding': "8px",
        },
        'headerCells': {
            'border': '1px solid lightgray',
            'padding': '8px',
            'fontWeight': 'bolder',
            'backgroundColor': 'white'
        }
    }
}
DEFAULT_CHART_RENDERING_CSS = {
    "style": {
        "container": {
            "color": "black",
            "border": "1px solid lightgray",
            "margin": "0",
            "padding": "24px",
            "fontSize": "16px",
            "background": "white",
            "borderRadius": "10px"
        }
    }
}

if platform.system() == 'Windows':
    basedir = os.getenv('HOMEPATH')
else:
    basedir = os.getenv('HOME')

DIRECTORY = os.path.join(basedir, '.aisquared')

TABLE_RENDERING_CSS_FILE = os.path.join(DIRECTORY, 'TableRendering.json')
HTML_TAG_RENDERING_CSS_FILE = os.path.join(DIRECTORY, 'HTMLTagRendering.json')
CHART_RENDERING_CSS_FILE = os.path.join(DIRECTORY, 'ChartRendering.json')
CONTAINER_RENDERING_CSS_FILE = os.path.join(
    DIRECTORY, 'ContainerRendering.json')
