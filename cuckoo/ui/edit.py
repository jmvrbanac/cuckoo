from gi.repository import Gtk


class EditDialog(Gtk.Dialog):

    def __init__(self, alarm, parent=None):
        super().__init__(title='Edit Alarm', parent=parent)
        self.add_button('Close', Gtk.ResponseType.CLOSE)
        self.connect('response', self.handle_response)

    def handle_response(self, dialog, response_id):
        if (response_id == Gtk.ResponseType.CLOSE or
            response_id == Gtk.ResponseType.DELETE_EVENT):
               self.close()

