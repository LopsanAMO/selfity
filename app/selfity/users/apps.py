# -*- coding: utf-8 -*-
from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'selfity.users'

    def ready(self):
        import selfity.users.signals  # noqa: F401