from estaty.data.data import VectorData


class NodesExtractor:
    """
    Class for nodes data extraction from each spatial object from vector data
    TODO we may remove such a class
    """

    def __init__(self, vector_data: VectorData):
        self.vector_data = vector_data

    def iter_objects(self):
        """ Return list with nodes for each vector spatial object """
        nodes_to_return = []
        if self.vector_data.polygons is not None:
            for row_id, row in self.vector_data.polygons.iterrows():
                nodes = row['nodes']
                if isinstance(nodes, str):
                    nodes = convert_string_into_list(nodes)

                nodes_to_return.append(nodes)

        for nodes in nodes_to_return:
            yield nodes


def convert_string_into_list(cell: str):
    """
    Take value from cell as string and transform into list. For example,
    convert '[0, 1, 2, 3]' into [0, 1, 2, 3]
    """
    cell = cell.replace('[', '')
    cell = cell.replace(']', '')
    values = cell.split(',')
    values = list(map(lambda x: int(x), values))
    return values
