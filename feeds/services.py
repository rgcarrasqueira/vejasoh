import requests
import json
from lxml import etree, cssselect, html
from lxml.html import document_fromstring, fromstring
from nested_lookup import nested_delete

def get_retrieve_content(url):
	
	feed_content = requests.get(url)
	return feed_content.content

def get_children_data(element):
	
	childrens = element.getchildren()
	
	k = {}
	
	tag = element.tag
	
	if len(childrens) > 0:
		
		k['%s'  % tag ] = []

		for child in childrens:
			
			k[tag].append(
				get_children_data(child)
			)
	else:

		k['%s'  % tag ] = element.text
		
	return k


def get_feed_data(content):
	
	content = etree.XML(content)
	
	elements = content.getchildren()
	
	feed_data = {
		'feed':[]
	}
	
	for element in elements:
		feed_data['feed'].append(get_children_data(element))

	return feed_data

def split_text_image_and_links(description):
	
	splitted_content = []
	
	document = html.document_fromstring(description)
	raw_text = document.text_content()
	
	splitted_content.append({
		'type': 'text',
		'content': raw_text
	})

	document = html.fromstring(description)
	select = cssselect.CSSSelector("img")
	images = [ el.get('src') for el in select(document) ]
	
	if len(images) == 1:
		images = images[0]
	
	splitted_content.append({
		'type': 'image',
		'content': images
	})

	document = html.fromstring(description)
	select = cssselect.CSSSelector("a")
	links = [ el.get('href') for el in select(document) ]
	
	splitted_content.append({
		'type': 'links',
		'content': links
	})
	
	return splitted_content

def upscale_dict_items(dictionary, items):

	keys = dictionary.keys()
	
	if type(items) != list:
		raise('Variable item must be a list')
	
	for key in keys:
		
		if type(dictionary[key]) == list:
		
			for item in items:
			
				if key == item:
				
					dictionary = dictionary[key]
					break
			else:
				
				if type(dictionary[key]) == list:
					
					for d in dictionary[key]:
				
						dictionary = upscale_dict_items(d, items)

	return dictionary

def delete_keys_from_dict(dictionary, keys):

	for key in keys:
		
		dictionary = nested_delete(dictionary, key)
		
	return dictionary


def prepare_feed(feed_data, upscaled_items=['channel'], remove_items=['language'], split_content=['description']):

	feed_data = upscale_dict_items(feed_data, items=upscaled_items)
	feed_data = delete_keys_from_dict(feed_data, keys=remove_items)
	
	prepared_feed = []
	
	for index, feed in enumerate(feed_data):
		
		keys = feed.keys()
		
		for key in keys:
				
			if key == 'item':
	
				for item in feed[key]:
					
					item_keys = item.keys()
					
					for item_key in item_keys:
					
						if item_key in split_content:
							
							item[item_key] = split_text_image_and_links(item[item_key])
							
				prepared_feed.append(feed)
	
	return prepared_feed

def is_json(myjson):
	
	try:
		json_object = json.loads(myjson)
	except ValueError as e:
		return False
	
	return True