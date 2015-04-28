import datetime
import os
import random

from cuckoo import utils, alarm
from gi.repository import Gtk


class OverviewWindow(Gtk.Window):

    def more_btn_clicked(self, widget):
        print('bam')

    def create_header_bar(self):
        bar = Gtk.HeaderBar()
        bar.set_title('Cuckoo')
        bar.set_show_close_button(True)
        bar.set_property('border-width', 0)

        more_btn = Gtk.Button.new_from_icon_name('view-more-symbolic', 4)
        more_btn.set_relief(Gtk.ReliefStyle.NONE)
        more_btn.connect('clicked', self.more_btn_clicked)
        bar.pack_start(more_btn)
        return bar

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

    def create_alarm_row(self, alarm):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        time_box = self.create_time_label(alarm.start_time)
        more_btn = Gtk.Button.new_from_icon_name('view-more-symbolic', 4)
        more_btn.set_relief(Gtk.ReliefStyle.NONE)

        switch = Gtk.Switch()
        switch.set_valign(Gtk.Align.CENTER)

        note_label = Gtk.Label()
        note_label.set_markup(
            '<span font_size="medium">{}</span>'.format('Good Morning')
        )

        row.pack_start(time_box, expand=False, fill=True, padding=5)
        row.pack_start(note_label, expand=True, fill=True, padding=0)
        row.pack_start(switch, expand=False, fill=True, padding=5)
        row.pack_start(more_btn, expand=False, fill=True, padding=5)
        return row

    def __init__(self):
        super().__init__(title='Cuckoo')
        self.set_default_size(500, 345)
        self.set_border_width(1)
        self.set_titlebar(self.create_header_bar())
        self.alarm_manager = alarm.AlarmManager()

        # TODO(jmvrbanac): Fix icon sourcing
        icon_path = utils.get_media_path('clock.svg')
        if os.path.exists(icon_path):
            self.set_default_icon_from_file(icon_path)

        scrolled_window = Gtk.ScrolledWindow()
        alarms = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        for _ in range(1):
            alarm_obj = alarm.Alarm(
                utils.format_time_str('11:20 pm'),
                utils.get_media_path('alarm.wav')
            )
            alarms.pack_start(
                self.create_alarm_row(alarm_obj),
                expand=False,
                fill=True,
                padding=5
            )

        scrolled_window.add_with_viewport(alarms)
        self.add(scrolled_window)

        self.connect("delete-event", Gtk.main_quit)
