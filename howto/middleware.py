from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseRedirect

from blog.utils import get_settings

class ViewNameMiddleware(object):
	def process_view(self, request, v_func, v_args, v_kwargs):
		url_name = resolve(request.path).url_name
		request.url_name = url_name

class ForceSetBlogMiddleware(object):
	def process_request(self, request):
		if get_settings():
			return None

		url_name = resolve(request.path).url_name
		if url_name in ['login', 'logout', 'settings']:
			return None

		return HttpResponseRedirect(reverse('settings'))