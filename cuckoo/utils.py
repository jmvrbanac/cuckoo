import os


def get_media_path(media_name):
    current_path = os.path.dirname(__file__)
    rel_path = os.path.join(current_path, '..', 'media', media_name)
    return os.path.abspath(rel_path)
