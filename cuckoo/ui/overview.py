from gi.repository import Gtk


class OverviewWindow(Gtk.Window):

    def create_alarm_row(self):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        time_label = Gtk.Label(label='12:00')
        switch = Gtk.Switch()

        row.pack_start(switch, expand=False, fill=False, padding=5)
        row.pack_start(time_label, expand=True, fill=True, padding=0)
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
