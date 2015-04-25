import gi
gi.require_version('Gst', '1.0')

from gi.repository import Gst

Gst.init(None)


class AudioPlayer(object):

    def __init__(self, filename, loop=False):
        self.player = Gst.ElementFactory.make('playbin', 'player');
        self.loop = loop
        self.volume = 1.0
        self.filename = filename

        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message::eos", self.eos_callback)

    def play(self):
        self.player.set_state(Gst.State.PLAYING)

    def stop(self):
        self.player.set_state(Gst.State.NULL)

    def eos_callback(self, bus, message):
        self.stop()
        if self.loop:
            self.play()

    @property
    def volume(self):
        self.player.get_property('volume')

    @volume.setter
    def volume(self, value):
        self.player.set_property('volume', value)

    @property
    def filename(self):
        self.player.get_property('filename')

    @filename.setter
    def filename(self, value):
        self.player.set_property('uri', value)

    @property
    def playing(self):
        if not self.player:
            return False

        _, state = self.player.get_state(0)
        return state == Gst.State.PLAYING
