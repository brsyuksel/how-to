from django.views.generic import *
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.db import transaction
from django.utils.text import slugify
from django.core.cache import cache

from json import loads as json_loads

from blog.models import *
from blog.collections import *
from .forms import *
from .mixins import *

class UserList(AdminTemplateFilesMixin, LoginRequiredMixin, ListView):
	queryset = User.objects.annotate(entries=Count('entry'))
	context_object_name = 'users'
	paginate_by = 10


class UserCreate(AdminTemplateFilesMixin, LoginRequiredMixin, \
FormFieldCSSMixin, FormView):
	form_class = UserCreationForm
	template_name = 'user_form.html'
	success_url = reverse_lazy('users')

	def form_valid(self, form):
		form.instance.is_superuser = True
		form.save()

		return super(UserCreate, self).form_valid(form)


class UserUpdate(AdminTemplateFilesMixin, LoginRequiredMixin, \
FormFieldCSSMixin, UpdateView):
	model = User
	form_class = UserUpdateForm
	template_name = 'user_form.html'
	success_url = reverse_lazy('users')

	def get_object(self):
		self.kwargs[self.pk_url_kwarg] = self.request.user.pk
		return super(UserUpdate, self).get_object()


class EntryList(AdminTemplateFilesMixin, LoginRequiredMixin, ListView):
	queryset = Entry.objects.select_related()
	context_object_name = 'entries'
	paginate_by = 10

	def get_queryset(self):
		_user = self.request.GET.get('user', None)
		queryset = super(EntryList, self).get_queryset()
		if not _user:
			return queryset

		if not User.objects.filter(username=_user).exists():
			return queryset

		return queryset.filter(author__username=_user)


class EntryCreate(AdminTemplateFilesMixin, LoginRequiredMixin, \
FormFieldCSSMixin, EntrySaveMixin, FormView):
	form_class = EntryForm
	template_name = 'entry_form.html'
	success_url = reverse_lazy('entries')


class EntryUpdate(AdminTemplateFilesMixin, LoginRequiredMixin, \
FormFieldCSSMixin, EntrySaveMixin, UpdateView):
	model = Entry
	form_class = EntryForm
	template_name = 'entry_form.html'
	success_url = reverse_lazy('entries')

	def get_form_kwargs(self):
		kwargs = super(EntryUpdate, self).get_form_kwargs()
		kwargs.update({'markdown_required':False})
		return kwargs


class EntryDelete(AdminTemplateFilesMixin, LoginRequiredMixin, \
DeleteView):
	model = Entry
	template_name = 'delete_confirm.html'
	success_url = reverse_lazy('entries')

	def delete(self, request, *args, **kwargs):
		obj = self.get_object()
		content = Content.objects.get(pk=obj.content)
		content.markdown.delete()
		content.html.delete()
		content.delete()
		return super(EntryDelete, self).delete(request, *args, **kwargs)


class EntryDetail(AdminTemplateFilesMixin, LoginRequiredMixin, DetailView):
	queryset = Entry.objects.select_related('author').prefetch_related('tags')
	context_object_name = 'entry'


class SetBlog(AdminTemplateFilesMixin, LoginRequiredMixin, FormFieldCSSMixin, \
FormView):
	form_class = SettingsForm
	prefix = 'blog'
	template_name = 'settings_form.html'
	success_url = reverse_lazy('settings')

	def get_initial(self):
		setobj = Settings.objects.first()
		if not setobj:
			return {}
		_init = {'name': setobj.name}
		
		htmlmeta = json_loads(setobj.html.to_json())
		_init.update(htmlmeta)
		_init.update({'keywords': ', '.join(htmlmeta.pop('keywords'))})
		return _init

	def form_valid(self, form):
		setobj = Settings.objects.first()
		if not setobj:
			setobj = Settings()
		setobj.name = form.cleaned_data['name']
		setobj.html = HTMLMeta(**form.cleaned_data)
		setobj.save()
		cache.delete('howto_settings')
		return super(SetBlog, self).form_valid(form)