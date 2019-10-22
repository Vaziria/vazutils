import sentry_sdk
from sentry_sdk import configure_scope
import subprocess
import os

from .builder import get_version

_version = get_version()

def create_sentry_task(dsn, email = 'anonimous'):
	sentry_sdk.init(dsn, release =  _version)
	with configure_scope() as scope:
		scope.user = { "email": email }


if __name__ == '__main__':
	print(_version)
