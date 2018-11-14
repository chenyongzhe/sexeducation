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
    path('index/',views.index1),
    path('',views.index),
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
    path('zhifu/',views.zhifu),
    path('gettip/',views.gettip),


    #url(r'^favicon.ico$',RedirectView.as_view(url=r'/static/favicon.ico')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


