# -*- coding: utf-8 -*-
from feeds.models import Stream
from django.conf import settings


def setup_streams():

	streams = Stream.objects.all()
	
	if streams.count() == 0:
		
		news_feeds = [
			{
				'name': u'Revista Auto Esporte',
				'url': 'http://revistaautoesporte.globo.com/rss/ultimas/feed.xml'
			},
			{
				'name': u'Revista Época Negócios',
				'url': 'http://epocanegocios.globo.com/rss/ultimas/feed.xml'
			},
			{
				'name': 'Revista Quem',
				'url': 'https://revistaquem.globo.com/rss/ultimas/feed.xml'
			}
		]
		
		for feed in news_feeds:
			
			Stream.objects.create(
				name=feed['name'],
				url=feed['url']
			)