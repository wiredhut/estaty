from typing import Union

from estaty.actions import Action
from estaty.data.data import CommonData


class DataSource(Action):
    """ Class for getting data from open (and other) sources and saving it """

    def __init__(self, action_name: str, params: dict = None):
        super().__init__(action_name, params)

    def execute(self, input_data: Union[CommonData, None] = None):
        """ Launch stages in execution pool """
        self.params['object_for_analysis'] = self.object_for_analysis

        for stage in self.execution_pool:
            stage = stage(**self.params)
            input_data = stage.apply(input_data)

        return input_data
