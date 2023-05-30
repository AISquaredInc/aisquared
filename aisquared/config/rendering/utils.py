from aisquared.base import DEFAULT_CONTAINER_RENDERING_CSS, DEFAULT_HTML_TAG_RENDERING_CSS, DEFAULT_TABLE_RENDERING_CSS, CONTAINER_RENDERING_CSS_FILE, HTML_TAG_RENDERING_CSS_FILE, TABLE_RENDERING_CSS_FILE
import json


def save_default_css():
    """
    Save default CSS so that default CSS can be edited and automatically utilized with changes

    Notes
    -----
    - Saves all CSS files to the `~/.aisquared/` directory
    """

    with open(CONTAINER_RENDERING_CSS_FILE, 'w') as f:
        json.dump(DEFAULT_CONTAINER_RENDERING_CSS, f)

    with open(HTML_TAG_RENDERING_CSS_FILE, 'w') as f:
        json.dump(DEFAULT_HTML_TAG_RENDERING_CSS, f)

    with open(TABLE_RENDERING_CSS_FILE, 'w') as f:
        json.dump(DEFAULT_TABLE_RENDERING_CSS, f)
