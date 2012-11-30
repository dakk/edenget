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
import gtk.gdk as gdk
import urllib2 as ul
import threading as th
import locale
import os
import sys
import gettext
from Locale import Locale
from SecondaryWindow import *


class QueueWindow (SecondaryWindow):
	activeTask = None
	tasks = []
	tasksLock = th.Lock()
	activeTaskLock = th.Lock()
	n = 0
	
	def __init__(self):
		_ = Locale()._
		
		SecondaryWindow.__init__(self, _("Edenget - Download Queue"))
		self.window.set_default_size(400, 500)
		self.window.set_modal(False)
		
		mainBox = gtk.VBox()
		self.window.add(mainBox)
		
		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		mainBox.pack_start(sw, True, True, 0)
		
		self.tasksList = gtk.ListStore(int, str, str)
		self.tasksListView = gtk.TreeView(self.tasksList)
		self.tasksListView.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
		
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("", rendererText, text=0)
		column.set_sort_column_id(0)
		self.tasksListView.append_column(column)
		
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn(_("File"), rendererText, text=1)
		column.set_sort_column_id(1)
		self.tasksListView.append_column(column)
		
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn(_("State"), rendererText, text=2)
		column.set_sort_column_id(2)
		self.tasksListView.append_column(column)
  
		sw.add(self.tasksListView)
	
	
	def getNextTask(self):
		self.tasksLock.acquire()
		for x in self.tasks:
			if x != None:
				return x
		
		return None
		self.tasksLock.release()
		
	class DownloadThread(th.Thread):
		qw = None 
		fileName = ""
		
		def __init__(self, i, mangaEden, mangaCode, chapterNumber, destination, formatType, queueWindow):
			th.Thread.__init__(self)
			self.i = i
			self.qw = queueWindow
			self.mangaEden = mangaEden
			self.mangaCode = mangaCode
			self.chapterNumber = chapterNumber
			self.destination = destination
			self.formatType = formatType
			self.fileName = mangaEden.getMangaChapterFileName(mangaCode, chapterNumber, destination)
			
		def run(self):
			fname = self.mangaEden.getMangaChapter(self.mangaCode, self.chapterNumber, self.destination, self.formatType)
				
			self.qw.tasksLock.acquire()
			self.qw.tasks[self.i] = None
			self.qw.tasksLock.release()
			
			self.qw.activeTaskLock.acquire()
			self.qw.activeTask = self.qw.getNextTask()
			
			if self.qw.activeTask != None:
				self.qw.activeTask.start()
			self.qw.activeTaskLock.release()
			
			self.qw.updateList()

			print "Download of", fname, "completed"
			#gdk.threads_enter()		
			#_ = Locale()._
			#md = gtk.MessageDialog(self.window, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, fname)
			#md.set_title(_("Download Complete"))
			#md.run()
			#md.destroy()
			#gdk.threads_leave()		
		
	
	def updateList(self):
		_ = Locale()._
		self.tasksList.clear()
		
		self.activeTaskLock.acquire()
		self.tasksLock.acquire()
		
		print self.tasks
		
		for x in self.tasks:
			if x != None:
				self.tasksList.append([int(x.i), str(x.fileName), _("Active") if (self.activeTask == x) else _("Queued")])	
			
			
		self.tasksLock.release()
		self.activeTaskLock.release()
			
		
	def add(self, mangaEden, mangaCode, chapterNumber, destination, formatType="pdf"):
		_ = Locale()._
		t = self.DownloadThread(self.n, mangaEden, mangaCode, chapterNumber, destination, formatType, self)
		
		self.tasksLock.acquire()
		self.tasks.append(t)
		self.tasksLock.release()
				
		self.n+=1
		
		
		self.activeTaskLock.acquire()
		
		self.tasksList.append([int(t.i), str(t.fileName), _("Active") if (self.activeTask == None) else _("Queued")])	
		if self.activeTask == None:
			self.activeTask = t
			t.start()
		self.activeTaskLock.release()
