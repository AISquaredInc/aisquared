"""
THIS MODULE IS IN DEVELOPMENT AND NOT STABLE. PLEASE USE WITH CAUTION AND DO NOT USE FOR ANY PRODUCTION WORKLOADS
"""

import random
import string

import warnings

from aisquared.base import BaseObject

from .BarChartRendering import BarChartRendering
from .ContainerRendering import ContainerRendering
from .DoughnutChartRendering import DoughnutChartRendering
from .HTMLTagRendering import HTMLTagRendering
from .LineChartRendering import LineChartRendering
from .PieChartRendering import PieChartRendering
from .TableRendering import TableRendering


class DashboardRendering(BaseObject):
    """
    THIS CLASS IS IN DEVELOPMENT AND IS NOT STABLE. PLEASE USE WITH CAUTION AND DO NOT USE FOR ANY PRODUCTION WORKLOADS
    """

    def __init__(self):
        super().__init__()
        self._steps = []
        warnings.warn(
            'THIS CLASS IS IN DEVELOPMENT AND IS NOT STABLE. PLEASE USE WITH CAUTION AND DO NOT USE FOR ANY PRODUCTION WORKLOADS',
            UserWarning
        )

    @property
    def steps(self):
        return self._steps

    def add_container(
        self,
        query_selector: str,
        width: str = 'auto',
        height: str = 'auto',
        display: str = 'flex',
        xOffset: str = '0',
        yOffset: str = '0',
        position: str = '',
        orientation: str = 'column',
        id: str = None,
        label: str = None
    ):
        if id is None:
            id = ''.join(random.choices(string.ascii_letters, k=10))
        if label is None:
            label = id

        self._steps.append(
            ContainerRendering(
                label=label,
                id=id,
                query_selector=query_selector,
                width=width,
                height=height,
                display=display,
                xOffset=xOffset,
                yOffset=yOffset,
                position=position,
                orientation=orientation
            )
        )

        return id

    def add_bar_chart(
        self,
        container_id: str,
        prediction_name_key: str,
        prediction_value_key: str,
        prediction_name_value: str,
        chart_colors: list,
        chart_labels: list,
        width: str = 'auto',
        height: str = 'auto',
        xOffset: str = '0',
        yOffset: str = '0',
        id: str = None,
        label: str = None,
        chart_name: str = None
    ):
        if id is None:
            id = ''.join(random.choices(string.ascii_letters, k=10))
        if label is None:
            label = id
        if chart_name is None:
            label = id

        self._steps.append(
            BarChartRendering(
                label=label,
                id=id,
                chart_name=chart_name,
                chart_colors=chart_colors,
                chart_labels=chart_labels,
                container_id=container_id,
                prediction_name_key=prediction_name_key,
                prediction_value_key=prediction_value_key,
                prediction_name_value=prediction_name_value,
                width=width,
                height=height,
                xOffset=xOffset,
                yOffset=yOffset
            )
        )

    def add_doughnut_chart(
        self,
        container_id: str,
        prediction_name_key: str,
        prediction_value_key: str,
        prediction_name_value: str,
        chart_colors: list,
        chart_labels: list,
        display_legend: bool = True,
        legend_icon: str = 'circle',
        width: str = 'auto',
        height: str = 'auto',
        xOffset: str = '0',
        yOffset: str = '0',
        id: str = None,
        label: str = None,
        chart_name: str = None
    ):
        if id is None:
            id = ''.join(random.choices(string.ascii_letters, k=10))
        if label is None:
            label = id
        if chart_name is None:
            chart_name = id

        self._steps.append(
            DoughnutChartRendering(
                label=label,
                id=id,
                chart_name=chart_name,
                chart_colors=chart_colors,
                chart_labels=chart_labels,
                container_id=container_id,
                prediction_name_key=prediction_name_key,
                prediction_value_key=prediction_value_key,
                prediction_name_value=prediction_name_value,
                display_legend=display_legend,
                legend_icon=legend_icon,
                width=width,
                height=height,
                xOffset=xOffset,
                yOffset=yOffset
            )
        )

    def add_html_tag(
        self,
        container_id: str,
        html_content: str,
        prediction_name_key: str = '',
        prediction_value_key: str = '',
        prediction_name_value: str = '',
        extra_content_tag: str = 'strong',
        injection_action: str = 'prepend',
        id: str = None,
        content: str = '',
        label: str = None
    ):
        if id is None:
            id = ''.join(random.choices(string.ascii_letters, k=10))
        if label is None:
            label = id

        self._steps.append(
            HTMLTagRendering(
                label=label,
                id=id,
                container_id=container_id,
                html_content=html_content,
                extra_content_tag=extra_content_tag,
                injection_action=injection_action,
                prediction_name_key=prediction_name_key,
                prediction_value_key=prediction_value_key,
                prediction_name_value=prediction_name_value,
                content=content
            )
        )

    def add_line_chart(
        self,
        container_id: str,
        prediction_name_key: str,
        prediction_value_key: str,
        prediction_name_value: str,
        chart_colors: list,
        chart_labels: list,
        width: str = 'auto',
        height: str = 'auto',
        xOffset: str = '0',
        yOffset: str = '0',
        id: str = None,
        label: str = None,
        chart_name: str = None
    ):
        if id is None:
            id = ''.join(random.choices(string.ascii_letters, k=10))
        if label is None:
            label = id
        if chart_name is None:
            chart_name = id

        self._steps.append(
            LineChartRendering(
                label=label,
                id=id,
                chart_name=chart_name,
                chart_colors=chart_colors,
                chart_labels=chart_labels,
                container_id=container_id,
                prediction_name_key=prediction_name_key,
                prediction_value_key=prediction_value_key,
                prediction_name_value=prediction_name_value,
                width=width,
                height=height,
                xOffset=xOffset,
                yOffset=yOffset
            )
        )

    def add_pie_chart(
        self,
        container_id: str,
        prediction_name_key: str,
        prediction_value_key: str,
        prediction_name_value: str,
        chart_colors: list,
        chart_labels: list,
        display_legend: bool = True,
        legend_icon: str = 'circle',
        width: str = 'auto',
        height: str = 'auto',
        xOffset: str = '0',
        yOffset: str = '0',
        id=None,
        label: str = None,
        chart_name: str = None
    ):
        if id is None:
            id = ''.join(random.choices(string.ascii_letters, k=10))
        if label is None:
            label = id
        if chart_name is None:
            chart_name = id

        self._steps.append(
            PieChartRendering(
                label=label,
                id=id,
                chart_name=chart_name,
                chart_colors=chart_colors,
                chart_labels=chart_labels,
                container_id=container_id,
                prediction_name_key=prediction_name_key,
                prediction_value_key=prediction_value_key,
                prediction_name_value=prediction_name_value,
                display_legend=display_legend,
                legend_icon=legend_icon,
                width=width,
                height=height,
                xOffset=xOffset,
                yOffset=yOffset
            )
        )

    def add_table(
        self,
        container_id: str,
        prediction_name_key: str,
        prediction_value_key: str,
        prediction_name_values: str,
        table_name: str = '',
        id: str = None,
        label: str = None
    ):
        if id is None:
            id = ''.join(random.choices(string.ascii_letters, k=10))
        if label is None:
            label = id

        self._steps.append(
            TableRendering(
                label=label,
                id=id,
                container_id=container_id,
                prediction_name_key=prediction_name_key,
                prediction_value_key=prediction_value_key,
                prediction_name_values=prediction_name_values,
                table_name=table_name
            )
        )

    def to_dict(self):
        return [
            step.to_dict() for step in self.steps
        ]
