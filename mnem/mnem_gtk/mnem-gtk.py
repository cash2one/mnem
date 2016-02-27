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

class MnemAppWindow(Gtk.Window):
    
    def __init__(self, client):
        super(MnemAppWindow, self).__init__()
        
        self.client = client
        self.connect("destroy", self.stop)

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
        self.main_box.add(main_input)
        
        self.add(self.main_box)

        
    def search_changed(self, entry):
        
        search = entry.get_text()
        
        parts = search.split(" ", 1)
        
        if not parts:
            return

        if len(parts) == 1:
            key = "Default" # TODO
            query = parts[0] 
        else:
            key = parts[0]
            query = parts[1]
                
        self.perform_search(key, query)
        
    def perform_search(self, key, query):
        
        # TODO
        key = "google"
        
        try:
            comps = self.client.getCompletions(key, None, query)
        except:
            raise
        
        if len(comps) == 0:
            return
        
        print(comps)
             

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