from pathlib import Path


def get_project_path() -> Path:
    return Path(__file__).parent.parent


def get_tmp_folder_path() -> Path:
    """
    Return path to the temporary folder where different files can be stored
    """
    return Path(get_project_path(), 'estaty', 'tmp')


def get_local_files_storage_path() -> Path:
    """
    Return path to the folder where different files saved for model processing
    """
    return Path(get_project_path(), 'estaty', 'repository', 'local_data')
