# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _
from feeds.models import Stream


# Register your models here.

class StreamAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'url',
        'date_created',
		'last_updated',
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'date_created',
    )

admin.site.register(Stream, StreamAdmin)