
class HtmlGenerator(object):
	wrapper = 'div'
	wrapper_attrs = {}
	list_tag = 'ul'
	list_tag_attrs = {}
	child_list_tag = 'ul'
	child_list_tag_attrs = {}
	li_attrs = {}
	item_wrapper = 'p'
	item_wrapper_attrs = {}
	item_attrs = {}

	@classmethod
	def html(cls, items):
		open_tag = lambda t,a: ("<%s>" % t) if not a else \
		"<{tag} {attrs}>".format(tag=t, attrs=' '.join([
			'='.join([k, repr(v)]) for k,v in a.items()
		]))
		close_tag = lambda t: "</%s>" % t
		wrap_text = lambda t,a,c: open_tag(t,a) + c + close_tag(t)

		yield open_tag(cls.wrapper, cls.wrapper_attrs) + \
		open_tag(cls.list_tag, cls.list_tag_attrs)

		current_level = 1
		for item in items:
			try:
				level, href, text = item[0], item[1], item[2]
			except:
				level, href, text = 1, item[0], item[1]
			_item_attrs = {'href': str(href)}
			_item_attrs.update(cls.item_attrs)

			if level > current_level:
				yield open_tag(cls.child_list_tag, cls.child_list_tag_attrs)

			if level < current_level:
				for i in range(current_level, level, -1):
					yield close_tag('li') + close_tag(cls.child_list_tag)
				current_level = level

			if items.index(item) and level == current_level:
				yield close_tag('li')

			current_level = level
			yield open_tag('li', cls.li_attrs) + \
			open_tag(cls.item_wrapper, cls.item_wrapper_attrs) + \
			wrap_text('a', _item_attrs, text) + close_tag(cls.item_wrapper)


		yield close_tag('li') + close_tag(cls.list_tag) + close_tag(cls.wrapper)


class TableOfContents(HtmlGenerator):
	wrapper = 'blockquote'
	wrapper_attrs = {'id':'index'}
	list_tag = child_list_tag = 'ul'
	list_tag_attrs = {'class':'list-unstyled'}
	item_wrapper = 'p'
	item_attrs = {'class':'text-danger'}

class References(TableOfContents):
	wrapper_attrs = {'id':'references'}
	item_attrs = {'class':'text-info'}