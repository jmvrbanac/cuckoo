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


class AlarmManager(object):

    def __init__(self):
        self.alarms = []
        GObject.timeout_add(1000, self._handle_alarms)

    def add(self, alarm):
        self.alarms.append(alarm)

    def remove(self, alarm):
        self.alarms.remove(alarm)

    def _handle_alarms(self):
        alarms_to_check = [alarm for alarm in self.alarms if alarm.activated]
        for alarm in alarms_to_check:
            if alarm.start_time == utils.get_current_time():
                alarm.sound()
