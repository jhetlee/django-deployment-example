from django.conf.urls import url
from simple_app import views

app_name = 'simple_app'
urlpatterns = [
    url(r'^base/$', views.base, name='base'),
    url(r'^relative/$', views.relative, name='relative'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^user_login/$', views.user_login, name='user_login'),
]

