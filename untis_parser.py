#!/usr/bin/env python
#
# Untis Info Vertretungsplan Parser
# History:
# Version 0.9 initial code @neo_hac0x
# Create 05.03.2015 @neo_hac0x

import urllib
from datetime import date
from bs4 import BeautifulSoup
from json import JSONEncoder as jsonEncode
base_url = "http://www.akg-bensheim.de/akgweb2011/content/Vertretung/w/"

year = date.today().year
month = date.today().month
day = date.today().day
week = str(date(year, month, day).isocalendar()[1])

url = base_url + week + "/w00000.htm"

def getVertretungsplan():
	try:
		vertretungsplan_request = urllib.urlopen(url)
		return vertretungsplan_request.read()

	except Exception as e:
		return e

def encodeandlog(data, filename):
	jsonData = jsonEncode().encode(data)
	with open(filename, "a+") as f:
		f.write(jsonData)

doc = BeautifulSoup(getVertretungsplan())

vertretung_root = {}
max_rows = len(doc.find_all("tr"))

for i in range(1,max_rows):
	tr = doc.select("tr:nth-of-type(" + str(i) +")")
	vertretung = {}
	for element in tr:
		td = element.select("td.list")
		i = 0
		for e in td:
			i = i+1
			#DEBUG: print str(i) + " " + e.string

			if i == 1:
				vertretung["klasse"] = e.string
			elif i == 2:
				vertretung["datum"] = e.string
			elif i == 3:
				vertretung["stunden"] = e.string
			elif i == 4:
				vertretung["art"] = e.string
			elif i == 5:
				vertretung["verFach"] = e.string
			elif i == 6:
				vertretung["fach"] = e.string
			elif i == 7:
				vertretung["verRaum"] = e.string
			elif i == 8:
				#TODO: fix the "---" problem (strike tag)
				vertretung["raum"] = e.string
			elif i == 9:
				vertretung["comment"] = e.string
				vertretung_root[str(vertretung["klasse"])] = vertretung
			else:
				print "[!] Something went wrong."

encodeandlog(vertretung_root, "vertretung.json")

#DEBUG: print vertretung_root