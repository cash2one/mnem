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

    def __init__(self, result, selected_listener):
        super(ResultContainer, self).__init__(
            name="result"
        )

        self.selected_listener = selected_listener
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

        # self.set_can_focus(True)

        # self.connect("focus-in-event", self.on_focus)

    def select(self, selected):

        if selected:
            self.get_style_context().add_class("selected")
            self.selected_listener.keyword_selected(self.keyword)
        else:
            self.get_style_context().remove_class("selected")

    def perform_main_action(self):

        if self.url:

            webbrowser.open(self.url, new=2, autoraise=True)


class ResultListBox(Gtk.VBox):

    def __init__(self, selection_listener):
        super(ResultListBox, self).__init__()

        self.selection_listener = selection_listener
        self.results = []
        self.reset()

    def clear(self):

        for r in self.results:
            r.destroy()

        self.results = []

        self.reset()

    def reset(self):
        self.focussed = -1

    def add_completion(self, c):

        resCont = ResultContainer(c, self.selection_listener)

        self.results.append(resCont)

        self.pack_start(resCont, expand=False, fill=False, padding=0)
        resCont.show()

    def confirm_entry(self):

        try:
            self.results[self.focussed].perform_main_action()
        except IndexError:
            pass

    def select_next(self):

        try:
            self.results[self.focussed].select(False)
        except IndexError:
            pass

        self.focussed += 1

        if self.focussed >= len(self.results):
            self.focussed = 0

        if self.focussed < len(self.results):
            self.results[self.focussed].select(True)

    def select_prev(self):

        try:
            self.results[self.focussed].select(False)
        except IndexError:
            pass

        self.focussed -= 1

        # if no focus or last, go to the end
        if self.focussed < 0:
            self.focussed = len(self.results) - 1

        self.results[self.focussed].select(True)

class MnemAppWindow(Gtk.Window):

    def __init__(self, client):
        super(MnemAppWindow, self).__init__(name="Mnem")

        self.client = client
        self.connect("destroy", self.stop)

        style_provider = Gtk.CssProvider()

        css = """
#result.selected{
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

        self.get_window().set_decorations(Gdk.WMDecoration.BORDER)

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

        self.main_input = Gtk.Entry()
        self.entry_change_sigid = self.main_input.connect(
            'changed', self.search_changed)

        self.main_box.pack_start(
            self.main_input, expand=False, fill=False, padding=0)

        self.completions = ResultListBox(self)
        self.main_box.add(self.completions)

        self.add(self.main_box)

        self.connect('key-press-event', self.key_press)

    def key_press(self, widget, event):

        shift = event.state & Gdk.ModifierType.SHIFT_MASK

        if event.keyval == Gdk.KEY_Tab or event.keyval == Gdk.KEY_ISO_Left_Tab:

            if event.keyval == Gdk.KEY_ISO_Left_Tab:
                self.handle_cycle(False)
            else:
                self.handle_cycle(not shift)

        elif event.keyval == Gdk.KEY_Down or event.keyval == Gdk.KEY_Up:
            self.handle_cycle(event.keyval == Gdk.KEY_Down)

        elif event.keyval == Gdk.KEY_Return:
            self.handle_enter()

        elif event.keyval == Gdk.KEY_Escape:
            self.iconify()

    def handle_cycle(self, forward):
        if forward:
            self.completions.select_next()
        else:
            self.completions.select_prev()

    def handle_enter(self):
        self.completions.confirm_entry()

    def keyword_selected(self, keyword):

        text = self.main_input.get_text()

        key, query = self.get_key_query(text)

        self.main_input.disconnect(self.entry_change_sigid)
        self.set_key_query(key, keyword)
        self.entry_change_sigid = self.main_input.connect(
            'changed', self.search_changed)

    def set_key_query(self, key, query):
        self.main_input.set_text("%s %s" % (key, query))
        #self.main_input.set_position(-1)  # end
        self.main_input.select_region(-1, -1)

    def get_key_query(self, text):

        parts = text.split(" ", 1)

        if not parts:
            return

        if len(parts) == 1:
            key = "Default"  # TODO
            query = parts[0]
        else:
            key = parts[0]
            query = parts[1]

        return key, query

    def search_changed(self, entry):

        search = entry.get_text()

        key, query = self.get_key_query(search)

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
            key = self.client.cfg.get('complete', 'default', fallback='google')

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
