from bson.objectid import ObjectId

from django.db.models import Field, SubfieldBase
from django.core.exceptions import ValidationError

class ObjectIdField(Field):
	__metaclass__ = SubfieldBase

	description = "bson-document objectid field"

	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = self._length = 24
		super(ObjectIdField, self).__init__(*args, **kwargs)

	def db_type(self, connection):
		_vendor = connection.settings_dict['ENGINE'].split('.')[-1]
		
		return "varchar" if _vendor == 'sqlite3' else "varchar(%d)" % \
		self._length

	def to_python(self, value):
		if isinstance(value, ObjectId):
			return value

		if not ObjectId.is_valid(value):
			raise ValidationError('invalid object id')

		return ObjectId(value) 

	def get_prep_value(self, value):
		return str(value)

	# https://docs.djangoproject.com/en/1.6/howto/custom-model-fields/#specifying-the-form-field-for-a-model-field
	# https://github.com/django/django/blob/master/django/db/models/fields/__init__.py#L88

try:
	from south.modelsinspector import add_introspection_rules
except:
	pass
else:
	add_introspection_rules([], ['^blog\.fields\.ObjectIdField'])