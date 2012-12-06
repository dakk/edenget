#!/usr/bin/python

from setuptools import setup, find_packages

import os
import platform
import sys


setup_info = dict(
	name = "edenget",
	version = open("VERSION","r").read(),
	description = "a multiplatform batch downloader for mangaeden.com",
	author = open("AUTHORS","r").read(),
	author_email = "gessadavide@gmail.com",
	keywords = "mangaeden manga batch",
	long_description = """edenget is a multiplatform batch downloader for mangaeden.com""",
	url = "http://dakk.github.com/edenget",
	license = "GNU GPL 2",
	classifiers = [
		"License :: OSI Approved :: GNU General Public License (GPL)",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
	],
	ext_package = "edenget",
	include_package_data = True,
	package_data = {
		"edenget": [
		]
	}
)

if os.name == "nt":
	from distutils.core import setup
	import py2exe


	includes = ["locale", "gio", "cairo", "pangocairo", "pango",
				"atk", "gobject", "os", "code", "winsound", "win32api",
				"plistlib", "win32gui", "OpenSSL", "Crypto", "Queue", "sqlite3",
				"glob", "webbrowser", "json", "imaplib", "cgi", "gzip", "uuid",
				"platform", "imghdr", "ctypes", "optparse", "plugin_base",
				"pyfb", "papyon", "e3.xmpp", "plugins", "webkit",
				"unicodedata", "dnspython"]
	
	opts = {
		"py2exe": {
			"packages": ["encodings", "gtk", "OpenSSL", "Crypto", "xml",
						 "xml.etree", "xml.etree.ElementTree"],
			"includes": includes,
			"excludes": ["appindicator", "ltihooks", "pywin", "pywin.debugger",
				"pywin.debugger.dbgcon", "pywin.dialogs",
				"pywin.dialogs.list", "Tkconstants", "Tkinter", "tcl",
				"doctest", "macpath", "pdb", "cookielib", "ftplib",
				"pickle", "win32wnet", "unicodedata",
				"getopt", "gdk"],
			"dll_excludes": ["libglade-2.0-0.dll", "w9xpopen.exe"],
			"optimize": "2",
			"dist_dir": "dist",
			"skip_archive": 1
		}
	}		
	
	_data_files = []
	sys.path.insert(0, os.path.abspath("./dlls"))
	sys.path.insert(0, os.path.abspath("./src"))
		
	setup(
		requires	= ["gtk"],
		windows	= [{"script": "main.py", "icon_resources": [(1, "edenget.ico")], "dest_base": "edenget"}],
		options	= opts,
		data_files = _data_files,
		**setup_info
	)
	print "done! files at: dist"

else:
	# Data files to be installed to the system
	_data_files = [	]

	setup(data_files = _data_files, packages = find_packages(), **setup_info)
	print "done! files at: dist"
