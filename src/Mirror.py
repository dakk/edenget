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
import threading as th

""" Abstract class that represent a mirror where I can get mangas """
class Mirror:
	""" 
		The mirror can download only a file at time. The getMangaChapter 
		acquire and release the lock 
	"""
	downloadLock = th.Lock()
	
	""" Supported formatType """
	formatTypes = None
	
	def __init__(self, user=None, password=None):
		self.user = user
		self.password = password
		
	""" Return the name of the mirror """
	def getName(self):
		raise BaseException("Abstract method not implementated")
		
		
	""" Give a list of tuple ["code", "Language"] """
	def getLanguageList(self):
		raise BaseException("Abstract method not implementated")
			
			
	""" Return manga infos as [language, alias, image, description] """
	def getMangaInfo(self, mangaCode):
		raise BaseException("Abstract method not implementated")
	
	
	""" Get the file path of a chapter """
	def getMangaChapterFileName(self, mangaCode, chapterNumber, destination, formatType):
		raise BaseException("Abstract method not implementated")
	
		
	""" 
		Return the list of available mangas for a given language code.
		Each element is a tuple ["code", "Title", "imageUrl", "alias"] 
	"""
	def getMangaList(self, languageCode):
		raise BaseException("Abstract method not implementated")
		

	""" Return the list of chapters ["id", "chapterNumber", "title"] """
	def getMangaChaptersList(self, mangaCode):
		raise BaseException("Abstract method not implementated")
		
		
	""" Download a single chapter and save it in the given destination """
	def getMangaChapter(self, mangaCode, chapterNumber, destination, formatType):
		raise BaseException("Abstract method not implementated")
		
