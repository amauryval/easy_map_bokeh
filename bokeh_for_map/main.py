from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.tile_providers import get_provider
from bokeh.tile_providers import CARTODBPOSITRON
from bokeh.models import HoverTool

from bokeh_for_map.helpers.geometry import geometry_2_bokeh_format

from bokeh_for_map.helpers.settings import expected_node_style


class BokehForMap:

    def __init__(self, title="My empty Map", width=800, height=600, background_map=CARTODBPOSITRON):
        super().__init__()

        self.figure = figure(
            title=title,
            output_backend="webgl",
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )

        self.figure.plot_width = width
        self.figure.plot_height = height

        self._add_background_map(background_map)

    def _add_background_map(self, map_name_object):
        tile_provider = get_provider(map_name_object)
        self.figure.add_tile(tile_provider)

    def _set_tooltip_from_features(self, features, rendered):
        column_tooltip = self.__build_column_tooltip(features)
        self.figure.add_tools(HoverTool(
            tooltips=column_tooltip,
            renderers=[rendered],
            mode="mouse"
        ))

    @staticmethod
    def format_features(features):
        """
        To build the bokeh data structure from a geodataframe.
        "format" key is useful if you want to work with some widgets
        "data" key contaings all data to plot them

        :param features: your input geodataframe
        :type features: geopandas.GeoDataFrame
        :return: the bokeh data and its structure
        :rtype: dict with following keys : "data", "format"
        """
        bokeh_data = ColumnDataSource({
            **{
                "x": features['geometry'].apply(lambda x: geometry_2_bokeh_format(x, 'x')).tolist(),
                "y": features['geometry'].apply(lambda x: geometry_2_bokeh_format(x, 'y')).tolist(),

            },
            **{
                column: features[column].to_list()
                for column in features.columns
                if column != "geometry"
            }
        })
        return {
            "data": bokeh_data,
            "format": ColumnDataSource(data={
                attribute_name: []
                for attribute_name in bokeh_data.data.keys()
            })
        }


    def add_lines(self, features, legend, color="blue", line_width=2):
        """
        To add a lines layer on bokeh Figure

        :param features: your input geodataframe
        :type features: geopandas.GeoDataFrame
        :param legend: layer name
        :type legend: str
        :param color: color value
        :type color: str
        :param line_width: line width
        :type line_width: int
        """
        rendered = self.figure.multi_line(
            xs="x",
            ys="y",
            legend_label=legend,
            line_color=color,
            line_width=line_width,
            source=features,
        )
        self._set_tooltip_from_features(features, rendered)

    def add_points(self, features, legend, fill_color="red", size=4, style="circle"):
        """
        To add a points layer on bokeh Figure

        :param features: ColumnDataSource
        :type features: ColumnDataSource
        :param legend: layer name
        :type legend: str
        :param color: color value
        :type color: str
        :param size: node size
        :type size: int
        :param style: node style, check expected_node_style variable
        :type style: str
        """
        assert style in expected_node_style, f"{style} not supported. Choose one of them : {', '.join(expected_node_style)}"
        rendered = getattr(self.figure, style)(
            x="x",
            y="y",
            color=fill_color,
            size=size,
            legend_label=legend,
            source=features,
        )
        self._set_tooltip_from_features(features, rendered)

    def add_polygons(self, features, legend, fill_color="red"):
        """
        To add a polygons layer on bokeh Figure

        :param features: your input geodataframe
        :type features: geopandas.GeoDataFrame
        :param legend: layer name
        :type legend: str
        :param fill_color: color value
        :type fill_color: str
        """
        rendered = self.figure.multi_polygons(
            xs="x",
            ys="y",
            legend_label=legend,
            fill_color=fill_color,
            source=features,
        )
        self._set_tooltip_from_features(features, rendered)

    def __build_column_tooltip(self, features):
        columns = list(filter(lambda x: x not in ["x", "y"], features.data.keys()))
        return list(zip(map(lambda x: str(x.upper()), columns), map(lambda x: f"@{x}", columns)))
