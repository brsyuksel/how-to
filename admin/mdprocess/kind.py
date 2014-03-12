from .base import *


class Document(Content):

	@property
	def html(self):
		_filelike = super(Document, self).html
		_filelike.write(self.body + self.sources)
		_filelike.seek(0)
		return _filelike

	@property
	def plain(self):
		_text = ' '.join([
			self.title, self.description, ' '.join(self.tags),
			self._body_text, self._sources_text
		])
		return _text.lower()



class Guide(Content):

	@property
	def html(self):
		_filelike = super(Guide, self).html
		_filelike.write(self.table_of_contents + self.body + self.sources)
		_filelike.seek(0)
		return _filelike

	@property
	def plain(self):
		_text = ' '.join([
			self.title, self.description, ' '.join(self.tags),
			self._toc_text, self._body_text, self._sources_text
		])
		return _text.lower()



class Trick(Content):

	@property
	def html(self):
		_filelike = super(Trick, self).html
		_filelike.write(self.body)
		_filelike.seek(0)
		return _filelike

	@property
	def plain(self):
		_text = ' '.join([
			self.title, self.description, ' '.join(self.tags),
			self._body_text
		])
		return _text.lower()