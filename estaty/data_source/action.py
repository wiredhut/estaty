from estaty.action import Action


class DataSource(Action):
    """ Class for getting data from open (and other) sources and saving it """

    def __init__(self, action_name: str, params: dict = None):
        super().__init__(action_name, params)

    def execute(self):
        pass
