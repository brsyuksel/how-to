from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from .views import *

urlpatterns = patterns('',

	url(r'^login/$', 'django.contrib.auth.views.login', 
	{'template_name': 'admin/login.html'}, name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', 
	{'next_page': reverse_lazy('login')}, name='logout'),

	url(r'^users/$', UserList.as_view(), name='users'),
	url(r'^users/create/$', UserCreate.as_view(), name='users-create'),
	url(r'^users/update/$', UserUpdate.as_view(), name='users-update'),

	url(r'^entries/$', EntryList.as_view(), name='entries'),
	url(r'^entries/create/$', EntryCreate.as_view(), name='entries-create'),
	url(r'^entries/update/(?P<pk>\d+)/$', EntryUpdate.as_view(), 
	name='entries-update'),
	url(r'^entries/delete/(?P<pk>\d+)/$', EntryDelete.as_view(), 
	name='entries-delete'),

	url(r'^entry/(?P<pk>\d+)/$', EntryDetail.as_view(), name='entry'),
	
	url(r'^settings/$', SetBlog.as_view(), name='settings'),
)