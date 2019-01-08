from django.conf.urls import url

from . import views

from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^newsfeed/$', views.newsfeed, name='newsfeed'),
    url(r'^newsfeed/new_post/$', views.new_post, name='new_post'),
    url(r'^search/$', views.search, name='search'),
    url(r'^profiles/(?P<pk>[0-9]+)/$', views.profile, name='profile'),
    url(r'^profiles/(?P<pk>[0-9]+)/follow/$', views.follow_profile, name='follow'),
    url(r'^profiles/(?P<pk>[0-9]+)/unfollow/$', views.unfollow_profile, name='unfollow'),
    url(r'^profiles/(?P<pk>[0-9]+)/followers/$', views.show_followers, name='followers'),
    url(r'^profiles/(?P<pk>[0-9]+)/following/$', views.show_following, name='following'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^$', views.index, name='index'),
]
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^$', views.index, name='index'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

