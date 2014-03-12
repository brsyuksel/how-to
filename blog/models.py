from types import StringTypes
from hashlib import md5

from django.db import models
from django.contrib.auth.models import User as authUser

from .fields import ObjectIdField

class User(authUser):
	class Meta:
		proxy = True

	@property
	def gravatar(self):
		return 'http://gravatar.com/avatar/' + md5(self.email).hexdigest()

class Common(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True
		ordering = ['-created_at']

	def __unicode__(self):
		attr = self.__class__.__name__ if not hasattr(self.__class__, \
		'unicode_attr') else getattr(self, self.__class__.unicode_attr)

		return attr if isinstance(attr, StringTypes) else \
		self.__class__.__name__


class Tag(Common):
	label = models.CharField(max_length=30, unique=True)

	unicode_attr = 'label'

	@models.permalink
	def get_absolute_url(self):
		return ('blog-tag', [str(self.label)])


class Entry(Common):
	kind = models.CharField(max_length=3, choices=(('doc', 'Document'),\
	('gde', 'Guide'), ('trk', 'Trick')), default='doc')
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=250, blank=True)
	content = ObjectIdField(null=True)
	tags = models.ManyToManyField(Tag)
	slug = models.SlugField(max_length=120, unique=True)
	publish = models.BooleanField(default=False)
	author = models.ForeignKey(User)

	unicode_attr = 'title'

	@models.permalink
	def get_absolute_url(self):
		return ('blog-entry', [str(self.slug)])


class PublishedEntryManager(models.Manager):
	def get_queryset(self):
		return super(PublishedEntryManager, self).get_queryset().filter(
			publish=True
		)


class PublishedEntry(Entry):
	objects = PublishedEntryManager()

	class Meta:
		proxy = True