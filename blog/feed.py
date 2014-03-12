from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.views import Feed

from .utils import get_settings
from .models import *

class LatestFeed(Feed):
	feed_type = Atom1Feed

	link = '/'
	feed_url = '/feed/'

	def __init__(self, *args, **kwargs):
		super(LatestFeed, self).__init__()

		_settings = get_settings()

		self.title = _settings['name']
		self.subtitle = _settings['html']['description']
		self.author_name = _settings['html']['author']

	def __call__(self, request, *args, **kwargs):
		self.__domain = request.get_host()
		return super(LatestFeed, self).__call__(request, *args, **kwargs)

	def items(self):
		return PublishedEntry.objects.all()[:10]

	def item_description(self, obj):
		return obj.description

	def item_author_name(self, obj):
		return obj.author.get_full_name()

	def item_pubdate(self, obj):
		return obj.modified_at

	def item_guid(self, obj):
		return "tag:{domain},{created_at}:{absolute_url}".format(
			domain=self.__domain, 
			created_at=obj.created_at.strftime("%Y-%m-%d"),
			absolute_url=obj.get_absolute_url()
		)