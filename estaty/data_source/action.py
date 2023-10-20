from estaty.actions import Action


class DataSource(Action):
    """ Class for getting data from open (and other) sources and saving it

    :param action_name: name of data source action to use.
    Possible variants:
        * 'osm' - Open Street Map data loader.
        Support the following configurations:
        {'category': 'water'} to load water objects geometries,
        {'category': 'park'} to load parks objects geometries,
        {'category': 'light'} to load streetlights objects geometries
        {'category': 'municipality'} to load municipality borders geometries
        {'category': 'school'} to load schools objects geometries
        {'category': 'driving_school'} to load driving school objects geometries
        {'category': 'bar'} to load bar objects geometries
        {'category': 'waste_disposal'} to load waste disposal objects geometries
        {'category': 'toilet'} to load toilet objects geometries
        {'category': 'police'} to load police objects geometries

        * 'csv' - csv file with coordinates
        * 'gpkg' - gpkg file
    """

    def __init__(self, action_name: str, params: dict = None):
        super().__init__(action_name, params)

    def execute(self):
        """ Launch stages in execution pool """
        self.params['object_for_analysis'] = self.object_for_analysis

        input_data = None
        for stage in self.execution_pool:
            stage = stage(**self.params)
            input_data = stage.apply(input_data)

        description = f'Data retrieved from DataSource action {self.action_name}' \
                      f' with parameters {str(self.params)}'
        input_data.description = description
        return input_data
