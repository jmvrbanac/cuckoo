from gi.repository import GObject
from cuckoo import player, utils


class Alarm(object):
    def __init__(self, start_time, filename, loop=True):
        self.player = player.AudioPlayer(filename, loop)
        self.start_time = start_time
        self.activated = False

    def sound(self):
        self.player.play()

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False
        self.player.stop()

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
