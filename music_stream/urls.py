from django.conf.urls import patterns, url
from music_stream import views

urlpatterns = patterns('music_stream.views',	
        url(r'^$', views.index, name='index'),
)
