from django.conf import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^admin/', include('admin.urls')),
	url(r'^', include('blog.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('django.contrib.staticfiles.views',
		url(r'^static/(?P<path>.*)$', 'serve'),
	)