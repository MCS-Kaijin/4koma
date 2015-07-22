# coding: utf-8

import requests
import zipfile
import sys
import re
import os

# get manga title
manga = raw_input('Manga: ').strip().lower()
dirname = manga.replace(' ','-')
if not os.path.exists(dirname): os.mkdir(dirname)
os.chdir(dirname)
manga = manga.replace(' ', '_')

# get links on main manga page
url = 'http://www.mangatown.com/manga/{}'.format(manga)
source = requests.get(url, stream=True)
source = source.content.split('\n')
links = []

for line in source:
	link = re.match((r'[^a]+a href="(?P<href>[^"]+)".+'), line)
	if link:
	tmp = re.search((r'{}'.format(manga)), link.group('href'))
	if tmp:
	links.append(link.group('href'))

#visit each link and extract all the pages in each chapter
with open('links.txt', 'w') as f:
	pass
	
img_urls = []
new_links = []
links.reverse()
for link in links:
	print 'Getting links from: '+link
	source = requests.get(link, stream=True)
	source = source.content.split('\n')
	for line in source:
	new_link = re.match((r'[^o]+option value="http(?P<href>[^"]+).+'), line)
	if new_link:
	try:
	l = new_links.index('http'+new_link.group('href'))
	new_links.pop()
	except:
	new_links.append('http'+new_link.group('href'))
i = 0
with open('links.txt', 'r') as f:
	lnks = f.read().split('\n')
	if lnks:
	for link in lnks:
	try: new_links.remove(link)
	except: pass
	i += 1
for link in new_links:
	print 'Downloading: '+link
	source = requests.get(link, stream=True)
	source = source.content.split('\n')
	for line in source:
	tmp1 = re.search((r'[^<]+id="image".+'), line)
	if tmp1:
	tmp = re.search((r'src="(?P<img_url>[^"]+).+'), tmp1.group())
	print tmp.group('img_url')
	if tmp:
	img_urls.append(tmp.group('img_url'))
	txt = ''
	with open('links.txt', 'r') as f:
	txt = f.read()
	with open('links.txt', 'w') as f:
	f.truncate()
	f.write(txt+'\n'+link)

# download images
for img in img_urls:
	print 'Getting image: '+img
	im = requests.get(img, stream=True)
	with open(dirname+'_'+str(i)+'.jpg', 'wb') as f:
	f.write(im.content)
	i+=1
os.chdir('..')
op = raw_input('Make zip file? ')
if(op == 'y'):
	with zipfile.ZipFile(dirname+'.zip', 'w') as z:
	for root, dirs, files in os.walk(dirname):
	for file in files:
	z.write(os.path.join(root, file))
with open('pageturnedx', 'w') as f:
	f.write('0')
print 'Done.'
