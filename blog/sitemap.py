from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from .models import PublishedEntry

class HowtoSitemap(Sitemap):
	changefreq = "never"
	priority = 0.9

	def items(self):
		return PublishedEntry.objects.all()

	def lastmod(self, obj):
		return obj.modified_at

	def location(self, obj):
		return obj.get_absolute_url()