"""sexeducation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from article import  views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('readarticle/',views.index),
    path('',views.homepage),
    path('s/',views.search),
    path('article/',views.article),
    path('video/',views.player),
    path('videoeducation/',views.videoeducation),
    path('login/',views.login),
    path('userinfor/',views.userinfor),
    path('sent_article/',views.sent_aritcle),
    path('insert_article/',views.insert_article),
    path('register/',views.register),
    url(r'(\d+).html',views.showhtml),
    path('twjx/',views.picedu),
    path('twjx/manbody/',views.manbody),
    path('twjx/womanbody/',views.womanbody),
    path('insert_comment/',views.insert_comment),
    path('user/',views.showuser),
    path('zhan/',views.zhan),
    path('gettip/',views.gettip),
    path('modify/',views.modify),
    path('exit/',views.exit_login),
path('sendmessage/',views.sendmessage),
    path('insert_message/',views.insert_message),
path('managerlogin/',views.managerlogin),
    path('manageruserinfor/',views.manageruserinfor),
    path('message/',views.message),
    path('sendto/',views.sendto),
    path('mymessage/',views.mymessage),
    path('usermessage/',views.usermessage),
    path('testedit/',views.testedit),
    path("upload_img/",views.upload_img),
    path("follow/",views.follow),
path("videolist/",views.video_list),
path("videoplay/",views.video_play),
path("insert_vcomment/",views.insert_vcomment),
path("insert_dm/",views.insert_dm),
path("insert_dm1/",views.insert_dm1),
path("get_dm/v3/",views.get_dm),
path("get_dm/",views.get_dm),
path("jz/",views.parent),
path("articletp/",views.articletp),
path("child/",views.child),
path("qsn/",views.qsn),
    #url(r'^favicon.ico$',RedirectView.as_view(url=r'/static/favicon.ico')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


