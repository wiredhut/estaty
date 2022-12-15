import pandas as pd
from geopandas import GeoDataFrame

from estaty.engine.vector.vector import prepare_points_layer


def get_pandas_dataframe():
    """ Generate simple pandas DataFrame with point coordinates """
    df = pd.DataFrame({'x': [58.96, 58.97, 58.99],
                       'y': [55.05, 55.06, 55.04],
                       'dummy_value': [0, 1, 2]})

    return df


def test_pandas_to_geo_convert():
    """ Test converting pandas into geopandas """
    df = get_pandas_dataframe()
    gdf = prepare_points_layer(df, lat='y', lon='x')

    assert isinstance(gdf, GeoDataFrame)
