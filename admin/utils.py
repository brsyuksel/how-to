from django.conf import settings

def mongo_connect():
	from django.db.utils import DatabaseError
	from mongoengine import connect

	mongo_conf = {k.lower(): v for k,v in settings.MONGODB_DATABASE.items()}
	db_name = mongo_conf.pop('name', None)
	if not db_name:
		raise DatabaseError('set mongodb database name')
	mongo_conf.pop('conf', None)
	return connect(db_name, **mongo_conf)