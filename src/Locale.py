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

import locale
import os
import sys
import gettext

APP_NAME = "edenget"

class Locale:
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
		return cls._instance
	
	# Locale init
	local_path = os.path.realpath(os.path.dirname(sys.argv[0]))

	langs = []
		
	lc, encoding = locale.getdefaultlocale()
	if (lc):
		langs = [lc]

	language = os.environ.get('LANGUAGE', None)
	if (language):
		langs += language.split(":")
	langs += ["it_IT", "en_US"]

	gettext.bindtextdomain(APP_NAME, local_path)
	gettext.textdomain(APP_NAME)
	
			
	lang = gettext.translation(APP_NAME, local_path, languages=langs, fallback = True)
			
	_ = lang.gettext
