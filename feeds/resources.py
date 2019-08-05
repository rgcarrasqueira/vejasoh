# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.db import connection
from feeds.models import Stream
from feeds.services import prepare_feed, get_retrieve_content, get_feed_data

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import  BasicAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.serializers import Serializer
from tastypie.http import HttpGone

class StreamResource(ModelResource):

    class Meta:
        queryset = Stream.objects.all()
        resource_name = 'feeds/stream'
        serializer = Serializer()
        authentication = BasicAuthentication()
        authorization = ReadOnlyAuthorization()
        always_return_data = True
        filtering = {
            "id": ('exact',),
        }
        connection.close()

    def prepend_urls(self):

        return [
            url(r"^(?P<resource_name>%s)/content/(?P<pk>\d+)/$" % self._meta.resource_name,
                self.wrap_view('feed_content'), name="api_feed_content"),
        ]

    def feed_content(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        try:
            stream = Stream.objects.get(id=kwargs['pk'])
        except Stream.DoesNotExist:
            return HttpGone()
            
        content = get_retrieve_content(stream.url)
        
        feed = get_feed_data(content)
        feed = prepare_feed(feed, upscaled_items=['channel'], remove_items=['link','image','language','copyright','guid', '{http://purl.org/dc/elements/1.1/}creator'])

        content = {
            'feed': feed
        }
        
        connection.close()
        return self.create_response(request, content)