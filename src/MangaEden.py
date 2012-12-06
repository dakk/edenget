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
import time
import httplib as hl
import cookielib
from Mirror import Mirror


class MangaEden (Mirror):		
	LANGUAGES = [["0", "English", "en"], ["1", "Italiano", "it"]] 
	IMG_BASE_PATH = "http://cdn.mangaeden.com/mangasimg/"
	
	def __init__(self, user = None, password = None):
		Mirror.__init__(self, user, password)
		self.formatTypes = {0:"pdf", 1:"image"}
	
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
		
		return [self.LANGUAGES[int(jd['language'])][2], jd['alias'], self.IMG_BASE_PATH+str(jd['image']) if jd['image'] != None else None, jd['description'], jd['chapters']]
		
		


	""" Get the file path of a chapter """
	def getMangaChapterFileName(self, mangaCode, chapterNumber, destination, formatType="pdf"):
		try:
			la = self.getMangaInfo(mangaCode)
		except:
			raise Exception('networkError')

				
		if formatType == "pdf":
			return destination+os.sep+la[1]+os.sep+la[1]+"_"+str(chapterNumber)+".pdf"
		elif formatType == "image":
			return destination+os.sep+la[1]+os.sep+str(chapterNumber)+os.sep
		
		return None
		
		
	""" Download a single chapter and save it in the given destination """
	def getMangaChapter(self, mangaCode, chapterNumber, destination, formatType="pdf", stopEvent = None, progressNotify = None):
		self.downloadLock.acquire()
		
		#self.user = ""
		#self.password = ""
		
		la = self.getMangaInfo(mangaCode)
		fileUri = self.getMangaChapterFileName(mangaCode, chapterNumber, destination, formatType)

		if formatType == "pdf":
			try:
				os.makedirs(destination+os.sep+la[1])
			except:
				pass
			
			url = "http://www.mangaeden.com/"+la[0]+"-"+formatType+"/"+la[1]+"/"+str(chapterNumber)+"/"

			# Login and get coockie
			login_data = ul.urlencode({ 'username' : self.user, 'password' : self.password })
			

			cj = cookielib.CookieJar()
			opener = ul2.build_opener(ul2.HTTPCookieProcessor(cj))
			data = opener.open("http://www.mangaeden.com/login/", login_data).read()	
			
			if data.find("Invalid username and password combination") != -1:
				self.downloadLock.release()
				raise Exception('loginError')
				
				
			# Get the chapter
			tr = 0
			while tr < 3 and (not stopEvent.is_set()):
				try:
					opener = ul2.build_opener(ul2.HTTPCookieProcessor(cj))
					req = opener.open(url)
					
					size = req.headers.items()[0][1]
					downloaded = 0


					f = open(fileUri, "w")
					
					while data != "" and (not stopEvent.is_set()):
						data = req.read(1024)
						f.write(data)
						downloaded += 1024
						
						if progressNotify:
							progressNotify(int(100*downloaded/size))
					
					f.close()
					tr = 5
				except:
					tr += 1
					time.sleep(1)
			if tr > 4:
				self.downloadLock.release()
				raise Exception('networkError')
			
		elif formatType == "image":
			try:
				os.makedirs(fileUri)
			except:
				pass
			
			# Get the chapter code
			data = ul.urlopen("http://www.mangaeden.com/api/manga/"+str(mangaCode)+"/").read()
				
			jd = js.loads(data)['chapters']
			chapterCode = None
						
			for chap in jd:
				if str(chap[0]) == str(chapterNumber):
					chapterCode = chap[3]
					break
			
			
			if chapterCode == None:
				self.downloadLock.release()
				raise Exception('invalidChapterError')
			
			
			# Get the list of pages
			data = ul.urlopen("http://www.mangaeden.com/api/chapter/"+str(chapterCode)+"/").read()
				
			l = []
			jd = js.loads(data)['images']
			urlList = []
			
			
			for page in jd:
				urlList.append([page[0], page[1]])
				
			
			
			# Download each page
			size = len(urlList)
			downloaded = 0
			
			for page in urlList:
				tr = 0
				while tr < 3:
					try:
						if stopEvent.is_set():
							raise None
							
						req = ul2.urlopen(self.IMG_BASE_PATH+page[1])
						
						form = page[1].split(".")[-1]
						f = open(fileUri+str(page[0])+"."+form, "w")
						
						data = req.read()
						f.write(data)				
						f.close()
						
						downloaded += 1
						
						if progressNotify:
							progressNotify(int(100*downloaded/size))
						
						tr = 5
					except:
						tr += 1
						time.sleep(1)
						
			
		self.downloadLock.release()
		return fileUri
