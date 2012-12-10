#!/usr/bin/python


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
				"atk", "gobject", "os", "win32api", "json", "gettext",
				"platform", "ctypes"]
	
	opts = {
		"py2exe": {
			"packages": ["encodings", "gtk", "gettext"],
			"includes": includes,
			"excludes": [],
			"optimize": "2",
			"dist_dir": "dist",
			"skip_archive": 1
		}
	}		
	
	_data_files = []
	sys.path.insert(0, os.path.abspath("./src"))
		
	setup(
		requires	= ["gtk"],
		windows	= [{"script": "src/main.py", "dest_base": "edenget"}],
		options	= opts,
		data_files = _data_files,
		**setup_info
	)
	
	print "done! files at: dist"

else:
	from setuptools import setup, find_packages
	
	# Data files to be installed to the system
	_data_files = [	]

	setup(data_files = _data_files, packages = find_packages(), **setup_info)
	print "done! files at: dist"
