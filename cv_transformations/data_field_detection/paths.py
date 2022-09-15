import os


def test_file_path(file_name):
    dirname = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dirname, 'test_folder/data', file_name)
    return path


def env_variable_path(file_name):
    dirname = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dirname, file_name)
    return path

