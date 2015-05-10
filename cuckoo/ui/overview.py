import datetime
import os
import random

from cuckoo import utils, alarm
from cuckoo.ui import edit
from gi.repository import Gtk, Gio

alarm_manager = alarm.AlarmManager()


class TimeText(Gtk.Box):
    def __init__(self, time):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.time_label, self.ampm_label = Gtk.Label(), Gtk.Label()
        self.time = time

        self.time_label.set_valign(Gtk.Align.BASELINE)
        self.ampm_label.set_valign(Gtk.Align.BASELINE)

        self.pack_start(self.time_label, expand=False, fill=True, padding=0)
        self.pack_start(self.ampm_label, expand=False, fill=False, padding=0)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        time_str = '<span font="sans 30">{}</span>'.format(
            value.strftime('%I:%M')
        )
        ampm_str = '<span font="sans 10">{}</span>'.format(
            value.strftime('%p').lower()
        )

        self.time_label.set_markup(time_str)
        self.ampm_label.set_markup(ampm_str)


class AlarmRow(Gtk.Box):
    def __init__(self, alarm, note='', parent=None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.parent = parent
        self.time_text = TimeText(alarm.start_time)
        self.note_label = Gtk.Label()
        self.note = note
        self.alarm = alarm

        more_btn = Gtk.Button.new_from_icon_name('view-more-symbolic', 4)
        more_btn.set_relief(Gtk.ReliefStyle.NONE)
        popover = self._build_popover(more_btn)
        more_btn.connect('clicked', lambda x: popover.show_all())

        switch = Gtk.Switch()
        switch.set_valign(Gtk.Align.CENTER)
        switch.connect('state-set', self.switch_toggled)

        self.pack_start(self.time_text, expand=False, fill=True, padding=5)
        self.pack_start(self.note_label, expand=True, fill=True, padding=0)
        self.pack_start(switch, expand=False, fill=True, padding=5)
        self.pack_start(more_btn, expand=False, fill=True, padding=5)

    def switch_toggled(self, switch, state):
        if state:
            self.alarm.activate()
        else:
            self.alarm.deactivate()

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, value):
        self._note = value
        self.note_label.set_markup(
            '<span font_size="medium">{}</span>'.format(value)
        )

    def _build_popover(self, parent):
        edit_btn = Gtk.Button(label='Edit')
        delete_btn = Gtk.Button(label='Delete')
        edit_btn.set_relief(Gtk.ReliefStyle.NONE)
        delete_btn.set_relief(Gtk.ReliefStyle.NONE)

        popover = Gtk.Popover.new(parent)
        popover.set_size_request(75, 100)
        popover_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        popover_container.pack_start(edit_btn, False, False, 5)
        popover_container.pack_start(delete_btn, False, False, 5)
        popover.add(popover_container)

        def edit_clicked(widget):
            def dialog_closed(dialog, response_id):
                if response_id == Gtk.ResponseType.CLOSE:
                    # Refresh stored and presented time
                    self.alarm.start_time = dialog.ui_input_time
                    self.time_text.time = self.alarm.start_time

            popover.hide()
            dialog = edit.EditDialog(self.alarm, parent=self.parent)
            dialog.connect('response', dialog_closed)
            dialog.show()

        def delete_clicked(widget):
            self.parent.alarms_box.remove(self)
            alarm_manager.remove(self.alarm)
            popover.hide()

        edit_btn.connect('clicked', edit_clicked)
        delete_btn.connect('clicked', delete_clicked)
        return popover


class OverviewWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title='Cuckoo')
        self.set_default_size(500, 345)
        self.set_border_width(1)
        self.set_titlebar(self.create_header_bar())

        # TODO(jmvrbanac): Fix icon sourcing
        icon_path = utils.get_media_path('clock.svg')
        if os.path.exists(icon_path):
            self.set_default_icon_from_file(icon_path)

        scrolled_window = Gtk.ScrolledWindow()
        self.alarms_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Adding a couple test alarm rows
        for _ in range(2):
            alarm_obj = alarm.Alarm(
                utils.get_current_time(),
                utils.get_media_uri('alarm.wav')
            )
            alarm_manager.add(alarm_obj)
            self.alarms_box.pack_start(
                AlarmRow(alarm_obj, 'Hello World', self),
                expand=False,
                fill=True,
                padding=5
            )

        scrolled_window.add_with_viewport(self.alarms_box)
        self.add(scrolled_window)

        self.connect("delete-event", Gtk.main_quit)

    def create_header_bar(self):
        bar = Gtk.HeaderBar()
        bar.set_title('Cuckoo')
        bar.set_show_close_button(True)
        bar.set_property('border-width', 0)

        more_btn = Gtk.Button.new_from_icon_name('view-more-symbolic', 4)
        more_btn.set_relief(Gtk.ReliefStyle.NONE)
        bar.pack_start(more_btn)
        return bar
