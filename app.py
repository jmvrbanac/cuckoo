from gi.repository import Gtk
from cuckoo.ui import overview

def start_app():
    window = overview.OverviewWindow()
    window.show_all()

    Gtk.main()

if __name__ == '__main__':
    start_app()
