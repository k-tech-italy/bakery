from functools import partial

from django.utils.functional import SimpleLazyObject, cached_property

from {{cookiecutter.project__slug}}.config.environ import env
from {{cookiecutter.project__slug}}.state import State
from {{cookiecutter.project__slug}}.utils.locking.backends.redis import RedisLockBackend
from {{cookiecutter.project__slug}}.utils.locking.manager import LockManager
from {{cookiecutter.project__slug}}.utils.redis import SmartRedis


class Logger:
    def __init__(self, system):
        from {{cookiecutter.project__slug}}.models import SysLogEntry
        self.info = partial(SysLogEntry.info, system.organization)


class System:
    def __init__(self):
        pass

    @cached_property
    def logger(self):
        return Logger(self)


core = SimpleLazyObject(System)
locks = LockManager(RedisLockBackend(SmartRedis.from_url(env('REDIS_LOCK_URL'))))
# stop = sys.stop
# stopped = sys.stopped
# running = sys.running
# restart = sys.restart
state = State()
