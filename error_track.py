import sentry_sdk
from sentry_sdk import configure_scope
import subprocess
import os

def create_sentry_task(dsn, email = 'anonimous', version = 'unofficial'):
	sentry_sdk.init(dsn, release =  version)
	with configure_scope() as scope:
		scope.user = { "email": email }


if __name__ == '__main__':
	print(_version)
