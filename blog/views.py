from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.cache import cache

from .models import *
from .collections import *

class EntryList(ListView):
	model = PublishedEntry
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(EntryList, self).get_context_data(**kwargs)

		object_list = context['object_list']
		entries = []
		for obj in object_list.all():
			if obj.kind != 'trk':
				entries.append({'object':obj, 'html':''})
				continue

			cache_key = 'howto_entry_'+str(obj.content)
			_entry_cache = cache.get(cache_key, {})
			_html = _entry_cache.get('html', None)
			if not _html:
				try:
					content = Content.objects.get(pk=obj.content)
				except:
					raise Http404
				else:
					_html = content.html.read()
					_entry_cache.update({'html':_html})
					cache.set(cache_key, _entry_cache)
			
			entries.append({'object':obj, 'html':_html})

		context.update({'entries':entries})
		return context

class EntryListByTag(EntryList):
	template_name = 'blog/publishedentry_list.html'

	def get_queryset(self):
		tagobj = get_object_or_404(Tag, label=self.kwargs['tag'])
		return tagobj.entry_set.filter(publish=True)

class EntryDetail(DetailView):
	model = PublishedEntry
	context_object_name = 'entry'

	def get_context_data(self, **kwargs):
		context = super(EntryDetail, self).get_context_data(**kwargs)

		cache_key = 'howto_entry_'+str(self.object.content)
		_entry_cache = cache.get(cache_key, {})

		if not _entry_cache.get('html', None) or \
		_entry_cache.get('toc', None) is None:
			try:
				content = Content.objects.get(pk=self.object.content)
			except:
				raise Http404
			else:
				_html = content.html.read()
				_toc = content.toc
				_entry_cache.update({'html': _html, 'toc':_toc})
				cache.set(cache_key, _entry_cache)

		context["entry_html"] = _entry_cache['html']
		context["toc"] = _entry_cache['toc']
		return context

class EntryFile(DetailView):
	model = Entry

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		content = Content.objects.get(pk=self.object.content)
		files = {
			'html': content.html if self.request.user.is_authenticated() \
			else content.markdown,
			'markdown': content.markdown
		}
		response = HttpResponse(content_type='text/plain; charset=utf-8')
		response.write(files.get(kwargs['file']).read())
		return response

class Search(EntryList):
	def get_queryset(self):
		_skey = self.request.GET.get('key', None)
		if not _skey:
			return super(Search, self).get_queryset()

		if settings.MONGODB_DATABASE.get('CONF',{}).get('USE_TEXTSEARCH', None):
			col_content = Content._get_collection()
			col_content.ensure_index([('plain', 'text')], background=True)

			db = col_content.database

			results = db.command('text', 'content', search=_skey)
		else:
			import re
			_sr = re.compile('|'.join(_skey.split()), re.IGNORECASE)

			Content.ensure_indexes()
			res = Content._get_collection().find({'keywords':{
				'$regex': _sr
			}}, fields=['_id'])

			results = {}
			results['results'] = [{'obj':r} for r in res]

		content_ids = [str(k['obj']['_id']) for k in results['results']]
		if not content_ids:
			raise Http404
		
		queryset = super(Search, self).get_queryset().filter(
			content__in=content_ids
		)

		return queryset