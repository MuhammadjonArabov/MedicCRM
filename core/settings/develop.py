from .base import *  # noqa

DEBUG = True
CELERY_TASK_ALWAYS_EAGER = True


MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")


INTERNAL_IPS = [
    "127.0.0.1",
    '192.168.1.21',
    '192.168.1.42'

]

