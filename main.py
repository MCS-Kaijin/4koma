# coding: utf-8

import requests
import re
import ui

gui = ui.load_view('main')

page = 1

def get_yonkoma(url):

	source = requests.get(url).content.split('\n')

	entries = []

	for line in range(0, len(source)-1):
		tmp = re.match((r'[^<]+<article class="entry.+'), source[line])
		if tmp:
			info = []
			line += 1
			tmp = re.search((r'href="(?P<href>[^"]+)'), source[line])
			if tmp:
				ns = requests.get(tmp.group('href')).content.split('\n')
				for nl in range(0, ns.index(ns[-1])):
					tmp = re.search((r'div class="body"'), ns[nl])
					if tmp:
						nl += 1
						tmp = re.search((r'src="(?P<src>[^"]+)'), ns[nl])
						if tmp:
							info.append(tmp.group('src'))
			line += 2
			tmp = re.search((r'alt="(?P<alt>[^"]+)'), source[line])
			if tmp:
				info.append(tmp.group('alt'))
			tmp = re.search((r'src="(?P<src>[^"]+)'), source[line])
			if tmp:
				info.append(tmp.group('src'))
			line += 7
			tmp = {'comic': info[0], 'title': info[1], 'preview': info[2]}
			entries.append(tmp)
	return entries

def hide_yonkama(sender):
	vw = sender.superview
	sender.alpha = 0
	vw['scrollview1'].alpha = 1

def view_yonkama(obj):
	vw = gui['view1']
	vw['scrollview1'].alpha = 0
	vw['webview1'].load_url(obj.href)
	vw['button1'].alpha = 1

class viw(ui.View):
	tx, ty = 0, 0
	def __init__(self, href):
		self.href = href
	def touch_began(self, touch):
		self.tx, self.ty = touch.location
	def touch_ended(self, touch):
		x, y = touch.location
		if x < self.tx+50 and x > self.tx-50 and y < self.ty+50 and y > self.ty-50:
			view_yonkama(self)

y = 0
def add_yonkoma(entries):
	global y
	for entry in entries:
		w, h = gui['view1']['scrollview1'].content_size
		h += 110
		im = ui.ImageView()
		im.load_from_url(entry['preview'])
		im.frame = (0, y, 100, 100)
		lbl = ui.Label()
		lbl.text = entry['title']
		lbl.frame = (110, y+40, 500, 20)
		vw = viw(entry['comic'])
		vw.frame = (0, y, 610, 100)
		y += 110
		gui['view1']['scrollview1'].add_subview(im)
		gui['view1']['scrollview1'].add_subview(lbl)
		gui['view1']['scrollview1'].add_subview(vw)
		gui['view1']['scrollview1'].content_size = (w,h)
entries = get_yonkoma('http://4komaparty.com')
add_yonkoma(entries)

def load_more(sender):
	global page
	page += 1
	entries = get_yonkoma('http://4komaparty.com/page/{}'.format(page))
	add_yonkoma(entries)

gui['view1']['button1'].action = hide_yonkama
gui['view1']['button1'].alpha = 0
gui['view1']['button2'].action = load_more

gui.present(hide_title_bar=True)
