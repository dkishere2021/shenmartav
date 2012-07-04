"""
URLs draftlaw
"""
__docformat__ = 'epytext en'

from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView

from .views import List, Detail, Info, Items, News, Alert, query
from .models import DraftLaw



urlpatterns = patterns('',
    url(r'^$', List.as_view(), name='draftlaw_list'),
    url(r'^draftlaw/(?P<slug>[-\w]+)/$', Detail.as_view(), name='draftlaw_detail'),

    # AJAX calls answered by HTML
    url(r'^info/(?P<pk>\d+)/$', Info.as_view(), name='draftlaw_info'),
    url(r'^items/(?P<page>\d+)/$', Items.as_view(), name='draftlaw_items'),
    url(r'^items/(?P<page>\d+)/(?P<query>.*)/$', Items.as_view(), name='draftlaw_items_query'),
    url(r'^news/(?P<page>\d+)/$', News.as_view(), name='draftlaw_news'),
    url(r'^alert/(?P<page>\d+)/$', Alert.as_view(), name='draftlaw_alert'),

    # AJAX calls answered by JSON
    url(r'^query/(?P<query>.*)/$', query, name='draftlaw_query'),
)