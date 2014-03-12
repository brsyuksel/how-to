from django.contrib.auth.forms import UserCreationForm as authUserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from blog.models import *
from .validators import *

class UserCreationForm(authUserCreationForm):
	class Meta(authUserCreationForm.Meta):
		fields = ['username', 'email', 'first_name', 'last_name']

	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['email'].validators.append(validate_user_email_unique)

class UserUpdateForm(forms.ModelForm):
	password1 = forms.CharField(label='New Password', required=False,
	widget=forms.PasswordInput)
	password2 = forms.CharField(label='New Password Again', required=False,
	widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['first_name', 'last_name']

	def clean_password2(self):
		pass1 = self.cleaned_data.get('password1')
		pass2 = self.cleaned_data.get('password2')

		if pass1 != pass2:
			raise ValidationError('Passwords didn\'t match')

		return pass2

	def save(self): 
		password = self.cleaned_data.get('password1')
		user = super(UserUpdateForm, self).save(commit=False)
		password and user.set_password(password)
		user.save()
		return user

class EntryForm(forms.ModelForm):
	markdown = forms.FileField()

	class Meta:
		model = Entry
		fields = ['kind', 'publish']

	def __init__(self, markdown_required=True, *args, **kwargs):
		super(EntryForm, self).__init__(*args, **kwargs)
		self.fields['markdown'].required = markdown_required
		self.fields.keyOrder = ['kind', 'markdown', 'publish']

	def clean_markdown(self):
		mdfile = self.cleaned_data.get('markdown')

		if mdfile:
			if mdfile.content_type not in ['text/x-markdown']:
				raise ValidationError('invalid file format')
		return mdfile

class SettingsForm(forms.Form):
	name = forms.CharField(label='Blog name', required=True)
	title = forms.CharField(label='Blog title', required=True)
	description = forms.CharField(label='Blog description', required=True, 
	widget=forms.Textarea(attrs={'rows':4}))
	keywords = forms.CharField(label='Blog keywords', required=True, 
	widget=forms.Textarea(attrs={'rows':4}))
	author = forms.CharField(label='Blog authors', required=True)

	def clean_keywords(self):
		_keywords = self.cleaned_data.get('keywords')

		return set(k.strip() for k in _keywords.split(','))