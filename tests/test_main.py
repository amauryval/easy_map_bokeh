import pytest


from easy_map_bokeh import EasyMapBokeh
from easy_map_bokeh import ErrorEasyMapBokeh


def test_bokeh_session(width, height):
    my_map = EasyMapBokeh("My beautiful map", width, height)

    assert my_map.figure.plot_height == height
    assert my_map.figure.plot_width == width


def test_bokeh_processing(multipolygons_data, polygons_data, linestrings_data, multilines_data, points_data):
    my_map = EasyMapBokeh("My beautiful map")

    my_map.add_polygons(
        multipolygons_data,
        fill_color="orange",
        legend="MultiPolygons"
    )

    my_map.add_polygons(
        polygons_data,
        fill_color="orange",
        legend="Polygons"
    )

    my_map.add_lines(
        linestrings_data,
        legend="linestrings"
    )

    my_map.add_lines(
        multilines_data,
        color="orange",
        legend="multilinestrings"
    )

    my_map.add_points(
        points_data,
        fill_color="orange",
        legend="points",
        style="diamond"
    )

    assert len(my_map.figure.renderers) == 6
    assert len(my_map.figure.tools) == 10
    assert len(my_map.get_bokeh_layer_containers) == 5


def test_bokeh_processing_with_incompatible_features(mixed_features_data, multilines_data, points_data):
    my_map = EasyMapBokeh("My beautiful map")

    with pytest.raises(ErrorEasyMapBokeh) as exception_returned:
        my_map.add_polygons(
            mixed_features_data,
            fill_color="orange",
            legend="my data"
        )
    assert "layer concerned 'my data'" in str(exception_returned.value)
    assert "geometry not supported by add_polygons()" in str(exception_returned.value)

    with pytest.raises(ErrorEasyMapBokeh) as exception_returned:
        my_map.add_lines(
            mixed_features_data,
            color="orange",
            legend="my data2"
        )
    assert "layer concerned 'my data2'" in str(exception_returned.value)
    assert "geometry not supported by add_lines()" in str(exception_returned.value)

    with pytest.raises(ErrorEasyMapBokeh) as exception_returned:
        my_map.add_points(
            mixed_features_data,
            fill_color="orange",
            legend="my data3"
        )
    assert "layer concerned 'my data3'" in str(exception_returned.value)
    assert "geometry not supported by add_points()" in str(exception_returned.value)

    with pytest.raises(ErrorEasyMapBokeh) as exception_returned:
        my_map.add_points(
            multilines_data,
            fill_color="orange",
            legend="points",
            style="diamond"
        )
    assert "layer concerned 'points'" in str(exception_returned.value)
    assert "geometry not supported by add_points()" in str(exception_returned.value)

    with pytest.raises(ErrorEasyMapBokeh) as exception_returned:
        my_map.add_lines(
            points_data,
            color="orange",
            legend="points2",
        )
    assert "layer concerned 'points2'" in str(exception_returned.value)
    assert "geometry not supported by add_lines()" in str(exception_returned.value)

    with pytest.raises(ErrorEasyMapBokeh) as exception_returned:
        my_map.add_polygons(
            multilines_data,
            fill_color="orange",
            legend="points3",
        )
    assert "layer concerned 'points3'" in str(exception_returned.value)
    assert "geometry not supported by add_polygons()" in str(exception_returned.value)


def test_bokeh_processing_with_gdf_without_crs(polygon_from_coords_without_crs):
    my_map = EasyMapBokeh("My beautiful map")
    with pytest.raises(ValueError) as excinfo:
        my_map.add_polygons(
            polygon_from_coords_without_crs,
            fill_color="purple",
            legend="Tricky Polygons"
        )
    assert 'Cannot transform naive geometries.  Please set a crs on the object first.' in str(excinfo.value)


def test_bokeh_processing_with_layers_with_max_settings(multipolygons_data, polygons_data, linestrings_data, multilines_data, points_data):

    layers_to_add = [
        {
            "input_gdf": multipolygons_data,
            "fill_color": "orange",
            "legend": "MultiPolygons"
        },
        {
            "input_gdf": polygons_data,
            "fill_color": "red",
            "legend": "Polygons"
        },
        {
            "input_gdf": linestrings_data,
            "color": "grey",
            "legend": "linestrings"
        },
        {
            "input_gdf": multilines_data,
            "color": "black",
            "legend": "multilinestrings"
        },
        {
            "input_gdf": points_data,
            "fill_color": "blue",
            "legend": "points",
            "style": "diamond"
        },
    ]
    my_map = EasyMapBokeh("My beautiful map", layers=layers_to_add)

    assert len(my_map.figure.renderers) == 6
    assert len(my_map.figure.tools) == 10
    assert len(my_map.get_bokeh_layer_containers) == 5


def test_bokeh_processing_with_layers_with_min_setting(multipolygons_data, polygons_data, linestrings_data, multilines_data, points_data):

    layers_to_add = [
        {
            "input_gdf": multipolygons_data,
            "legend": "MultiPolygons"
        },
        {
            "input_gdf": polygons_data,
            "legend": "Polygons"
        },
        {
            "input_gdf": linestrings_data,
            "legend": "linestrings"
        },
        {
            "input_gdf": multilines_data,
            "color": "black",
            "legend": "multilinestrings"
        },
        {
            "input_gdf": points_data,
            "legend": "points",
        },
    ]
    my_map = EasyMapBokeh("My beautiful map", layers=layers_to_add)

    assert len(my_map.figure.renderers) == 6
    assert len(my_map.figure.tools) == 10
    assert len(my_map.get_bokeh_layer_containers) == 5


def test_bokeh_processing_with_layers_with_min_setting_and_incompatible_geometry(mixed_features_data, multipolygons_data, polygons_data, linestrings_data, multilines_data, points_data):

    layers_to_add = [
        {
            "input_gdf": multipolygons_data,
            "legend": "MultiPolygons"
        },
        {
            "input_gdf": polygons_data,
            "legend": "Polygons"
        },
        {
            "input_gdf": linestrings_data,
            "legend": "linestrings"
        },
        {
            "input_gdf": multilines_data,
            "color": "black",
            "legend": "multilinestrings"
        },
        {
            "input_gdf": points_data,
            "legend": "points",
        },
        {
            "input_gdf": mixed_features_data,
            "legend": "incompatible_features",
        }
    ]
    with pytest.raises(ErrorEasyMapBokeh) as exception_returned:
        _ = EasyMapBokeh("My beautiful map", layers=layers_to_add)

    assert "geometry have to be split by geometry types (layer concerned 'incompatible_features')" in str(exception_returned.value)

def test_bokeh_processing_with_layers_with_min_setting_and_empty_data(empty_data, multipolygons_data, polygons_data, linestrings_data, multilines_data, points_data):

    layers_to_add = [
        {
            "input_gdf": multipolygons_data,
            "legend": "MultiPolygons"
        },
        {
            "input_gdf": polygons_data,
            "legend": "Polygons"
        },
        {
            "input_gdf": linestrings_data,
            "legend": "linestrings"
        },
        {
            "input_gdf": multilines_data,
            "color": "black",
            "legend": "multilinestrings"
        },
        {
            "input_gdf": points_data,
            "legend": "points",
        },
        {
            "input_gdf": empty_data,
            "legend": "empty_data",
        }
    ]
    with pytest.raises(ErrorEasyMapBokeh) as exception_returned:
        _ = EasyMapBokeh("My beautiful map", layers=layers_to_add)

    assert "Your geodataframe may not have geometry features (layer concerned 'empty_data')" in str(exception_returned.value)


def test_bokeh_structure(multipolygons_data):

    points_input = EasyMapBokeh("hello").get_bokeh_structure_from_gdf(multipolygons_data)
    assert set(points_input.data.keys()) == {"x", "y", "geom_type", "name"}
    assert len(points_input.data.values()) == 4
    for value in points_input.data.values():
        assert isinstance(value, list)
