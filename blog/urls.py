from . import views
from django.urls import path


# Note: the code has been used from the CI tutorial
# I Think Therefore I Blog
# to help the setup and creation of this project.


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('add/', views.add_post, name='add_post'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('<slug:slug>/delete/', views.delete_post, name='delete_post'),
]
