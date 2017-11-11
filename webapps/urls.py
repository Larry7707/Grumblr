"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as views
import grumblr.views as views1
import grumblr.urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^grumblr/', include('grumblr.urls')),
    url(r'^$', views1.home),
    # url(r'^login$', views.login, {'template_name': 'grumblr/login_page.html'}, 
    #     name = "login"),
    # url(r'^grumblr/registration/', views1.registration),
    # url(r'^login$', views.login, {'template_name': 'grumblr/login_page.html'
    #     }, name = "login"),
    # url(r'^logout$', views.logout_then_login, name = "logout"),
    # url(r'^register$', views1.registration, name = 'registration'),
    # # show global
    # url(r'^global', views1.home, name = 'global'),
    # url(r'^post', views1.post1, name = 'post'),
    # url(r'^profile/(?P<id>\d+)$', views1.profile1, name = "profile"),
    # url(r'^my_profile', views1.my_profile, name = "my_profile"),
    # url(r'^edit_profile', views1.edit_profile, name = "edit_profile"),
    # url(r'^my_following', views1.following_stream, name = "my_following"),
    # url(r'^email_sent', views1.send_change_email, name="send_email"),
    # url(r'^confirmation_email', views1.send_confirm_email, name="resend_email"),
    # url(r'^change_password/(?P<username>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
    #         views1.change_password, name='change_password'),
    # url(r'^confirmation/(?P<id>\d+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #          views1.confirm_registration, name='confirmation'),
    # url(r'^follow/(?P<id>\d+)$', views1.do_follow, name = "follow"),
    # url(r'^unfollow/(?P<id>\d+)$', views1.do_follow, name = "unfollow"),
    # # url(r'^search', views1.do_search, name = "search"),
    # url(r'^delete/(?P<id>\d+)$', views1.delete_post, name = "delete_post"),
    # url(r'^add_comment/(?P<id>\d+)$', views1.add_comment, name = "comment"),
    # url(r'^show_comment/(?P<id>\d+)$', views1.show_comment, name = "show_comment"),
    # url(r'^get_posts/?$', views1.get_posts),
    # url(r'^get_posts/(?P<time>.+)$', views1.get_posts),
    # url(r'^get_changes/?$', views1.get_changes),
    # url(r'^get_changes/(?P<time>.+)$', views1.get_changes),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)