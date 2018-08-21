#!/usr/bin/env python

import shlex, sys

if (sys.version_info < (2, 7)):
    import subprocess
    def check_output(args):
        #print("check_output(args={0})".format(args))
        return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
elif (sys.version_info > (3, 0)):
    from subprocess import call, Popen, check_output, PIPE
elif (sys.version_info > (2, 6)):
    from subprocess import call, Popen, check_output, PIPE
else:pass

from threading import Thread
import gi, signal, time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

resources=[]

def safe_exit():
    counter=0
    for r in resources:
        try:
            counter+=1
            if None == r:
                continue
            r.close()
            resources.remove(r)
            del r
            print("deleted {}".format(counter))
        except Exception as inst:
            print (type(inst))
            print (inst.args)
            print (inst)
            print (__file__, 'Oops')
            continue
    try:
        Gtk.main_quit()
    except Exception as inst:
        print (type(inst))
        print (inst.args)
        print (inst)
        print (__file__, 'Oops')


def sig_handler(sig, frame):
    print ("got sig(%d)\n" % sig)
    safe_exit()

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

XCastProjectsCreatorResults = ''

def saveRpmScript(commands):
    XCastProjectsCreatorResults = commands
    #print("Saving {}".format(XCastProjectsCreatorResults))

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))

class XCastProjectsCreator(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="Select project path")
        self.set_border_width(10)
        self.execute = None

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_outer)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox, True, True, 0)
        rvbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(rvbox, True, True, 0)

        button = Gtk.Button.new_with_mnemonic("_Close")
        button.connect("clicked", self.on_close_clicked)
        rvbox.pack_start(button, True, True, 0)

        #self.pulse = Gtk.CheckButton("Check Results")
        #self.pulse.connect("toggled", self.on_pulse_toggled)
        #self.pulse.set_active(False)
        #vbox.pack_start(self.pulse, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.set_text("Select a project below")
        vbox.pack_start(self.entry, True, True, 0)

        self.label = Gtk.Label("Results will show up here")
        self.label.set_line_wrap(True)
        self.label.set_selectable(True)
        self.label.set_justify(Gtk.Justification.FILL)

        rvbox.pack_start(self.label, True, True, 0)


        listbox.add(row)

        listbox_2 = Gtk.ListBox()
        self.items = 'middle/stack_na/mserver ACD middle/stack_opt/mserver middle/stack_opt/redir confdep mediaframework/Hermes middle middle/stack_opt/console middle/stack_opt/bbua monitoring/cfg monitoring/AcdMon middle/stack_opt/teleblock middle/sparser middle/stack_opt/webphone mapp monitoring/CnfMon monitoring/EvService middle/stack_opt/platform-proxy mediaframework/Codecs tui scripts/cdrs db config/xbroker coast middle/middle_ng updater middle/stack_opt middle/stack_opt/non-platform-proxy middle/stack_opt/mserver/t38 scripts/utils middle/stack_opt/syncmwi voice_loader altdb monitoring/DashMan  middle/utils'.split()

        for item in self.items:
            listbox_2.add(ListBoxRowWithData(item))

        self.hide_when_done = vbox
        self.resize_me = box_outer

        def sort_func(row_1, row_2, data, notify_destroy):
            return row_1.data.lower() > row_2.data.lower()


        def filter_func(row, data, notify_destroy):
            return False if row.data == 'Fail' else True

        def on_row_activated(listbox_widget, row):
            try:
                if row.data in self.items:
                    #self.pulse.set_active(True)
                    self.entry.set_progress_pulse_step(0.2)
                    # Call self.do_pulse every 100 ms
                    self.timeout_id = GLib.timeout_add(100, self.do_pulse, None)

                    self.entry.set_text("Working now, please wait")
                    cmd="/home/nir/bin/get_project_commands.sh '{}'".format(row.data)
                    args=shlex.split(cmd)
                    self.execute = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    #print('\n'.join(check_output(args).split('\n')))
                    #print("Done!")
            except:
                print("OOOOPPPPS!")
            #self.pulse.set_active(False)

        listbox_2.set_sort_func(sort_func, None, False)
        listbox_2.set_filter_func(filter_func, None, False)

        listbox_2.connect('row-activated', on_row_activated)
        #listbox_2.set_justify(Gtk.Justification.LEFT)

        vbox.pack_start(listbox_2, True, True, 0)
        listbox_2.show_all()
        self.projects_list = listbox_2

    def on_close_clicked(self, button):
        print("Closing application")
        Gtk.main_quit()

    def on_pulse_toggled(self, button):
        if button.get_active():
            self.entry.set_progress_pulse_step(0.2)
            # Call self.do_pulse every 100 ms
            self.timeout_id = GLib.timeout_add(100, self.do_pulse, None)
        else:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
            self.entry.set_progress_pulse_step(0)

    def do_pulse(self, user_data):
        if None != self.execute and None != self.execute.poll():
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
            self.entry.set_progress_pulse_step(0)
            self.print_results(self.execute)
        else:
            self.entry.progress_pulse()
        return True

    def print_results(self,process):
        if None == process:
            return
        (out,err) = process.communicate()
        self.label.set_text(out)
        self.hide_when_done.destroy()
        self.resize_me.queue_resize()

#windows = [ ListBoxWindow(), LabelWindow()] #ButtonWindow(), StackWindow(), EntryWindow(), ToggleButtonWindow()]
def main():
    windows = [ XCastProjectsCreator(), ] #LabelWindow()] #ButtonWindow(), StackWindow(), EntryWindow(), ToggleButtonWindow()]

    for win in windows:
        win.connect("destroy", Gtk.main_quit)
        resources.append(win)
        win.show_all()

    Gtk.main()
    print("Reading {}".format(XCastProjectsCreatorResults))
    safe_exit()

if __name__ == "__main__":
    main()
