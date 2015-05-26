from collections import namedtuple
from cuckoo import utils, alarm
import os
import json


class CuckooConfig(object):
    default_filename = os.path.join(
        os.path.expanduser('~'),
        '.config',
        'cuckoo.json'
    )

    def __init__(self):
        self.filename = self.default_filename
        self.default_alarm_uri = utils.get_media_uri('alarm.wav')
        self.alarms = []

    @classmethod
    def load(cls, filename=None):
        cfg = cls()
        real_path = filename or cls.default_filename
        if not os.path.exists(real_path):
            print("Couldn't load config... Creating a new config")
            cfg.save()
            return cfg

        with open(real_path, 'r') as config_file:
            json_dict = json.load(config_file)

            cfg.default_alarm_uri = json_dict.get('default_alarm_uri', '')
            cfg.alarms = [alarm.Alarm.from_dict(alarm_data)
                          for alarm_data in json_dict.get('alarms', [])]
        return cfg

    def save(self, filename=None):
        real_path = filename or self.filename

        with open(real_path, 'w+') as config_file:
            config_dict = {
                'default_alarm_uri': self.default_alarm_uri,
                'alarms': []
            }
            json.dump(config_dict, config_file, indent=4)
