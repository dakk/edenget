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

class SecondaryWindow:
	def __init__(self, title):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.onDestroy)
		self.window.connect("destroy", lambda w: None)
		self.window.set_title(title)
				
		self.window.hide_all()
	
	def onDestroy(self, w, data = None):
		self.changeVisibility()
					
	def changeVisibility(self):
		if not self.window.get_visible():
			self.window.show_all()
		else:
			self.window.hide_all()
