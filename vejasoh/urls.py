"""vejasoh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from vejasoh.api import api

from django.contrib.auth.decorators import login_required

from accounts.views import LoginView, LogoutView, RegisterUserView
from feeds.views import IndexView, FeedJsonView

urlpatterns = [
    url(r'^$', login_required(IndexView.as_view()), name='index'),
    url(r'^feeds/stream/(?P<pk>\d+)/feed/$', login_required(FeedJsonView.as_view()), name='stream-feed'),
    url(r'^accounts/login/$', LoginView.as_view(), name='user-login'),
    url(r'^accounts/logout/$', LogoutView.as_view(), name='user-logout'),
    url(r'^accounts/register/$', RegisterUserView.as_view(), name='user-register'),
    path('admin/', admin.site.urls),
    url(r'^api/', include(api.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
