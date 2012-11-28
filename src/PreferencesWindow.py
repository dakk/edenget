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

class PreferencesWindow (SecondaryWindow):
	#first = True
	
	def __init__(self, mainWindow):
		self.mainWindow = mainWindow
		
		SecondaryWindow.__init__(self, "Edenget - Preferences")
		self.window.set_default_size(500, 150)

		mainBox2 = gtk.VBox()
		mainBox = gtk.VBox()
		self.window.add(mainBox2)
		mainBox2.pack_start(mainBox, False, False, 2)
		
		
		# Login frame
		frame = gtk.Frame("Login")
		mainBox.pack_start(frame, False, False, 5)
		
		boxm = gtk.VBox()
		frame.add(boxm)
		
		self.username = gtk.Entry()
		self.password = gtk.Entry()

		# Username
		box = gtk.HBox()
		boxm.pack_start(box, True, True, 3)
		
		box.pack_start(gtk.Label("Username: "), False, False, 2)
		box.pack_start(self.username, False, False, 2)

		# Password
		box = gtk.HBox()
		boxm.pack_start(box, True, True, 3)
		
		box.pack_start(gtk.Label("Password: "), False, False, 2)
		box.pack_start(self.password, False, False, 2)


		
				
		# Destination frame
		frame = gtk.Frame("Filesystem")
		mainBox.pack_start(frame, False, False, 5)
		
		box = gtk.HBox()
		frame.add(box)
		
		self.destination = gtk.Entry()
		if self.mainWindow.folderUri != None:
			self.destination.set_text(self.mainWindow.folderUri)
		box.add(self.destination)
		
		bu = gtk.Button("Select")
		bu.connect('clicked', self.onChooseDestination, None)
		box.add(bu)
		
		# Button
		bu = gtk.Button("Close")
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
			self.username.set_text(data[0])
			self.password.set_text(data[1])
			self.mainWindow.folderUri = data[2]
			self.destination.set_text(self.mainWindow.folderUri)
			self.mainWindow.onChangeLoginData(self.username.get_text(), self.password.get_text())

		
	def savePrefs(self):
		f = open("eden.cfg", "w")
		
		f.write(self.username.get_text()+"\n")
		f.write(self.password.get_text()+"\n")
		if self.mainWindow.folderUri != None:
			f.write(self.mainWindow.folderUri+"\n")
		else:
			f.write(".\n")
		f.close()
		
		
	def onChooseDestination(self, window, data=None):
		self.mainWindow.onChooseDestination(window)
		self.destination.set_text(self.mainWindow.folderUri)


	def onClose(self, w, data):
		PreferencesWindow.changeVisibility(self)

	def changeVisibility(self):
		#if self.first:
		#	self.loadPrefs()
		#	self.first = False
		#else:
		self.savePrefs()
			
		self.mainWindow.onChangeLoginData(self.username.get_text(), self.password.get_text())
		
		SecondaryWindow.changeVisibility(self)
		
		if self.mainWindow.folderUri != None:
			self.destination.set_text(self.mainWindow.folderUri)
