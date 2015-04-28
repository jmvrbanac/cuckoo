import os
from datetime import datetime


def get_media_path(media_name):
    current_path = os.path.dirname(__file__)
    rel_path = os.path.join(current_path, '..', 'media', media_name)
    return os.path.abspath(rel_path)

def format_time_str(time_str):
    return datetime.strptime(time_str, '%I:%M %p')

def time_to_str(time_obj):
    return time_obj.strftime('%I:%M %p')

def get_current_time():
    return time.strftime('%I:%M %p')
