from gi.repository import Gtk


class EditDialog(Gtk.Dialog):

    def __init__(self, alarm, parent=None):
        super().__init__(title='Edit Alarm', parent=parent)
        self.set_default_size(200, 200)
        self.alarm = alarm

        layout = self.get_content_area()
        layout.add(self.build_edit_time_button_row())

        self.add_button('Close', Gtk.ResponseType.CLOSE)
        self.connect('response', self.handle_response)

        self.show_all()

    def build_edit_time_button_row(self):
        time_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hour_spinner = Gtk.SpinButton.new_with_range(1, 12, 1)
        minute_spinner = Gtk.SpinButton.new_with_range(0, 60, 1)

        hour, minute, ampm = self.alarm.time_tuple
        hour_spinner.set_value(hour)
        minute_spinner.set_value(minute)

        time_row.pack_start(hour_spinner, True, False, 0)
        time_row.pack_start(minute_spinner, True, False, 0)
        return time_row

    def handle_response(self, dialog, response_id):
        if (response_id == Gtk.ResponseType.CLOSE or
            response_id == Gtk.ResponseType.DELETE_EVENT):
               self.close()

