from gi.repository import Gtk
from cuckoo import utils


class EditDialog(Gtk.Dialog):

    def __init__(self, alarm, parent=None):
        super().__init__(title='Edit Alarm', parent=parent)
        self.set_default_size(200, 200)
        self.alarm = alarm

        self.sound_file_chooser = Gtk.FileChooserButton(title='Choose Sound File')
        file_filter = Gtk.FileFilter()
        file_filter.set_name('Sound Files')
        file_filter.add_pattern('*.wav')
        file_filter.add_pattern('*.mp3')
        file_filter.add_pattern('*.ogg')
        self.sound_file_chooser.add_filter(file_filter)
        self.sound_file_chooser.set_uri(self.alarm.filename)

        layout = self.get_content_area()
        audio_file_label = Gtk.Label('Audio File', xalign=0, xpad=5)
        alarm_time_label = Gtk.Label('Alarm Time', xalign=0, xpad=5)
        layout.pack_start(audio_file_label, True, False, 5)
        layout.pack_start(self.sound_file_chooser, False, True, 5)
        layout.pack_start(alarm_time_label, True, False, 5)
        layout.pack_start(self.build_edit_time_button_row(), False, False, 5)

        self.add_button('Close', Gtk.ResponseType.CLOSE)
        self.connect('response', self.handle_response)

        self.show_all()

    def build_edit_time_button_row(self):
        time_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hour_spinner = Gtk.SpinButton.new_with_range(1, 12, 1)
        minute_spinner = Gtk.SpinButton.new_with_range(0, 60, 1)
        ampm_box = Gtk.ComboBoxText()
        ampm_box.append_text('AM')
        ampm_box.append_text('PM')

        hour, minute, ampm = self.alarm.time_tuple
        hour_spinner.set_value(hour)
        minute_spinner.set_value(minute)
        ampm_box.set_active(0 if ampm == 'AM' else 1)

        time_row.pack_start(hour_spinner, True, True, 5)
        time_row.pack_start(minute_spinner, True, True, 5)
        time_row.pack_start(ampm_box, True, True, 5)

        self.hour_spinner = hour_spinner
        self.minute_spinner = minute_spinner
        self.ampm_box = ampm_box
        return time_row

    @property
    def selected_filename(self):
        return self.sound_file_chooser.get_uri()

    @property
    def ui_input_time(self):
       time_str = '{hour}:{minute} {ampm}'.format(
           hour=int(self.hour_spinner.get_value()),
           minute=int(self.minute_spinner.get_value()),
           ampm='AM' if self.ampm_box.get_active() == 0 else 'PM'
       )
       return utils.format_time_str(time_str)

    def handle_response(self, dialog, response_id):
        if (response_id == Gtk.ResponseType.CLOSE or
            response_id == Gtk.ResponseType.DELETE_EVENT):
               self.close()
