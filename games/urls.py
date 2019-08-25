from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from games import views

app_name="games"

urlpatterns = [
    url('authtoken/', views.AuthToken.as_view(), name='gettoken'),
    url('upload/', views.upload, name='upload'),
    url('search/', views.search, name='search')
]
