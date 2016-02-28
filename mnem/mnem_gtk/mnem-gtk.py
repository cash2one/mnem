'''
Created on 26 Feb 2016

@author: John Beard
'''

from mnem_rest_client import client

import signal
import sys

from gi import require_version

require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GdkPixbuf
from gi.repository import GObject

from gi.repository import Pango

import webbrowser


class ResultContainer(Gtk.HBox):

    def __init__(self, result):
        super(ResultContainer, self).__init__(
            name="result"
        )

        self.selected = False
        self.set_homogeneous(False)

        try:
            self.url = result["url"]
        except KeyError:
            pass

        self.keyword = result["keyword"]

        keyword = Gtk.Label(result["keyword"])
        keyword.set_justify(Gtk.Justification.LEFT)

        self.pack_start(keyword, expand=False, fill=True, padding=0)

        urlLabel = Gtk.Label(self.url)
        urlLabel.set_justify(Gtk.Justification.LEFT)
        urlLabel.set_ellipsize(Pango.EllipsizeMode.MIDDLE)

        self.pack_end(urlLabel, expand=False, fill=True, padding=100)

        self.set_can_focus(True)

        self.connect("focus-in-event", self.on_focus)
        self.connect("key-press-event", self.on_keypress)

    def on_focus(self, widget, ev):

        print(self.is_focus(), self.keyword)

    def on_keypress(self, widget, ev):

        if ev.keyval == Gdk.KEY_Return:
            print(ev, self.keyword)

            self.perform_main_action()

    def perform_main_action(self):

        if self.url:

            webbrowser.open(self.url, new=2, autoraise=True)


class ResultListBox(Gtk.VBox):

    def __init__(self):
        super(ResultListBox, self).__init__()

        self.results = []
        self.reset()

    def clear(self):

        for r in self.results:
            r.destroy()

        self.results.clear()

        self.reset()

    def reset(self):
        self.focussed = -1

    def add_completion(self, c):

        resCont = ResultContainer(c)

        self.results.append(resCont)

        self.pack_start(resCont, expand=False, fill=False, padding=0)
        resCont.show()

    def select_next(self):

        if self.focussed >= 0:
            self.results[self.focussed].select(False)

        self.focussed += 1

        if self.focussed >= len(self.results):
            self.focussed = 0

        self.results[self.focussed].select(True)


class MnemAppWindow(Gtk.Window):

    def __init__(self, client):
        super(MnemAppWindow, self).__init__(name="Mnem")

        self.client = client
        self.connect("destroy", self.stop)

        style_provider = Gtk.CssProvider()

        css = """
#result:focus{
    background-color: #77f;
}
"""

        style_provider.load_from_data(bytes(css.encode()))

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.create_layout()

        self.show_all()

    def bind_signals(self):
        signal.signal(signal.SIGINT, self.signal_stop_received)  # 9
        signal.signal(signal.SIGTERM, self.signal_stop_received)  # 15

    def signal_stop_received(self, *args):
        self.stop()

    def signal_stop_received(self, *args):
        self.stop()

    def start(self):
        self.bind_signals()

        # https://bugzilla.gnome.org/show_bug.cgi?id=622084
        # so don't just use Gtk.main()
        try:
            GLib.MainLoop().run()
        except KeyboardInterrupt:
            pass

    def stop(self, *args):
        GLib.MainLoop().quit()
        sys.exit(0)

    def create_layout(self):

        self.main_box = Gtk.VBox()

        main_input = Gtk.Entry()
        main_input.connect('changed', self.search_changed)

        self.main_box.pack_start(
            main_input, expand=False, fill=False, padding=0)

        self.completions = ResultListBox()
        self.main_box.add(self.completions)

        self.add(self.main_box)

        #self.connect('key-press-event', self.key_press)

    def key_press(self, widget, event):

        if event.keyval == Gdk.KEY_Tab:
            self.handle_tab()

    def handle_tab(self):
        print("Tab")
        self.completions.select_next()

    def search_changed(self, entry):

        search = entry.get_text()

        parts = search.split(" ", 1)

        if not parts:
            return

        if len(parts) == 1:
            key = "Default"  # TODO
            query = parts[0]
        else:
            key = parts[0]
            query = parts[1]

        self.perform_search(key, query)

    def perform_search(self, key, query):

        # TODO
        key_map = {
            "g": "google",
            "a": "amazon",
            "f": "farnell",
            "b": "baidu",
        }

        try:
            key = key_map[key]
        except KeyError:
            key = "google"

        try:
            comps = self.client.getCompletions(key, None, query)
        except:
            raise

        if len(comps) == 0:
            return

        self.handle_completions(comps)

    def handle_completions(self, comps):

        if "completions" not in comps:
            return

        self.completions.clear()

        for c in comps["completions"]:
            self.completions.add_completion(c)

        self.completions.show_all()


class MnemGtk(object):
    '''
    GTK frontend for the Mnem REST client
    '''

    def __init__(self):
        '''
        Constructor
        '''
        port = 27183
        url = "http://localhost:%d" % (port)

        self.client = client.MnemRestClient(url)

        self.client.connect()

        self.window = MnemAppWindow(self.client)

        # enter the GUI loop
        self.window.start()


if __name__ == "__main__":

    print("Mnem GTK")

    mnemGtk = MnemGtk()
