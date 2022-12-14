from abc import abstractmethod
from typing import List, Union

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

        # Data for pools processing - may be none or list with data from
        # previous actions
        self.input_data: Union[List, None] = None
        # Pool with stages to be launched
        self.execution_pool: List = []

    @abstractmethod
    def execute(self):
        """ Start execute all defined processing stages """
        raise NotImplementedError(BASE_EXCEPTION_MESSAGE)


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

    def get_data_from_previous_actions(self):
        """
        There is a need to launch previous actions first and collect data
        from them
        """
        self.input_data = []
        for action in self.from_actions:
            self.input_data.append(action.execute())
