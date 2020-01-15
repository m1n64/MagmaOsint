#!/usr/local/bin/python3
# coding: utf-8 

from requests import get
from fuzzywuzzy import fuzz
from googlesearch import search
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style, init
import sys


# colorama
init(autoreset=True)

saveInFile = "--save" in sys.argv

# Logo
print(Fore.YELLOW + '''
  █▀▄▀█ █▀▀█ █▀▀▀ █▀▄▀█ █▀▀█   █▀▀█ █▀▀ ░▀░ █▀▀▄ ▀▀█▀▀
  █░▀░█ █▄▄█ █░▀█ █░▀░█ █▄▄█   █░░█ ▀▀█ ▀█▀ █░░█ ░░█░░
  ▀░░░▀ ▀░░▀ ▀▀▀▀ ▀░░░▀ ▀░░▀   ▀▀▀▀ ▀▀▀ ▀▀▀ ▀░░▀ ░░▀░░
                                   Created by LimerBoy
''' +Fore.WHITE+"                            some modded by m1n64")

print(Fore.CYAN+'''
add --save how argument in console to save finded links in text file. File will be located in osint.py directory. Example: 
'''+Fore.MAGENTA+"python3 osint.py --save")

query   = input(Back.BLACK + Fore.YELLOW + 'Find > ' + Back.RESET + Fore.WHITE)
results = 100

print(Fore.GREEN + '[~] Searching ' + query)
for url in search(query, stop = results):
	print('\n' + Fore.CYAN + '[+] Url detected: ' + url)
	if saveInFile:
		with open(query + ".txt", "a") as file:
			file.write(url + "\n")
	try:
		text = get(url, timeout = 1).text
	except:
		continue
	soup = BeautifulSoup(text, "html.parser")
	links_detected = []
	try:
		print(Fore.MAGENTA + '[?] Title: ' + soup.title.text.replace('\n', ''))
	except:
		print(Fore.RED + '[?] Title: null')
	# Find by <a> tags
	try:
		for link in soup.findAll('a'):
			href = link['href']
			if not href in links_detected:
				if href.startswith('http'):
					# Filter
					if url.split('/')[2] in href:
						links_detected.append(href)
					# If requested data found in url
					elif query.lower() in href.lower():
						print(Fore.GREEN + '--- Requested data found at link : ' + href)
						links_detected.append(href)
						if saveInFile:
							with open(query + ".txt", "a") as file:
								file.write(href + "\n")
					# If text in link and link location is similar
					elif fuzz.ratio(link.text, href) >= 60:
						print(Fore.GREEN + '--- Text and link are similar : ' + href)
						links_detected.append(href)
						if saveInFile:
							with open(query + ".txt", "a") as file:
								file.write(href + "\n")
	except:
		continue
	if links_detected == []:
		print(Fore.RED + '--- No data found')



	
#for s in links_detected: print(s)

	