from urllib import parse

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

Gst.init(None)


class AudioPlayer(object):

    def __init__(self, filename, loop=False):
        self._filename, self._volume = None, 1.0

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
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        self.player.set_property('volume', value)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        parsed = parse.urlparse(value)
        if parsed and not parsed.scheme:
            raise ValueError('Must include a valid uri {}'.format(value))
        self._filename = value
        self.player.set_property('uri', value)

    @property
    def playing(self):
        if not self.player:
            return False

        _, state, pending_state = self.player.get_state(0)
        return state == Gst.State.PLAYING or pending_state == Gst.State.PLAYING
