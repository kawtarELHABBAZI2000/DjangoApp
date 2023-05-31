
from django.contrib import admin
from django.urls import path
from HawkViewApp import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include
from mozilla_django_oidc.views import OIDCAuthenticationRequestView, OIDCLogoutView



urlpatterns = [
    path('login', views.login, name='login'),
    path('oidc/', include('mozilla_django_oidc.urls')),
    # path('oidc/authenticate/', OIDCAuthenticationRequestView.as_view(), name='oidc_authentication_init'),
    # path('oidc/logout/', OIDCLogoutView.as_view(), name='oidc_logout'),

]
