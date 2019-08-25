from django.conf.urls import include, url, static
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^games/', include('games.urls', namespace="games"))
]
