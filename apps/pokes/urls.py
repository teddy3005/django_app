from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.success),
    url(r'^index2$', views.new),
    url(r'^poke_process$', views.poke_process, name="poke_process"),
    url(r'^logout$', views.logout),
]