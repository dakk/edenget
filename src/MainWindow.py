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

import MirrorList

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
	folderUri = None
	chapterInfo = None
	mangaInfo = None
	
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.destroy)
		self.window.set_title("EdenGet")
		self.window.set_default_size(400, 500)
		
		mainBox = gtk.VBox()
		self.window.add(mainBox)


		# Button toolbar
		toolbar = gtk.Toolbar()

		iconw = gtk.Image()
		iconw.set_from_stock(gtk.STOCK_FLOPPY, 16)
		add_button = toolbar.append_item("Download", "", "Private", iconw, self.onDownload)
		
		iconw = gtk.Image()
		iconw.set_from_stock(gtk.STOCK_FLOPPY, 16)
		add_button = toolbar.append_item("Download All", "", "Private", iconw, self.onDownloadAll)
		
		iconw = gtk.Image()
		iconw.set_from_stock(gtk.STOCK_DIRECTORY, 16)
		add_button = toolbar.append_item("Destination Folder", "", "Private", iconw, self.onChooseDestination)
  
   		#iconw = gtk.Image()
		#iconw.set_from_stock(gtk.STOCK_ABOUT, 16)
		#about_button = toolbar.append_item("About", "About this app", "Private", iconw, self.aboutEvent)
		
		#iconw = gtk.Image()
		#iconw.set_from_stock(gtk.STOCK_QUIT, 16)
		#close_button = toolbar.append_item("Quit", "Closes this app", "Private", iconw, self.destroy)

		mainBox.pack_start(toolbar, False, False, 0)
		
		
		# Box
		hbox = gtk.HBox()
		mainBox.add(hbox)
		
		
		# VBox for mangalist
		vbox = gtk.VBox()
		hbox.add(vbox)
		
		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw, True, True, 0)
		
		self.mangaList = gtk.ListStore(str, str)
		self.mangaListView = gtk.TreeView(self.mangaList)
		self.mangaListView.connect('cursor-changed', self.onSelectedManga)

		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Nome", rendererText, text=1)
		column.set_sort_column_id(1)
		self.mangaListView.append_column(column)
  
		sw.add(self.mangaListView)
		
		for x in MirrorList.get()[0].getMangaList(1):	
			self.mangaList.append([x[0], x[1]])	
		
		
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


		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("", rendererText, text=0)
		column.set_sort_column_id(0)
		self.chapterListView.append_column(column)
		
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Titolo", rendererText, text=1)
		column.set_sort_column_id(1)
		self.chapterListView.append_column(column)
  
		sw.add(self.chapterListView)
			
		self.window.show_all()


	def onDownload(self, window):
		if self.chapterInfo == None:
			pass
			
		if self.folderUri == None:
			self.onChooseDestination(window)
			
			
	def onDownloadAll(self, window):
		if self.mangaInfo == None:
			pass
			
		if self.folderUri == None:
			self.onChooseDestination(window)		
		
			
	def onChooseDestination(self, window):
		d = gtk.FileChooserDialog(	title = "Select a directory to save downloaded data", 
									action = gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
									buttons = (("Select", 1)))
		if d.run() == 1:
			try:
				self.folderUri = d.get_uri().replace("file://", "")
				d.destroy()
			except:
				d.destroy()
				self.onChooseDestination(window)
			
	def onSelectedChapter(self, widget, data = None):
		selection = self.chapterListView.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		tree_model, tree_iter = selection.get_selected()
		self.chapterInfo = [tree_model.get_value(tree_iter, 1), tree_model.get_value(tree_iter, 0)]
		
		
	def onSelectedManga(self, widget, data = None):
		selection = self.mangaListView.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		tree_model, tree_iter = selection.get_selected()
		manga = [tree_model.get_value(tree_iter, 1), tree_model.get_value(tree_iter, 0)]
		self.chapterInfo = None
		
		self.chapterList.clear()
		
		for x in MirrorList.get()[0].getMangaChaptersList(manga[1]):	
			self.chapterList.append([int(x[1]), x[2], x[0]])	
			
		self.mangaInfo = MirrorList.get()[0].getMangaInfo(manga[1])
			
		if self.mangaInfo[2] != None:
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
			
		else:
			self.mangaImage.clear()
			
		
	def destroy(self, widget, data = None):			
		gtk.main_quit()
		
		
	def run(self):
		gtk.main()
		
