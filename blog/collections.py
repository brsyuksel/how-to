from datetime import datetime

from mongoengine import document, fields

class Content(document.Document):
	html = fields.FileField(required=True)
	markdown = fields.FileField(required=True)
	plain = fields.StringField(required=True)
	keywords = fields.ListField(fields.StringField())
	toc = fields.ListField()
	created_at = fields.DateTimeField(default=datetime.now)

	meta = {
		'ordering': ['-created_at'],
		'indexes': ['keywords'],
		'auto_create_index': False
	}

class HTMLMeta(document.EmbeddedDocument):
	title = fields.StringField(required=True)
	description = fields.StringField(required=True)
	keywords = fields.ListField(fields.StringField(unique=True))
	author = fields.StringField(required=True)

class Settings(document.Document):
	name = fields.StringField(required=True)
	html = fields.EmbeddedDocumentField(HTMLMeta, required=True)