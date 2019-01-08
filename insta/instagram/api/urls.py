from django.conf.urls import url

from rest_framework.authtoken import views as auth_views

from instagram.api import views


urlpatterns = [
    url(r'^users/$', views.UserListAPIView.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetailAPIView.as_view(), name='user-detail'),
    url(r'^posts/$', views.PostListAPIView.as_view(), name='post-list'),
    url(r'^posts/(?P<pk>[0-9]+)/$', views.PostDetailAPIView.as_view(), name='post-detail'),
    url(r'^likes/$', views.LikeListAPIView.as_view(), name='like-list'),
    url(r'^likes/(?P<pk>[0-9]+)/$', views.LikeDetailAPIView.as_view(), name='like-detail'),
    url(r'^comments/$', views.CommentListAPIView.as_view(), name='comment-list'),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.CommentDetailAPIView.as_view(), name='comment-detail'),
    url(r'^signup/$', views.UserSignupAPIView.as_view(), name='user-signup'),
    url(r'^signup/available/$', views.UsernameEmailAvailableAPIView.as_view(), name='user-signup2'),
    url(r'^login/$', views.UserLoginAPIView.as_view(), name='user-login'),
    url(r'^logout/$', views.UserLogoutAPIView.as_view(), name='user-logout'),
    url(r'^newsfeed/$', views.NewsfeedListAPIView.as_view(), name='user-newsfeed'),
    url(r'^api-token-auth/', auth_views.obtain_auth_token),
]