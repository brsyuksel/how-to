from django.core.cache import cache
from json import loads as json_loads

from .collections import Settings

def get_settings():
	_set = cache.get('howto_settings')
	if not _set:
		setobj = Settings.objects.first()
		if not setobj:
			return {}
		_set = json_loads(setobj.to_json())
		_set['html'].update({'keywords': ', '.join(k.strip() \
		for k in _set['html'].pop('keywords'))})
		_set.pop('_id')
		cache.set('howto_settings', _set, 3600)
	return _set