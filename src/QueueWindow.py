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

class QueueWindow:
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.changeVisibility)
		self.window.set_title("EdenGet - Download Queue")
		self.window.set_default_size(400, 500)
		
		mainBox = gtk.VBox()
		self.window.add(mainBox)
		
		
		self.window.hide_all()
				
			
	def changeVisibility(self):
		if not self.window.get_visible():
			self.window.show_all()
		else:
			self.window.hide_all()
