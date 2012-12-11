# EdenGet
# Copyright (C) 2012,  Davide Gessa
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import pygtk
pygtk.require('2.0')
import gtk
import urllib2 as ul
import threading as th
import locale
import os
import sys
import gettext
from SecondaryWindow import *
from Locale import Locale


class PreferencesWindow (SecondaryWindow):
	folderUri = None
	
	def __init__(self, mainWindow):
		_ = Locale._
		self.mainWindow = mainWindow
		
		SecondaryWindow.__init__(self, _("Edenget - Preferences"))
		self.window.set_default_size(500, 150)
		self.window.set_modal(True)

		mainBox2 = gtk.VBox()
		mainBox = gtk.VBox()
		self.window.add(mainBox2)
		mainBox2.pack_start(mainBox, False, False, 2)
		
		
		# Login frame
		frame = gtk.Frame(_("Login"))
		mainBox.pack_start(frame, False, False, 5)
		
		boxm = gtk.VBox()
		frame.add(boxm)
		
		self.usernameEntry = gtk.Entry()
		self.passwordEntry = gtk.Entry()
		self.passwordEntry.set_visibility(False)

		# Username
		box = gtk.HBox()
		boxm.pack_start(box, True, True, 3)
		
		box.pack_start(gtk.Label(_("Username: ")), False, False, 2)
		box.pack_start(self.usernameEntry, False, False, 2)

		# Password
		box = gtk.HBox()
		boxm.pack_start(box, True, True, 3)
		
		box.pack_start(gtk.Label(_("Password: ")), False, False, 2)
		box.pack_start(self.passwordEntry, False, False, 2)


		
				
		# Destination frame
		frame = gtk.Frame(_("Filesystem"))
		mainBox.pack_start(frame, False, False, 5)
		
		box = gtk.HBox()
		frame.add(box)
		
		self.destination = gtk.Entry()
		if self.folderUri != None:
			self.destination.set_text(self.folderUri)
		box.add(self.destination)
		
		bu = gtk.Button(_("Select"))
		bu.connect('clicked', self.onChooseDestination, None)
		box.add(bu)
		
		
		# Button
		bu = gtk.Button(_("Close"))
		bu.connect("clicked", self.onClose, None)
		mainBox.pack_start(bu, False, False, 5);


	def loadPrefs(self):
		try:
			f = open("eden.cfg", "r")
		except:
			return
		data = f.read().split("\n")
		f.close()
		
		if len(data) >= 3:
			self.usernameEntry.set_text(data[0])
			self.passwordEntry.set_text(data[1])
			self.folderUri = data[2]
			self.destination.set_text(self.folderUri)
			self.mainWindow.onChangeLoginData(self.usernameEntry.get_text(), self.passwordEntry.get_text())

		
	def savePrefs(self):
		f = open("eden.cfg", "w")
		
		f.write(self.usernameEntry.get_text()+"\n")
		f.write(self.passwordEntry.get_text()+"\n")
		if self.folderUri != None:
			f.write(self.folderUri+"\n")
		else:
			f.write(".\n")
		f.close()
		
		
	def onChooseDestination(self, window, data=None):
		_ = Locale._
		d = gtk.FileChooserDialog(	title = _("Select a directory to save downloaded data"), 
									action = gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
									buttons = ((_("Select"), 1)))
		if d.run() == 1:
			try:
				self.folderUri = d.get_uri().replace("file://", "")
				if sys.platform.find("win") != -1 and (self.folderUri[0] == "/"):
					self.folderUri = self.folderUri[1:]
				d.destroy()
			except:
				d.destroy()
				self.onChooseDestination(window)
				
		self.destination.set_text(self.folderUri)


	def onClose(self, w, data):
		PreferencesWindow.changeVisibility(self)

	def changeVisibility(self):
		self.savePrefs()
			
		self.mainWindow.onChangeLoginData(self.usernameEntry.get_text(), self.passwordEntry.get_text())
		
		SecondaryWindow.changeVisibility(self)
		
		if self.folderUri != None:
			self.destination.set_text(self.folderUri)
