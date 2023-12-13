from django.apps import AppConfig


# Note: the code has been used from the CI tutorial
# I Think Therefore I Blog
# to help the setup and creation of this project.


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
