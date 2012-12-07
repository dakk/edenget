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

class Bookmarks:
	marks = []
	
	def __init__(self):
		try:
			f = open("bookmarks.me", "r")
		except:
			f = None
		
		if f:
			b = f.read().split("\n")
			for x in b:
				if x!="":
					self.marks.append(x.split(","))
			f.close()
			
	def get(self):
		return self.marks
	
	def add(self, sel):
		try:
			self.marks.index(sel)
		except:
			self.marks.append(sel)
			self.save()
			
	
	def delete(self, sel):
		self.marks.remove(sel)
		self.save()
			
	def save(self):
		f = open("bookmarks.me", "w")
		for x in self.marks:
			f.write(x[0]+","+x[1]+"\n")
			
		f.close()
			
