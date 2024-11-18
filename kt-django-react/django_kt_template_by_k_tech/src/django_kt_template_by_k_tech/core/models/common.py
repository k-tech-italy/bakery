from django.db import models
from django.db.models.base import ModelBase
from django.contrib.auth.models import AbstractUser


class AuditableModelBase(ModelBase):
    def __new__(mcs, name, bases, attrs, **kwargs):
        if name != "Auditable":
            class MetaB:
                db_table = name

            attrs["Meta"] = MetaB

        r = super().__new__(mcs, name, bases, attrs, **kwargs)
        return r


class Auditable(models.Model, metaclass=AuditableModelBase):
    updated_by = models.CharField(max_length=50)
    update_ts = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class User(AbstractUser):
    email = models.EmailField(unique=True)
    

    def __str__(self):
        return self.username
