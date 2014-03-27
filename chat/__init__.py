# __init__.py is the top level file in a Python package.

from apps import ChatApp

def make():
	app = apps.ChatApp('./chat/html')
	return app

