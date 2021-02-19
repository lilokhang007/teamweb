from jinja2.exceptions import TemplateSyntaxError
from staticjinja import Site
from distutils.dir_util import copy_tree
from path import static, src, docs

if __name__ == "__main__":
	copy_tree(static, docs)
	site = Site.make_site(
		searchpath = src,
		outpath = docs
	)
	try:
		site.render()
	except TemplateSyntaxError as error:
		print('Template syntax error:', error.filename, 'line', error.lineno)
		print(error.message)