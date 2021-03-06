from typing import List

from shapely.geometry import base
from shapely.geometry import Point
from shapely.geometry import MultiPoint

from shapely.geometry import LineString
from shapely.geometry import LinearRing
from shapely.geometry import MultiLineString

from shapely.geometry import Polygon
from shapely.geometry.polygon import InteriorRingSequence
from shapely.geometry import MultiPolygon

from shapely.geometry import GeometryCollection

import pandas as pd
import geopandas as gpd
from shapely.wkt import loads


def geometry_2_bokeh_format(geometry: base, coord_name: str = "xy") -> List:
    """
    geometry_2_bokeh_format
    Used for bokeh library

    :type geometry: shapely.geometry.*
    :type coord_name: str, default: xy (x or y)
    :return: float or list of tuple
    """
    coord_values: List = []
    if isinstance(geometry, Point):
        if coord_name != "xy":
            coord_values = getattr(geometry, coord_name)
        else:
            coord_values = next(iter(geometry.coords))

    elif isinstance(geometry, Polygon):
        exterior = [geometry_2_bokeh_format(geometry.exterior, coord_name)]
        interiors = geometry_2_bokeh_format(geometry.interiors, coord_name)
        coord_values = [exterior, interiors]
        if len(interiors) == 0:
            coord_values = [exterior]

    elif isinstance(geometry, (LinearRing, LineString)):
        coord_values = [
            geometry_2_bokeh_format(Point(feat), coord_name) for feat in geometry.coords
        ]

    if isinstance(geometry, (MultiPolygon, MultiLineString)):
        for feat in geometry.geoms:
            if isinstance(feat, Point):
                coord_values.append([geometry_2_bokeh_format(feat, coord_name)])
            else:
                coord_values.extend(geometry_2_bokeh_format(feat, coord_name))

    if isinstance(geometry, MultiPoint):
        raise ValueError(
            "no interest to handle MultiPoint, it's very tricky to support point simple points and multipoints"
        )

    if isinstance(geometry, InteriorRingSequence):
        # compute holes
        coord_values.extend(
            [geometry_2_bokeh_format(feat, coord_name) for feat in geometry]
        )

    if isinstance(geometry, GeometryCollection):
        raise ValueError("no interest to handle GeometryCollection")

    return coord_values


def wkt_to_gpd(geom_wkt, geom_epsg=3857):
    df = pd.DataFrame([{
        "geometry": loads(geom_wkt),
    }])
    geometry = df["geometry"]
    properties = df.drop(columns=["geometry"])

    return gpd.GeoDataFrame(
        properties,
        geometry=geometry,
        crs=f"EPSG:{geom_epsg}"
    )