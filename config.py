#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Created on 15.01.2010

    @author: eurekafag

    Anonbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Anonbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Anonbot.  If not, see <http://www.gnu.org/licenses/>.

'''

Settings = [ "test@radioanon.ru", "pass_goes_here" ]	# JID and password of bots account
Conferences = [ "radioanon@conference.jabber.ru" ]	# conferences which bots are joining to
Names = [ "ХУЕГЛОТ", "ОБОРМОТ", "ЗАДРОТ", "ОКТОКОТ", "АШОТ", "КАВОТ", "ЖИВОТ", "ФОКСТРОТ", "ДОСМОТ" ]
threadnum = 9						# number of bots
maxlen = 300						# max message length
maxlines = 3						# max lines
secflood = 3						# time between posts
password = "pass_for_admin"				# pass for bot admining
salt = "f439847erwgrgf$&#@RFHR_FJ"			# some random symbols for tripcode generation (change this!)
