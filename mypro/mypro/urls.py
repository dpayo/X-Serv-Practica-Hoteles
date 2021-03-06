"""mypro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from myapp import views



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.main),
    url(r'^more$',views.more),
    url(r'^about$',views.about),
    url(r'^(.*)/moreuser$',views.moreuser),
    url(r'^alojamientos/(\d+)$',views.show_aloj_id),
    url(r'^alojamientos/(\d+)/xmlingles$',views.show_aloj_id_ingles),
    url(r'^alojamientos/(\d+)/xmlfrances$',views.show_aloj_id_frances),
    url(r'^alojamientos$',views.show_aloj),
    url(r'^login', 'django.contrib.auth.views.login'),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^(.*)/xml$',views.show_userxml),
    url(r'^(.*)/(\d+)$', views.add_hotels),
    url(r'^(.*)$',views.show_hotels),


]
