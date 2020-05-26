from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "klanten.utils"

    def ready(self):
        from . import checks  # noqa
