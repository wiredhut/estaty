from abc import abstractmethod

from estaty.actions import SecondaryAction


class Preset:
    """
    Base class for configuring engine for analysis with desired data
    sources, preprocessing, merging and analysis stages
    """

    @abstractmethod
    def return_final_action(self) -> SecondaryAction:
        """ Return configured pipeline for processing """
        raise NotImplementedError()
