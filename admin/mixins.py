from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.utils.text import slugify
from django.core.cache import cache

from .mdprocess import *
from blog.models import *
from blog.collections import *

class AdminTemplateFilesMixin(TemplateResponseMixin):
	def get_template_names(self):
		files = super(AdminTemplateFilesMixin, self).get_template_names()
		return map(lambda f: 'admin/' + f.split('/')[-1], files)

class FormFieldCSSMixin(FormMixin):
	def get_form(self, form_class):
		from django.forms.widgets import CheckboxInput
		
		form = super(FormFieldCSSMixin, self).get_form(form_class)
		for field in form.fields:
			widget = form.fields[field].widget
			if isinstance(widget, CheckboxInput):
				continue
			widget.attrs['class'] = 'form-control'
		return form

class LoginRequiredMixin(View):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class EntrySaveMixin(FormMixin):
	def form_valid(self, form):
		r2r_wargs = lambda **e: self.render_to_response(self.get_context_data(
			**e
		))

		try:
			def markdown_file():
				try:
					contentobj = Content.objects.get(pk=form.instance.content)
				except:
					contentobj = None

				if form.cleaned_data.get('markdown', None):
					return contentobj, form.cleaned_data['markdown']

				try:
					from cStringIO import StringIO
				except:
					from StringIO import StringIO

				markdown_f = StringIO()
				markdown_f.write(contentobj.markdown.read())
				markdown_f.seek(0)
				return contentobj, markdown_f

			contentobj, markdown = markdown_file()

			kind = form.instance.get_kind_display()

			md_proc = MDProcess(markdown, kind)
			content = md_proc.convert()

			user = User.objects.get(pk=self.request.user.id)
			
			with transaction.atomic():
				form.instance.title = content.title
				form.instance.description = content.description
				form.instance.slug = slugify(content.title)
				if not form.instance.id:
					form.instance.author = user
				entry = form.save()

				entry.tags.clear()

				for label in content.tags:
					tag, created = Tag.objects.get_or_create(
						label=slugify(label)
					)
					entry.tags.add(tag)
				
				if not contentobj:
					contentobj = Content()
					contentobj.html.put(
						content.html, 
						content_type='text/html',
						encoding='utf-8'
					)
					contentobj.markdown.put(
						content.markdown, 
						content_type='text/x-markdown',
						encoding='utf-8'
					)
				else:
					contentobj.html.replace(
						content.html, 
						content_type='text/html',
						encoding='utf-8'
					)
					contentobj.markdown.replace(
						content.markdown, 
						content_type='text/x-markdown',
						encoding='utf-8'
					)

				contentobj.plain = content.plain
				contentobj.keywords = content.keywords
				contentobj.toc = content.toc
				contentobj.save()
				
				entry.content = contentobj.id
				entry.save()

				entry_cache_key = 'howto_entry_'+str(contentobj.id)
				cache.delete(entry_cache_key)

		except Exception as e:
			return r2r_wargs(form=form, errors=[e])

		return super(EntrySaveMixin, self).form_valid(form)