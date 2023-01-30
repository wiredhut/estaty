from abc import abstractmethod
from typing import List, Union, Any, Callable

from estaty.data.data import CommonData
from estaty.repository.labels import DATA_SOURCE_POOL_BY_NAME

BASE_EXCEPTION_MESSAGE = 'Does not support action execution for base class'


class Action:
    """
    Base class for creating actions for analysis

    Responsibility zone: Group stages in execution pool and launch lower
    abstractions
    """

    def __init__(self, action_name: str, params: dict = None):
        self.action_name = action_name
        self.params = params
        if self.params is None:
            self.params = {}

        # Pool with stages to be launched
        self.execution_pool: Union[List, Callable] = DATA_SOURCE_POOL_BY_NAME[action_name]

        # Object for analysis
        self.object_for_analysis = None

    @abstractmethod
    def execute(self):
        """ Start execute all defined processing stages """
        raise NotImplementedError(BASE_EXCEPTION_MESSAGE)

    def set_object(self, object_for_analysis: Any):
        self.object_for_analysis = object_for_analysis


class SecondaryAction(Action):
    """ Base class for actions, which must be applied after others actions """

    def __init__(self, action_name: str, params: dict = None,
                 from_actions: List[Action] = None):
        super().__init__(action_name, params)
        # List with actions to be executed before launching current action
        self.from_actions = from_actions

    @abstractmethod
    def execute(self):
        """ Start execute all defined processing stages """
        raise NotImplementedError(BASE_EXCEPTION_MESSAGE)

    def execute_previous_actions(self) -> List[CommonData]:
        """
        There is a need to launch previous actions first and collect data
        from them
        """
        output_from_previous_actions = []
        for action in self.from_actions:
            # Transform data in action and return updated version
            input_data = action.execute()
            # Action may return list with outputs
            if isinstance(input_data, list):
                output_from_previous_actions.extend(input_data)
            else:
                output_from_previous_actions.append(input_data)

        return output_from_previous_actions

    def set_object(self, object_for_analysis: Any):
        """ Set estate object for analysis """
        self.object_for_analysis = object_for_analysis
        for action in self.from_actions:
            action.set_object(object_for_analysis)
