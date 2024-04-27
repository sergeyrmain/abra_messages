from django.apps import AppConfig


class MessagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messages'
    label = 'user_messages'  # A unique label to avoid conflicts with Django's built-in messages
    verbose_name = 'User Messages'
