import shutil
from pathlib import Path
from typing import Union

from estaty.paths import get_tmp_folder_path


class TemporaryFolderExplorer:
    """
    Class for creating and monitoring temporary folder during module
    execution
    """

    def __init__(self):
        self.tmp_folder = get_tmp_folder_path()
        if self.tmp_folder.is_dir() is False:
            self.tmp_folder.mkdir(exist_ok=True, parents=True)

        self.non_removing_tmp = Path(self.tmp_folder, 'non_removing')
        if self.non_removing_tmp.is_dir() is False:
            self.non_removing_tmp.mkdir(exist_ok=True, parents=True)

        # Clear before each launch
        self.removing_tmp = Path(self.tmp_folder, 'removing')
        if self.removing_tmp.is_dir() is True:
            shutil.rmtree(self.removing_tmp)
            # Create it one
            self.removing_tmp.mkdir(exist_ok=True, parents=True)

    def add_file_non_removing_folder(self, file_to_save: Union[str, Path, None] = None):
        """
        Generate temporary file into non-removing folder. Non-removing folder
        means that it will not cleaned automatically.
        """
        raise NotImplementedError(f'Does not support folder creation yet')
