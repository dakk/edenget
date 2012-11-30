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

import urllib as ul
import urllib2 as ul2
import json as js
import os
import httplib as hl
import cookielib
from Mirror import Mirror


class MangaEden (Mirror):		
	LANGUAGES = [["0", "English", "en"], ["1", "Italiano", "it"]] 
	IMG_BASE_PATH = "http://cdn.mangaeden.com/mangasimg/"
	
	def __init__(self, user, password):
		Mirror.__init__(self, user, password)
	
	""" Return the name of the mirror """
	def getName(self):
		return "MangaEden"
	
		
	""" Give a list of tuple ["code", "Language"] """
	def getLanguageList(self):
		return self.LANGUAGES
			
	
	""" 
		Return the list of available mangas for a given language code.
		Each element is a tuple ["code", "Title", "imageUrl", "alias"] 
	"""
	def getMangaList(self, languageCode):
		data = ul.urlopen("http://www.mangaeden.com/api/list/"+str(languageCode)+"/").read()
			
		l = []
		jd = js.loads(data)['manga']
		
		for manga in jd:
			l.append([manga['i'],manga['t'], self.IMG_BASE_PATH+str(manga['im']) if manga['im'] != None else None, manga['a']])
		
		return l
		
		

	""" Return the list of chapters ["id", "chapterNumber", "title"] """
	def getMangaChaptersList(self, mangaCode):
		data = ul.urlopen("http://www.mangaeden.com/api/manga/"+str(mangaCode)+"/").read()
			
		l = []
		jd = js.loads(data)['chapters']
		
		for chap in jd:
			l.append([chap[3],chap[0],chap[2]])
		
		return l
		
	
	""" Return manga infos as [language, alias, image, description]"""	
	def getMangaInfo(self, mangaCode):
		data = ul.urlopen("http://www.mangaeden.com/api/manga/"+str(mangaCode)+"/").read()
			
		l = []
		jd = js.loads(data)
		
		return [self.LANGUAGES[int(jd['language'])][2], jd['alias'], self.IMG_BASE_PATH+str(jd['image']) if jd['image'] != None else None, jd['description']]
		
		



	def getMangaChapterFileName(self, mangaCode, chapterNumber, destination, formatType="pdf"):
		la = self.getMangaInfo(mangaCode)
		return destination+os.sep+la[1]+"_"+str(chapterNumber)+".pdf"

		
	""" Download a single chapter and save it in the given destination """
	def getMangaChapter(self, mangaCode, chapterNumber, destination, formatType="pdf"):
		self.user = "edenget"
		self.password = "pwedenget"
		
		la = self.getMangaInfo(mangaCode)
		
		url = "http://www.mangaeden.com/"+la[0]+"-"+formatType+"/"+la[1]+"/"+str(chapterNumber)+"/"
		fileUri = destination+os.sep+la[1]+"_"+str(chapterNumber)+".pdf"

		# Login and get coockie
		login_data = ul.urlencode({ 'username' : self.user, 'password' : self.password })

		cj = cookielib.CookieJar()
		opener = ul2.build_opener(ul2.HTTPCookieProcessor(cj))
		data = opener.open("http://www.mangaeden.com/login/", login_data).read()	

		if data.find("Invalid username and password combination") != -1:
			return None
			
		# Get the chapter
		opener = ul2.build_opener(ul2.HTTPCookieProcessor(cj))
		req = opener.open(url)

		f = open(fileUri, "w")
		
		while data != "":
			data = req.read(1024)
			f.write(data)
		
		f.close()
		
		return fileUri
