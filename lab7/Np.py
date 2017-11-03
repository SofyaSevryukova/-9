from __future__ import division
from bs4 import BeautifulSoup
from sqlalchemy import Column, String, Integer, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bottle import route, run, template, request, redirect, static_file
from stemming.porter2 import stem
from collections import defaultdict
from math import log
import operator
import requests
import time


site = "http://www.technewsworld.com"
lastSite = "http://www.technewsworld.com/perl/archives/tnw/?init=1100"

classes = None
predictWords = None

Base = declarative_base()

class News(Base):
	__tablename__ = "news"
	id = Column(Integer, primary_key = True)
	title = Column(String)
	date = Column(String)
	url = Column(String)
	label = Column(String)
	teaser = Column(String)
	predict = Column(String)

def get_news(htmlText):
	page = BeautifulSoup(htmlText, 'html.parser')
	newsColl = page.body.find_all("div", class_ = 'story-list')

	print(str(len(newsColl)) + " news pages found")	
	
	newsList = []
	for x in range(len(newsColl)):
		_title = newsColl[x].find("div", class_ = "title").find("a").text
		_date = newsColl[x].find("div", class_ = "date").text
		_url = site + newsColl[x].find("div", class_ = "title").find("a").get("href")
		_teaser = newsColl[x].find("div", class_ = "teaser").text
		
		newsList.append({"title": _title, "date": _date, "url": _url, "teaser": _teaser})

	return newsList


def updateDB(dataDict):
	s = session()
	
	counter = 0
	for x in range(0, len(dataDict)):
		if s.query(News).filter_by(url=dataDict[x]['url']).scalar() == None:
			s.add(News(title = dataDict[x]['title'], date = dataDict[x]['date'], url = dataDict[x]['url'], teaser = dataDict[x]['teaser']))
			counter = counter + 1
			
	print(str(counter) + " news added to DB")
	s.commit()


@route('/static/<filename>')
def server_static(filename):
	return static_file(filename, root='static')
	

@route('/news')
def news_list():
	train()
	s = session()
	rows = s.query(News).filter(News.label == None).all()
	if classes != None and predictWords != None:
		for r in range(len(rows)):
			rows[r].predict = classify(rows[r].title)
		s.commit()
		
		rows.sort(key=operator.attrgetter('predict'))

	return template('news_template', rows=rows, lastSite=lastSite)
	

@route('/add_label')
@route('/')
def add_label():
	s = session()
	# 1. Получить значения параметров label и id из GET-запроса
	label = request.query.label
	newsID = request.query.id	
	# 2. Получить запись из БД с соответствующим id (такая запись только одна!)
	newsRow = s.query(News).filter(News.id == newsID).first()
	# 3. Изменить значение метки записи на значение label
	newsRow.label = label
	# 4. Сохранить результат в БД
	s.commit()
	redirect("/news")
	

@route('/update_news')
@route('/')
def update_news():
	s = session()
	global lastSite		
	lastSite = "http://www.technewsworld.com/perl/archives/tnw/?init=" + str(len(s.query(News).all()))
	
	lastSitePage = BeautifulSoup(requests.get(lastSite).text, 'html.parser')
	lastSite = site + lastSitePage.body.find("div", {"id": "earlier"}).find("a").get("href")
	# 1. Получить данные с новостного сайта	
	print('Getting news from ' + lastSite)
	
	newsData = get_news(requests.get(lastSite).text)	
	# 2. Проверить каких новостей еще нет в БД. Будем считать,
	#    что каждая новость может быть уникально идентифицирована
	#    по совокупности двух значений: заголовка и автора 
	# 3. Сохранить в БД те новости, которых там нет
	updateDB(newsData)
	redirect('/news')


# @route('/load_all')
# def load_all():
# 	s = session()
# 	counter = 0
# 	attempts = 0
# 	while counter < 100 and attempts < 3:
# 		global lastSite		
# 		lastSite = "http://www.technewsworld.com/perl/archives/tnw/?init=" + str(len(s.query(News).all()))
		
# 		lastSitePage = BeautifulSoup(requests.get(lastSite).text, 'html.parser')
# 		lastSite = site + lastSitePage.body.find("div", {"id": "earlier"}).find("a").get("href")
		
# 		print('Getting news from ' + lastSite)
# 		newsData = get_news(requests.get(lastSite).text)	
		
# 		lastAdd = 0
# 		for x in range(0, len(newsData)):
# 			if s.query(News).filter_by(url=newsData[x]['url']).scalar() == None:
# 				s.add(News(title = newsData[x]['title'], date = newsData[x]['date'], url = newsData[x]['url'], teaser = newsData[x]['teaser']))
# 				counter += 1
# 				lastAdd += 1
		
# 		print(str(lastAdd) + " loaded")
		
# 		if lastAdd == 0 and counter != 0:
# 			attempts += 1
		
				
# 		s.commit()
		
	print(str(counter) + " news added to DB")
	print()
	redirect('/news')
	

@route('/justify')
def manageLabeled():
	s = session()
	goodRatio = 0
	maybeRatio = 0
	neverRatio = 0
	
	unlabeled = s.query(News).filter_by(label = None).all()
	labeled = s.query(News).filter_by(label != None).all()
	
	for x in range(len(labeled)):
		pass		


def classify(title):
	result = min(classes.keys(), key = lambda cl: -log(classes[cl]) + \
			sum(-log(predictWords.get((cl, stem(word)), 10**(-7))) for word in title.split() ))
	return result
 
 
@route('/train')
def redirectTrain():
	train()
	redirect("/news")


def train():
	global classes, predictWords
	classes, predictWords = defaultdict(lambda: 0), defaultdict(lambda: 0)
	s = session()
	labeled_articles = s.query(News).filter(News.label != None).all()
	for article in labeled_articles:
		classes[article.label] += 1
		words = article.title.split()
		for word in words:
			predictWords[article.label, stem(word)] += 1
 
	for label, word in predictWords:
		predictWords[label, word] /= classes[label]
	for c in classes:
		classes[c] /= len(labeled_articles)
		
	print(str(len(labeled_articles)) + " titles inspected.")

##################################################################################
engine = create_engine("sqlite:///news.db")
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)

# req = requests.get(site)
# newsData = get_news(req.text)
# updateDB(newsData)

# Start bottle
run(host='localhost', port=8080)