from django.conf.urls import patterns, url

from .views import *
from .feed import *
from .sitemap import *

urlpatterns = patterns('', 
	url(r'^$', EntryList.as_view(), name='blog-entries'),
	url(r'^entry/(?P<slug>[\w-]+)/$', EntryDetail.as_view(), name='blog-entry'),
	url(r'^tag/(?P<tag>[\w-]+)/$', EntryListByTag.as_view(), name='blog-tag'),

	url(r'^file/(?P<pk>\d+)/(?P<file>html|markdown)/$', EntryFile.as_view(), name='entry-file'),

	url(r'^search/$', Search.as_view(), name='search'),

	url(r'^feed/$', LatestFeed(), name='feed'),

	url(r'sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', 
		{'sitemaps':{'howto':HowtoSitemap()}}, 
		name='sitemap'
	),

)