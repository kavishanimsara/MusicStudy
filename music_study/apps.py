from django.apps import AppConfig


class MusicStudyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'music_study'
def ready(self):
    import music_study.signals