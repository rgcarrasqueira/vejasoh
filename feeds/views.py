from django.shortcuts import render

from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from vejasoh.mixins import JSONResponseMixin
from feeds.models import Stream
from feeds.services import get_retrieve_content, get_feed_data, prepare_feed

class IndexView(ListView):
    
    model = Stream
    context_object_name = 'streams'
    template_name = "feeds/stream/stream_index.html"
    paginate_by = 10
    
    def get_queryset(self):
        streams = Stream.objects.all().order_by('name')
        return streams

class FeedJsonView(JSONResponseMixin, DetailView):
    
    def get_object(self):
        
        stream_id = self.kwargs['pk']
        stream = get_object_or_404(Stream, id=stream_id)
        
        return stream
        
    def get_context_data(self, *args, **kwargs):
        
        stream = self.get_object()
        
        content = get_retrieve_content(stream.url)
        
        feed = get_feed_data(content)
        feed = prepare_feed(feed, upscaled_items=['channel'],
                            remove_items=['link','image','language','copyright','guid', '{http://purl.org/dc/elements/1.1/}creator'])

        context = {
            'feed': feed
        }
        
        return context
