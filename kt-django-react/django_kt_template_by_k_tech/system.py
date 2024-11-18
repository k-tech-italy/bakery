from functools import partial

from django.utils.functional import SimpleLazyObject, cached_property

from django_kt_template_by_k_tech.config.environ import env
from django_kt_template_by_k_tech.state import State
from django_kt_template_by_k_tech.utils.locking.backends.redis import RedisLockBackend
from django_kt_template_by_k_tech.utils.locking.manager import LockManager
from django_kt_template_by_k_tech.utils.redis import SmartRedis


class Logger:
    def __init__(self, system):
        from django_kt_template_by_k_tech.models import SysLogEntry
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
