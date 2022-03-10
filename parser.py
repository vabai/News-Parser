from urllib.request import urlopen
from bs4 import BeautifulSoup
import random, re, json, datetime, time
annotation_f = open('annotation.txt','w')
titles = ''
annotations = ''
preview = ''
publishedAt = 0
content = ''
image = []
s1 = ''
s2 = ''
prev = False
tags = [{"title": "Важно","color": "negative"},
        {"title": "Информация","color": "info"},
        {"title": "Обучение","color": "primary"},
        {"title": "Самодеятельность","color": "positive"},
   		{"title": "Внутреннее событие","color": "accent"},
        {"title": "Абитурьенту","color": "grey"}]
month = {'Декабрь':'12,','Январь':'01,','Февраль':'02,',
		 'Март':'03,','Апрель':'04,','Май':'05,',
		 'Апрель':'04,','Май':'05,','Июнь':'06,',
		 'Июль':'07,','Август':'08,','Сентябрь':'09,',
		 'Октябрь':'10,','Ноябрь':'11,'}
data = {
	"data": []
}
data_id_i = 1
data_id_j = 0
m = {}

for i in range(33):
	html = urlopen("http://www.skf-mtusi.ru/?cat=6&paged="+str(i))
	bsObj = BeautifulSoup(html.read(),features="html.parser")
	entry = bsObj.findAll('div',{'class':'entry'})
	
	for post in entry:
		
		#titles
		s1=''	
		for link in post.findAll('h1'):
			s1 += link.a.text
			titles = s1
		s1=''
		
		#annotations
		
		s2 = ''
		for j in post.findAll('p'):
			s2+=j.text
		annotations = s2[:len(s2)-17]
		
		#preview
		prev = False
		m = post.find('div',{'style':"float:left; padding: 0 10px 0 0;"})
		if m:
			prev = m
			for i in prev:
				preview = prev.img['src']
		
		
		for link in (post).findAll('h1'):
			s3 = ''
			html2 = urlopen(link.a['href'])
			obj2 = BeautifulSoup(html2.read(),features="html.parser",from_encoding="utf-8")
			entryIn = obj2.findAll('div',{'class':'entry'})
			
			#content
			for article in entryIn:
				for i in article.findAll('p'):
					s3+=i.text
				content = s3
		
			#image
			postObj = obj2.findAll('div',{'class':'post'})
			for i in postObj:
				imgs = i.findAll('img')
				srcs = []
				for j in imgs:
					srcs.append(j['src'])
				image = srcs
		m = {
			'id': data_id_i,
			'options': {
				'visible': ['all'],
				'tags': [random.choice(tags)],
				'createdBy': { 'uid': 1, 'name':'СКФ МТУСИ' },
				'publishedBy': { 'uid': 0, 'name': 'Avem system deamon'},
				'publishedAt': 0,
				'edited': False,
				'meta': ['Новости СКФ МТУСИ']
			},
			'preview': preview,
			'image': image if len(image)!=0 else False,
			'title': titles,
			'annotation': annotations,
			'content': content
		}
		data_id_i += 1
		data['data'].append(m)

	#publishedAt
	category = bsObj.findAll('div',{'class':'category'})

	for i in category:
		for j in i.findAll('p',{'align':'right'}):
			publishedAt = j.text
			m = publishedAt.split(' ')[0]
			publishedAt = publishedAt.replace(m, month[m])
			ms = publishedAt.split(', ')
			ms = ms[2]+'-'+ms[0]+'-'+ms[1]
			publishedAt = 1000*int(time.mktime(time.strptime(ms, '%Y-%m-%d')))
			data['data'][data_id_j]['options']['publishedAt'] = publishedAt
		data_id_j += 1

with open("parsed.json","w", encoding='utf-8') as parsed:
	json.dump(data, parsed,ensure_ascii=False)