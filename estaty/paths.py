from pathlib import Path


def get_project_path() -> Path:
    return Path(__file__).parent.parent


def get_tmp_folder_path() -> Path:
    """ Return path to folder where different files can be stored """
    return Path(get_project_path(), 'estaty', 'tmp')
