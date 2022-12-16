from estaty.data.data import VectorData


class VectorToPointsRepresentation:
    """
    Class for processing geopandas dataframes and transform each geometry type
    (point, line, polygon or multipolygon) into points. So polygon can be
    represented as single point.
    """

    def __init__(self):
        pass


def get_nearest_nodes_from_layer(vector_data: VectorData,
                                 object_for_analysis: dict):
    """
    For each polygon, point or line layer in VectorData get node which is the
    nearest to target coordinate. The aim of this function to represent polygon
    or line with one value and one spatial location (node)
    """
    pass
