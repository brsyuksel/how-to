from django.core.urlresolvers import resolve

class ViewNameMiddleware(object):
	def process_view(self, request, v_func, v_args, v_kwargs):
		url_name = resolve(request.path).url_name
		request.url_name = url_name