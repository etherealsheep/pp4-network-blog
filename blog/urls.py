from django.urls import path
from . import views as blog_views

urlpatterns = [
    path(r'^$', blog_views.post_list, name="post-list"),
    path(r'^post-single/$', blog_views.post_single, name="post-single"),
    path(r'^contact-us/$', blog_views.contact_us, name="contact-us"),
]
