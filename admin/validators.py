from django.core.exceptions import ValidationError

from blog.models import User

def validate_user_email_unique(value):
	try:
		User.objects.get(email=value)
	except:
		pass
	else:
		raise ValidationError('A user with that email already exists.')