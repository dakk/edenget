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
import locale
import os
import sys
import gettext
import threading as th

import MirrorList
from MangaEden import MangaEden
import QueueWindow
import PreferencesWindow
from Locale import Locale

gtk.gdk.threads_init()



license = """
EdenGet
Copyright (C) 2012, Davide Gessa

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

		

class MainWindow:
	selectedChapters = None
	mangaInfo = None
	selectedManga = None
	mangas = None
	mangaEden = None
	queueWindow = None
	preferencesWindow = None
	lang = 1
	
	def __init__(self):	
		_ = Locale()._
		self.queueWindow = QueueWindow.QueueWindow()
		self.preferencesWindow = PreferencesWindow.PreferencesWindow(self)
		self.preferencesWindow.loadPrefs()
		
		# Gtk stuffs
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.destroy)
		self.window.set_title("EdenGet")
		self.window.set_default_size(400, 500)
		
		mainBox = gtk.VBox()
		self.window.add(mainBox)


		# Menu
		menubar = gtk.MenuBar()
		mainBox.pack_start(menubar, False, False, 0)
		
		# File menu
		menu_item = gtk.MenuItem(_("File"))
		menubar.append(menu_item)
		menu = gtk.Menu()
		menu_item.set_submenu(menu)
		
		it = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		it.connect('activate', self.destroy)
		menu.append(it)
		


		# Edit menu
		menu_item = gtk.MenuItem(_("Edit"))
		menubar.append(menu_item)		
		menu = gtk.Menu()
		menu_item.set_submenu(menu)
		
		it = gtk.MenuItem(_("Destination folder"))
		#it = gtk.ImageMenuItem(gtk.STOCK_HARDDISK)
		it.connect('activate', lambda w: self.preferencesWindow.onChooseDestination(w))
		menu.append(it)

		it = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
		it.connect('activate', lambda w: self.preferencesWindow.changeVisibility())
		menu.append(it)
		
				
		# Help menu
		menu_item = gtk.MenuItem(_("Help"))
		menubar.append(menu_item)
		menu = gtk.Menu()
		menu_item.set_submenu(menu)
		
		it = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
		it.connect('activate', self.onAbout)
		menu.append(it)
		
		

		# Button toolbar
		toolbar = gtk.Toolbar()
		
		iconw = gtk.Image()
		iconw.set_from_stock(gtk.STOCK_EXECUTE, 16)
		toolbar.append_item(_("Download Queue"), "", "Private", iconw, lambda w: self.queueWindow.changeVisibility())  

		iconw = gtk.Image()
		iconw.set_from_stock(gtk.STOCK_DIRECTORY, 16)
		toolbar.append_item(_("Destination Folder"), "", "Private", iconw, self.preferencesWindow.onChooseDestination)
		
		self.languageCombo = gtk.combo_box_new_text()
		self.languageCombo.insert_text(1, "Italiano")
		self.languageCombo.insert_text(0, "English")
		self.languageCombo.set_active(1)
		self.languageCombo.connect('changed', self.onLanguageComboChanged)
		toolbar.append_element(gtk.TOOLBAR_CHILD_WIDGET, self.languageCombo, None, None, None, None, None, None)
		
		mainBox.pack_start(toolbar, False, False, 0)

		
		# Box
		hbox = gtk.HBox()
		mainBox.add(hbox)
		
		
		# VBox for mangalist
		vbox = gtk.VBox()
		hbox.add(vbox)
		
		notebook = gtk.Notebook()
		notebook.set_tab_pos(gtk.POS_TOP)
		vbox.add(notebook)
		
		
		# Search tab
		searchbox = gtk.VBox()
		notebook.prepend_page(searchbox, gtk.Label(_("Search")))
		
		self.searchEntry = gtk.Entry()
		self.searchEntry.connect('changed', self.onSearchTextModified)
		searchbox.pack_start(self.searchEntry, False, False, 0)
		
		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		searchbox.pack_start(sw, True, True, 0)
		
		self.searchList = gtk.ListStore(str, str)
		self.searchListView = gtk.TreeView(self.searchList)
		self.searchListView.connect('cursor-changed', self.onSelectedManga, self.searchListView)

		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn(_("Name"), rendererText, text=1)
		column.set_sort_column_id(1)
		self.searchListView.append_column(column)
  
		sw.add(self.searchListView)

		
		# Bookmarks tab		
		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		#vbox.pack_start(sw, True, True, 0)
		notebook.prepend_page(sw, gtk.Label(_("Bookmarks")))
		
		self.marksList = gtk.ListStore(str, str)
		self.marksListView = gtk.TreeView(self.marksList)
		self.marksListView.connect('cursor-changed', self.onSelectedManga, self.marksListView)

		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn(_("Name"), rendererText, text=1)
		column.set_sort_column_id(1)
		self.marksListView.append_column(column)
  
		sw.add(self.marksListView)
		
				
		# List tab
		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		#vbox.pack_start(sw, True, True, 0)
		notebook.prepend_page(sw, gtk.Label(_("Full List")))
		
		self.mangaList = gtk.ListStore(str, str)
		self.mangaListView = gtk.TreeView(self.mangaList)
		self.mangaListView.connect('cursor-changed', self.onSelectedManga, self.mangaListView)

		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn(_("Name"), rendererText, text=1)
		column.set_sort_column_id(1)
		self.mangaListView.append_column(column)
  
		sw.add(self.mangaListView)
			
		
		
		# VBox for chapter list
		vbox = gtk.VBox()
		hbox.add(vbox)
		
		self.mangaImage = gtk.Image()
		vbox.pack_start(self.mangaImage, False, False, 0)
		
		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw, True, True, 0)
		
		self.chapterList = gtk.ListStore(int, str, str)
		self.chapterListView = gtk.TreeView(self.chapterList)
		self.chapterListView.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
		self.chapterListView.connect('cursor-changed', self.onSelectedChapter)

		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("", rendererText, text=0)
		column.set_sort_column_id(0)
		self.chapterListView.append_column(column)
		
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn(_("Title"), rendererText, text=1)
		column.set_sort_column_id(1)
		self.chapterListView.append_column(column)
  
		sw.add(self.chapterListView)
	
	
		toolbar = gtk.Toolbar()

		iconw = gtk.Image()
		iconw.set_from_stock(gtk.STOCK_FLOPPY, 16)
		toolbar.append_item(_("Download"), "", "Private", iconw, self.onDownload)
		
		iconw = gtk.Image()
		iconw.set_from_stock(gtk.STOCK_FLOPPY, 16)
		toolbar.append_item(_("Download All"), "", "Private", iconw, self.onDownloadAll)
		
  
		vbox.pack_start(toolbar, False, False, 0)
			
		self.window.show_all()
		
		
		self.mangaEden = MangaEden("", "")
		self.onLanguageComboChanged(self.window)
		


	def onAbout(self, window):
		_ = Locale()._
		d = gtk.AboutDialog()
		d.set_authors(["Davide Gessa (gessadavide@gmail.com)"])
		d.set_license(license)
		d.set_comments(_("A multiplatform batch downloader for mangaeden.com"))
		d.set_wrap_license(True)
		
		d.set_logo(window.render_icon(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DIALOG))
		d.set_name(APP_NAME)
		d.run()
		d.destroy()
		

	def onLanguageComboChanged(self, window):
		self.lang = self.languageCombo.get_active()
		
		self.searchList.clear()
		self.mangaList.clear()
		self.marksList.clear()
		self.chapterList.clear()
		self.onSearchTextModified(window)
		
		try:
			self.mangas = self.mangaEden.getMangaList(self.lang)
			for x in self.mangas:	
				self.mangaList.append([x[0], x[1]])	
		except:
			self.mangas = []
			self.mangaList.clear()
			self.networkError()

	def onSearchTextModified(self, window):
		if self.mangas == None:
			return
			
		query = self.searchEntry.get_text()
		
		self.searchList.clear()
		for x in self.mangas:
			if x[1].lower().find(query.lower()) != -1:
				self.searchList.append([x[0], x[1]])	


	def onDownload(self, window):
		if self.selectedChapters == None:
			pass
			
		if self.preferencesWindow.folderUri == None:
			self.preferencesWindow.onChooseDestination(window)
			
		for x in self.selectedChapters:
			self.mangaEden.getMangaChapter(self.selectedManga[1], x, self.preferencesWindow.folderUri)
			
			
	def onDownloadAll(self, window):
		if self.mangaInfo == None:
			pass
			
		if self.preferencesWindow.folderUri == None:
			self.preferencesWindow.onChooseDestination(window)		
		
			
			
	def onSelectedChapter(self, widget, data = None):
		selection = self.chapterListView.get_selection()
		selection.set_mode(gtk.SELECTION_MULTIPLE)
		
		self.selectedChapters = []
		
		def foreach(model, path, iter, selected):
			selected.append(model.get_value(iter, 0))
			
		selection.selected_foreach(foreach, self.selectedChapters)
    
		#[tree_model.get_value(tree_iter, 1), tree_model.get_value(tree_iter, 0)]
		
		
	def onSelectedManga(self, widget, data = None):
		if data == None:
			return
		
		selection = data.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		tree_model, tree_iter = selection.get_selected()
		self.selectedManga = [tree_model.get_value(tree_iter, 1), tree_model.get_value(tree_iter, 0)]
		self.selectedChapters = None
		
		self.chapterList.clear()
		
		try:
			for x in self.mangaEden.getMangaChaptersList(self.selectedManga[1]):	
				self.chapterList.append([int(x[1]), x[2], x[0]])	
		
			self.mangaInfo = self.mangaEden.getMangaInfo(self.selectedManga[1])
		except:
			self.mangaInfo = ""
			self.networkError()
			return
				
		if self.mangaInfo[2] != None:
			try:
				response = ul.urlopen(self.mangaInfo[2])
				loader = gtk.gdk.PixbufLoader()
				loader.write(response.read())
				loader.close()        			
			
				pixbuf = loader.get_pixbuf()
						
				if pixbuf.get_height() < pixbuf.get_width():
					pixbuf = pixbuf.scale_simple(200,200*pixbuf.get_height()/pixbuf.get_width(),gtk.gdk.INTERP_BILINEAR)  
				else:
					pixbuf = pixbuf.scale_simple(200*pixbuf.get_width()/pixbuf.get_height(),200,gtk.gdk.INTERP_BILINEAR)  
					
				self.mangaImage.set_from_pixbuf(pixbuf)
			
			except:
				self.mangaImage.clear()
				return
		else:
			self.mangaImage.clear()
			
	
	def networkError(self):
		_ = Locale()._
		md = gtk.MessageDialog(self.window, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, _("Cannot connect to the server."))
		md.set_title(_("Network Error"))
		md.run()
		md.destroy()
		
		
	def destroy(self, widget, data = None):			
		gtk.main_quit()
		
	
	def onChangeLoginData(self, username, password):
		self.mangaEden = MangaEden(username, password)
		
	def run(self):
		gtk.main()
		
