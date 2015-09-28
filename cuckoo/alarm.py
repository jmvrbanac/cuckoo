from gi.repository import GObject
from cuckoo import player, utils


class Alarm(object):
    def __init__(self, start_time, filename, loop=True, activated=False,
                 note=''):
        self.player = player.AudioPlayer(filename, loop)
        self.start_time = start_time
        self.activated = activated
        self.note = note

    def sound(self):
        self.player.play()

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False
        self.player.stop()

    def to_dict(self):
        return {
            'time': utils.time_to_str(self.start_time),
            'uri': self.filename,
            'active': self.activated,
            'note': self.note
        }

    @classmethod
    def from_dict(cls, alarm_dict):
        return cls(
            start_time=utils.format_time_str(alarm_dict.get('time')),
            filename=alarm_dict.get('uri'),
            activated=alarm_dict.get('active'),
            note=alarm_dict.get('note')
        )

    @property
    def filename(self):
        return self.player.filename

    @filename.setter
    def filename(self, value):
        self.player.filename = value

    @property
    def time_tuple(self):
        hour, minute, ampm = self.start_time.strftime('%I|%M|%p').split('|')
        return int(hour), int(minute), ampm


class AlarmManager(object):

    def __init__(self):
        self.alarms = []
        self._handle_alarms()

    def add(self, alarm):
        self.alarms.append(alarm)

    def remove(self, alarm):
        alarm.deactivate()
        self.alarms.remove(alarm)

    def _handle_alarms(self):
        alarms_to_check = [alarm for alarm in self.alarms if alarm.activated]
        for alarm in alarms_to_check:
            if alarm.start_time == utils.get_current_time():
                if not alarm.player.playing:
                    alarm.sound()

        GObject.timeout_add(1000, self._handle_alarms)
