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
	tasksListLock = th.Lock()
	selectedTasks = []
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
		
		self.tasksList = gtk.ListStore(int, str, int)
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
		
		column = gtk.TreeViewColumn(_("Progress"), gtk.CellRendererProgress(), value=2)
		column.set_sort_column_id(2)
		self.tasksListView.append_column(column)
  
  
		selection = self.tasksListView.get_selection()
		selection.set_mode(gtk.SELECTION_MULTIPLE)
		selection.connect("changed", self.onSelectedTasks)
		
		sw.add(self.tasksListView)
		
		
		# Toolbar
		toolbar = gtk.Toolbar()
		toolbar.set_style(gtk.TOOLBAR_BOTH_HORIZ)

		iconw = gtk.Image()
		iconw.set_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_LARGE_TOOLBAR)
		toolbar.append_item(_("Delete"), "", "Private", iconw, self.onDeleteTask)	

		iconw = gtk.Image()
		iconw.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_LARGE_TOOLBAR)
		toolbar.append_item(_("Close"), "", "Private", iconw, lambda w: self.changeVisibility())	
		  
		mainBox.pack_start(toolbar, False, False, 0)

	
	
	def onSelectedTasks(self, w):
		selection = self.tasksListView.get_selection()
		selection.set_mode(gtk.SELECTION_MULTIPLE)
		
		self.selectedChapters = []
		
		def foreach(model, path, iter, selected):
			selected.append([model.get_value(iter, 0),model.get_value(iter, 1)])
			
		selection.selected_foreach(foreach, self.selectedTasks)
		
		
	def onDeleteTask(self, w):
		for task in self.selectedTasks:
			i = task[0]
			self.tasksLock.acquire()
			if self.tasks[i] == None:
				self.tasksLock.release()
				return		
			
			self.activeTaskLock.acquire()
			if self.tasks[i][1] == self.activeTask:
				self.tasks[i][1].stop()
				self.tasks[i][1].progressFunc("Stopped")
				self.tasks[i] = None
				self.runNext()
			else:
				self.tasks[i] = None
			self.activeTaskLock.release()
			
			self.tasksLock.release()
	
	def getNextTask(self):
		self.tasksLock.acquire()
		for x in self.tasks:
			if x != None:
				self.tasksLock.release()
				return x
		
		self.tasksLock.release()
		return None
		
		
	class DownloadThread(th.Thread):
		qw = None 
		fileName = ""
		progressFunc = None
		stopEvent = None
		
		def __init__(self, i, mangaEden, mangaCode, chapterNumber, destination, formatType, queueWindow):
			th.Thread.__init__(self)
			self.stopEvent = th.Event()
			
			self.i = i
			self.qw = queueWindow
			self.mangaEden = mangaEden
			self.mangaCode = mangaCode
			self.chapterNumber = chapterNumber
			self.destination = destination
			self.formatType = formatType
			self.fileName = mangaEden.getMangaChapterFileName(mangaCode, chapterNumber, destination, formatType)
			
		def run(self):
			fname = None
			try:
				fname = self.mangaEden.getMangaChapter(self.mangaCode, self.chapterNumber, self.destination, self.formatType, self.stopEvent, self.progressFunc)
			except Exception as e:
				er = e.args[0]

				self.progressFunc("Failed")
				#print er

			self.qw.tasksLock.acquire()
			self.qw.tasks[self.i] = None
			self.qw.tasksLock.release()
			
			self.qw.runNext()

			print "Download of", fname, "completed"	
		
		def stop(self):
			self.stopEvent.set()
			super(DownloadThread, self).join(None)

	
	def runNext(self):
		self.activeTaskLock.acquire()
		self.activeTask = self.getNextTask()
			
		if self.activeTask != None:
			print "Starting next..."
			self.activeTask[0].start()
		self.activeTaskLock.release()		
		
	
	def setRowProgress(self, rowIter, progress):
		if type(progress) == str:
			self.tasksListLock.acquire()
			self.tasksList[rowIter][2] = progress
			self.tasksListLock.release()
		else:
			self.tasksListLock.acquire()
			self.tasksList[rowIter][2] = progress
			self.tasksListLock.release()
	
	def add(self, mangaEden, mangaCode, chapterNumber, destination, formatType="pdf"):
		_ = Locale()._
		t = self.DownloadThread(self.n, mangaEden, mangaCode, chapterNumber, destination, formatType, self)
					
		self.n+=1				
		
		self.tasksListLock.acquire()
		it = self.tasksList.append([int(t.i), str(t.fileName), 0])	
		self.tasksListLock.release()
		t.progressFunc = (lambda progress: self.setRowProgress(it,progress))
				
		self.tasksLock.acquire()
		self.tasks.append([t, it])
		self.tasksLock.release()
		
		self.activeTaskLock.acquire()
		if self.activeTask == None:
			self.activeTaskLock.release()
			self.runNext()
			return
		self.activeTaskLock.release()
		
