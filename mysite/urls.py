"""

/***************************************************************************************
*  REFERENCES
*  Title: In 5 mins: Set up Google login to sign up users on Django
*  Author: Zoe Chew
*  Date: 7/27/19
*  Code version: n/a
*  URL: https://medium.com/@whizzoe/in-5-mins-set-up-google-login-to-sign-up-users-on-django-e71d5c38f5d5
*  Software License: Not released under license, part of tutorial
*
***************************************************************************************/
"""

"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView # <--

from microdollars import views
from django.conf import settings # new
from django.urls import path, include # new
from django.conf.urls.static import static # new
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('lookup', views.lookup , name='lookup'),
    path('about', views.about, name='about'),
    path('leaderboard/', views.gamify, name='leaderboard'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)