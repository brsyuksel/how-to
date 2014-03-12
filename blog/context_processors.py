from .utils import get_settings

def howto_settings(request):
	_settings = get_settings()
	return {'blog': _settings}