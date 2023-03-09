import platform
import json
import os

DEFAULT_CONTAINER_RENDERING_CSS = {
    'style': {
        'container': {
            'border': "none",
            'margin': "0",
            'padding': "8px",
            'background': "#ffffff",
            'borderRadius': "0",
            'color': "#000000",
            'fontSize': '16px',
            'textAlign': 'left',
            'textDecoration': 'none',
            'textTransform': 'none',
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
            'fontSize': '16px',
            'textAlign': 'left',
            'textDecoration': 'none',
            'textTransform': 'none',
            'fontWeight': '',
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
            'fontSize': '16px',
            'textAlign': 'left',
            'textDecoration': 'none',
            'textTransform': 'none',
            'fontWeight': '',
            'width': 'auto',
            'height': 'auto',
        },
    }
}

DEFAULT_TABLE_RENDERING_CSS = {
    'style': {
        'container': {
            'border': "none",
            'margin': "0",
            'padding': "8px",
            'background': "#ffffff",
            'borderRadius': "0",
            'color': "#000000",
            'fontSize': '16px',
            'textAlign': 'left',
            'textDecoration': 'none',
            'textTransform': 'none',
        },
        'title': {
            'color': "inherit",
            'fontSize': '16px',
            'textAlign': 'left',
            'textDecoration': 'none',
            'textTransform': 'capitalize',
            'textShadow': 'none',
            'textIndent': '',
            'letterSpacing': '',
            'lineHeight': '',
            'wordSpacing': '',
            'whiteSpace': ''
        },
        'table': {
            'border': "1px solid lightgray",
            'margin': "8px",
            'padding': "8px",
            'background': "transparent",
            'color': '#000000',
            'fontSize': '16px',
            'textAlign': 'left',
            'textDecoration': 'none',
            'textTransform': 'capitalize',
            'width': "auto",
            'height': "auto"
        },
        'tableHeader': {
            'border': "1px solid lightgray",
            'background': "transparent",
            'color': "#000000",
            'margin': "0",
            'padding': "0",
            'fontSize': '16px',
            'textAlign': 'left',
            'textDecoration': 'none',
            'textTransform': 'capitalize',
        },
        'tableBody': {
            'border': "1px solid lightgray",
            'background': "transparent",
            'color': "#000000",
            'margin': "8px",
            'padding': "8px",
            'fontSize': '16px',
            'textAlign': 'left',
            'textDecoration': 'none',
            'textTransform': 'capitalize',
        },
        'tableRows': {
            'border': "1px solid lightgray",
            'background': "transparent",
            'color': "#000000",
            'margin': "0",
            'padding': "0",
            'fontSize': '16px',
            'textAlign': 'left',
            'textDecoration': 'none',
            'textTransform': 'capitalize',
        },
        'rowCells': {
            'border': "1px solid lightgray",
            'background': "transparent",
            'color': "#000000",
            'margin': "0",
            'padding': "0",
            'fontSize': '16px',
            'textAlign': 'left',
            'textDecoration': 'none',
            'textTransform': 'capitalize',
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
CONTAINER_RENDERING_CSS_FILE = os.path.join(
    DIRECTORY, 'ContainerRendering.json')
