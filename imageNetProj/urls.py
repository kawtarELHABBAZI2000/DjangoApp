"""imageNetProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from HawkViewApp import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include
from mozilla_django_oidc.views import OIDCAuthenticationRequestView, OIDCLogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='homepage'),
    path('firstHome', views.firstHome, name='firstHome'),
    path('uploadBrain', views.uploadBrain, name='uploadBrain'),
    path('uploadKnee', views.uploadKnee, name='uploadKnee'),
    path('uploadLung', views.uploadLung, name='uploadLung'),    
    path('uploadEye', views.uploadEye, name='uploadEye'),
    path('uploadBone', views.uploadBone, name='uploadBone'),
    path('predictImageBrain', views.predictImageBrain, name='predictImageBrain'),    
    path('predictImageKnee', views.predictImageKnee, name='predictImageKnee'),
    path('predictImageLung', views.predictImageLung, name='predictImageLung'),
    path('predictImageEye', views.predictImageEye, name='predictImageEye'),
    path('predictImageBone', views.predictImageBone, name='predictImageBone'),    
    path('predictImageRec', views.predictImageRec, name='predictImageRec'),
    path('helpPage', views.helpPage, name='helpPage'),
    path('firstHelpPage', views.firstHelpPage, name='firstHelpPage'),    
    path('modelRec', views.modelRec, name='modelRec'),
    path('login', views.login, name='login'),
    path('viewDataBase', views.viewDataBase, name='viewDataBase'),
    path('oidc/', include('mozilla_django_oidc.urls')),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
