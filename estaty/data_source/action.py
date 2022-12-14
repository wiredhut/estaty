from typing import Union

from estaty.actions import Action
from estaty.data.data import CommonData
from estaty.repository.labels import DATA_SOURCE_POOL_BY_NAME


class DataSource(Action):
    """ Class for getting data from open (and other) sources and saving it """

    def __init__(self, action_name: str, params: dict = None):
        super().__init__(action_name, params)

        # Get list with actions to perform
        self.execution_pool = DATA_SOURCE_POOL_BY_NAME[action_name]

    def execute(self, input_data: Union[CommonData, None] = None):
        """ Launch stages in execution pool """
        # Set location to params
        self.params['location'] = self.object_for_analysis['location']

        for stage in self.execution_pool:
            stage = stage(**self.params)
            input_data = stage.apply(input_data)

        return input_data
