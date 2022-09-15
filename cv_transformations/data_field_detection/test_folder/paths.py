import os


def get_data_field_detection_path(file_name):
    dirname = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dirname, 'data', file_name)