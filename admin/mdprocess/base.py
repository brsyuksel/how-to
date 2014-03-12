import abc
from functools import partial
from bs4 import BeautifulSoup

try:
	from cStringIO import StringIO
except:
	from StringIO import StringIO

class Content(object):
	__metaclass__ = abc.ABCMeta

	def __init__(self, markdown, title, desc, tags, toc):
		self._markdown = markdown
		self._title = title
		self._desc = desc
		self._tags = tags
		self._toc = toc

		self._toc_html = self._toc_text = ''
		self._body_html = self._body_text = ''
		self._sources_html = self._sources_text = ''

	@property
	def markdown(self):
		self._markdown.seek(0)
		return self._markdown

	@property
	def title(self): return self._title

	@property
	def description(self): return self._desc

	@property
	def tags(self): return self._tags

	@property
	def toc(self): return self._toc

	def __html_and_text_setter(self, html, name):
		setattr(self, name+'_html', html.encode('utf-8'))
		_soup = BeautifulSoup(html)
		_stripped = _soup.get_text(' ',strip=True).replace('\n', ' ')
		setattr(self, name+'_text', _stripped)

	table_of_contents = property(
		lambda self: self._toc_html,
		partial(__html_and_text_setter, name='_toc')
	)

	body = property(
		lambda self: self._body_html,
		partial(__html_and_text_setter, name='_body')
	)

	sources = property(
		lambda self: self._sources_html,
		partial(__html_and_text_setter, name='_sources')
	)

	@abc.abstractproperty
	def html(self):
		_filelike = StringIO()
		return _filelike

	@abc.abstractproperty
	def plain(self):
		return

	@property
	def keywords(self):
		keys = self.plain.split()
		return list(set(k.lower() for k in keys if k.isalpha()))

def get_kind_class(kind):
	for kcls in Content.__subclasses__():
		if kind == kcls.__name__:
			return kcls
	raise RuntimeError('invalid kind')