# -*- coding: utf-8 -*-

from feeds.resources import StreamResource
from tastypie.api import Api

# API Registering

api = Api(api_name='v1')

# Stream Resource
api.register(StreamResource())