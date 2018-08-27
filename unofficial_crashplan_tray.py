#!/usr/bin/python
####
#### Unofficial Code42 CrashPlan tray utility for Linux.
####
#### THIS PRODUCT IS NOT ENDORSED, SUPPORTED, OR RECOMMENDED BY CODE42.
####
#### Written by: Ben Alldridge (developer@onkraken.net) on 26-08-2018

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
import signal
import os
import subprocess

APPINDICATOR_ID = 'unofficial_crashplan_tray'


def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('icon.png'),
                                           appindicator.IndicatorCategory.APPLICATION_STATUS)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(cp_menu())
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    gtk.main()


def cp_menu():
    menu = gtk.Menu()

    item_open_crashplan = gtk.MenuItem('Open CrashPlan')
    item_quit_tray = gtk.MenuItem('Quit Tray')
    item_about = gtk.MenuItem('About')

    item_open_crashplan.connect('activate', cp_open)
    item_quit_tray.connect('activate', tray_close)
    item_about.connect('activate', about)

    menu.append(item_open_crashplan)
    menu.append(item_quit_tray)
    menu.append(item_about)
    menu.show_all()
    return menu


def cp_open(source):
    try:
        process = subprocess.check_output("ps aux | grep crashplan | grep -oP '[\/].+?(?=\/jre\/bin\/java)'",
                                          shell=True).strip()
        process_string = str(process.decode("utf-8"))
        cp_path = "{}{}".format(process_string, "/bin/CrashPlanDesktop")
        subprocess.Popen(cp_path)

    except subprocess.CalledProcessError as exception:
        md = gtk.MessageDialog(None, gtk.MessageType.INFO, buttons=gtk.ButtonsType.OK,
                               message_format="The CrashPlan engine is not running. Typically you can start it "
                                              "by running \"sudo service crashplan start\" from the terminal.")
        md.run()

        if gtk.ResponseType.OK:
            md.destroy()


def tray_close(source):
    gtk.main_quit()


def about(source):
    md = gtk.MessageDialog(None, gtk.MessageType.INFO, buttons=gtk.ButtonsType.CLOSE,
                           message_format="Unofficial CrashPlan Tray Utility \n"
                                          "\n"
                                          "Written by: Ben Alldridge (developer@onkraken.net)")
    md.run()

    if gtk.ResponseType.CLOSE:
        md.destroy()


if __name__ == "__main__":
    main()
