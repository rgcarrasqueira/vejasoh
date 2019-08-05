# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory

from tastypie.test import ResourceTestCaseMixin
from tastypie.models import ApiKey

from feeds.services import get_children_data, get_feed_data, get_retrieve_content
from feeds.services import prepare_feed, split_text_image_and_links
from feeds.services import upscale_dict_items, delete_keys_from_dict, is_json
from nested_lookup import nested_lookup, get_occurrence_of_key

from model_mommy import mommy

# Create your tests here.

class TestServices(TestCase):
	
	def setUp(self):
		pass
	
	def test_get_feed_data(self):
		
		content = get_retrieve_content('https://revistaautoesporte.globo.com/rss/ultimas/feed.xml')
		feed = get_feed_data(content)
		
		assert 'feed' in feed
		assert 'channel' in feed['feed'][0]
		assert 'item' in feed['feed'][0]['channel'][6]
		
	def test_split_text_image_and_links(self):
		
		content = get_retrieve_content('https://revistaautoesporte.globo.com/rss/ultimas/feed.xml')
		feed = get_feed_data(content)
		
		description = feed['feed'][0]['channel'][6]['item'][1]['description']
		
		description = split_text_image_and_links(description)
		
		assert description[0]['type'] == 'text'
		assert description[1]['type'] == 'image'
		assert description[2]['type'] == 'links'
		
		
	def test_upscale_dict_items(self):
		
		content = get_retrieve_content('https://revistaautoesporte.globo.com/rss/ultimas/feed.xml')
		feed_data = get_feed_data(content)
		feed = upscale_dict_items(feed_data, items=['channel'])
		
		assert feed == feed_data['feed'][0]['channel']
		
	def test_delete_keys_from_dict(self):
		
		content = get_retrieve_content('https://revistaautoesporte.globo.com/rss/ultimas/feed.xml')
		feed_data = get_feed_data(content)
		feed_data = upscale_dict_items(feed_data, items=['channel'])
		feed = delete_keys_from_dict(feed_data, keys=['language','copyright','guid', '{http://purl.org/dc/elements/1.1/}creator'])
		
		assert len(nested_lookup(feed,'language')) == 0
		assert len(nested_lookup(feed,'copyright')) == 0
		assert len(nested_lookup(feed,'guid')) == 0
		assert len(nested_lookup(feed,'{http://purl.org/dc/elements/1.1/}creator')) == 0

		
	def test_prepare_json(self):
		
		content = get_retrieve_content('https://revistaautoesporte.globo.com/rss/ultimas/feed.xml')
		feed = get_feed_data(content)
		feed = prepare_feed(feed, upscaled_items=['channel'], remove_items=['link','image','language','copyright','guid', '{http://purl.org/dc/elements/1.1/}creator'])

		assert 'item' in feed[4]
		

class TestResources(ResourceTestCaseMixin, TestCase):
	
	def setUp(self):

		super(TestResources, self).setUp()
		
		self.username = 'fulano'
		self.password = 'senha'
		self.user = User.objects.create_user(self.username, 'fulano@infoglobo.com.br', self.password)
		self.user.is_active = True
		self.user.save()

	def get_credentials(self):
		return self.create_basic(username=self.username, password=self.password)
	
	def test_get_list_unauthenticated(self):
		self.assertHttpUnauthorized(self.api_client.get('/api/v1/feeds/stream/', format='json'))

	def test_get_feed_from_stream(self):
		
		stream = mommy.make(
			'feeds.Stream',
			name='Revista Auto Esporte',
			url='https://revistaautoesporte.globo.com/rss/ultimas/feed.xml'
		)
	
		resp = self.api_client.get('/api/v1/feeds/stream/content/%s/' % stream.id,
										authentication=self.get_credentials(),
										format='json'
										)
		assert resp.status_code == 200
