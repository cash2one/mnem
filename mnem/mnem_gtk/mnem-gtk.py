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

import threading

class MnemEntryBoxModel(object):
    '''
    Class to represent the model for the entry box area of the UI
    '''

    def __init__(self, listener):
        self.entered = ''
        self.searchkey = ''
        self.listener = listener

    def setEntered(self, entered):
        self.entered = entered
        self.listener.changed()

class MnemEntryBox(object):
    '''
    UI for the entry box area
    '''

    def __init__(self, mainapp):
        self.mainapp = mainapp

        self.model = MnemEntryBoxModel(self)

        self.box = Gtk.VBox()

        self.main_input = Gtk.Entry()
        self.entry_change_sigid = self.main_input.connect(
            'changed', self.search_changed)

        self.box.pack_start(
            self.main_input, expand=False, fill=False, padding=0)

    def changed(self):
        '''
        Callback from the model on change
        '''
        print('changed')

    def get_entry_text(self):
        return self.main_input.get_text()

    def set_key_query(self, key, query):

        self.main_input.disconnect(self.entry_change_sigid)
        self.main_input.set_text("%s %s" % (key, query))
        self.entry_change_sigid = self.main_input.connect(
            'changed', self.search_changed)

        # self.main_input.set_position(-1)  # end
        self.main_input.select_region(-1, -1)

    def search_changed(self, entry):

        search = entry.get_text()

        self.mainapp.do_search(search)

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
            self.url = None

        self.keyword = result["keyword"]

        keyword = Gtk.Label(result["keyword"])
        keyword.set_justify(Gtk.Justification.LEFT)

        self.pack_start(keyword, expand=False, fill=True, padding=0)

        if self.url:
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

        self.set_default_size(300, 0)

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

        self.entry_box = MnemEntryBox(self)
        self.main_box.add(self.entry_box.box)

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

        text = self.entry_box.get_entry_text()

        key, query = self._get_key_query(text)

        self.entry_box.set_key_query(key, keyword)

    def _get_key_query(self, text):

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

    def do_search(self, search):

        key, query = self._get_key_query(search)

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

        srch_thd = SearchRequestThread(self.client, key, 'complete', query, self.handle_results)
        srch_thd.start()

    def handle_results(self, comps):

        print(comps)

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

class SearchRequestThread(threading.Thread):
    '''
    Thread to go off and execute a request, which might take some time
    '''

    def __init__(self, client, key, reqtype, query, handler, *args, **kwargs):
        self.client = client
        self.key = key
        self.reqtype = reqtype
        self.query = query
        self.handler = handler

        super(SearchRequestThread, self).__init__(*args, **kwargs)

    def run(self):

        res = self.client.getCompletions(self.key, self.reqtype, self.query)

        self.handler(res)


if __name__ == "__main__":

    print("Mnem GTK")

    mnemGtk = MnemGtk()
