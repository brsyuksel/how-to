from markdown2 import Markdown
from bs4 import BeautifulSoup

from .base import get_kind_class
from .kind import *
from .html import *

class Process(object):
	def __init__(self, mdf, kind):
		self.__markdown = mdf
		self.kindcls = get_kind_class(kind)

	def _strip_tags(self, text):
		soup = BeautifulSoup(text)
		return soup.get_text(' ',strip=True).replace('\n', ' ')

	def _check_metadata(self, metadata):
		assert metadata, "file has no contain metadata"

		assert all(metadata.get(k) for k in ['title', 'description', 'tags']), \
		"invalid metadata"

	def _regulate_metadata(self, metadata):
		self._check_metadata(metadata)

		title = self._strip_tags(metadata['title'])
		desc = self._strip_tags(metadata['description'])
		tags = set(map(
			lambda x: x.strip(), 
			self._strip_tags(metadata['tags']).split(',')
		))

		return title, desc, tags

	def _remove_child_headers(self, toc, md_inst, add_references):
		if not toc:
			return []

		_toc = []
		body_soup = BeautifulSoup(md_inst)
		for toc_item in toc:
			header = body_soup.find(id=toc_item[1])
			if not header:
				continue

			if header.parent.name != "[document]":
				continue

			_toc.append((toc_item[0], '#'+toc_item[1], toc_item[2]))

		add_references and _toc.append((1, u'#references', u'references'))
		return _toc

	def _generate_toc_data(self, toc, md_inst, add_references=False):
		_toc = self._remove_child_headers(toc, md_inst, add_references)
		_toc_html = ''
		for line in TableOfContents.html(_toc):
			_toc_html += line
		return _toc, _toc_html

	def _regulate_references_links(self, refs):
		_refs = set([(1,v,k) for k,v in refs.items()])
		return list(_refs)
	
	def _generate_sources_html(self, refs):
		_refs = self._regulate_references_links(refs)
		_source_html = ''
		for line in References.html(_refs):
			_source_html += line
		return _source_html

	def convert(self):
		mdowner = Markdown(extras=[
			'toc', 'header-ids', 'fenced-code-blocks', 'metadata', 'pyshell'
		])

		md_text = self.__markdown.read()
		md_inst = mdowner.convert(md_text)

		title, description, tags = self._regulate_metadata(md_inst.metadata)
		
		toc, toc_html = self._generate_toc_data(
			md_inst._toc, md_inst, bool(mdowner.urls)
		)
		
		sources_html = self._generate_sources_html(mdowner.urls)
		
		_content = self.kindcls(self.__markdown, title, description, tags, toc)
		_content.table_of_contents = toc_html
		_content.body = md_inst
		_content.sources = sources_html

		return _content