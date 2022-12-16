import numpy as np

from estaty.data_source.load.osm_vector_utils import convert_osm_bbox_coordinates
from estaty.engine.vector.crop import crop_points_by_polygon
from estaty.engine.vector.convert import prepare_points_layer
from tests.vector.test_convert import get_pandas_dataframe


def test_crop_point_dataframe():
    """ Check dataframe cropping operation """
    gdf = prepare_points_layer(get_pandas_dataframe(), lat='y', lon='x')
    # Generate polygon
    polygon = convert_osm_bbox_coordinates([55.055, 55.03, 58.95, 59.00])

    cropped = crop_points_by_polygon(gdf, polygon)

    assert len(cropped) == 2
    assert np.isclose(cropped['x'].iloc[0], 58.96)
    assert np.isclose(cropped['y'].iloc[0], 55.05)
