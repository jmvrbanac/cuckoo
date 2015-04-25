import datetime

from gi.repository import Gtk


class OverviewWindow(Gtk.Window):

    def create_time_label(self, time_obj):
        time_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        time_label, ampm_label = Gtk.Label(), Gtk.Label()

        time_label.set_valign(Gtk.Align.BASELINE)
        ampm_label.set_valign(Gtk.Align.BASELINE)

        time_str = '<span font="sans 30">{}</span>'.format(
            time_obj.strftime('%I:%M')
        )
        ampm_str = '<span font="sans 10">{}</span>'.format(
            time_obj.strftime('%p').lower()
        )

        time_label.set_markup(time_str)
        ampm_label.set_markup(ampm_str)

        time_box.pack_start(time_label, expand=False, fill=True, padding=0)
        time_box.pack_start(ampm_label, expand=False, fill=False, padding=0)
        return time_box

    def create_alarm_row(self):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        time_box = self.create_time_label(datetime.datetime.now())

        switch = Gtk.Switch()
        switch.set_valign(Gtk.Align.CENTER)
        note_label = Gtk.Label()
        note_label.set_markup(
            '<span font_size="medium">{}</span>'.format('Good Morning')
        )

        row.pack_start(time_box, expand=False, fill=True, padding=5)
        row.pack_start(note_label, expand=True, fill=True, padding=0)
        row.pack_start(switch, expand=False, fill=True, padding=5)
        return row

    def __init__(self):
        super().__init__(title='Cuckoo')
        self.set_default_size(400, 200)
        scrolled_window = Gtk.ScrolledWindow()

        alarms = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        for _ in range(5):
            alarms.pack_start(
                self.create_alarm_row(),
                expand=False,
                fill=True,
                padding=5
            )

        scrolled_window.add_with_viewport(alarms)
        self.add(scrolled_window)

        self.connect("delete-event", Gtk.main_quit)
