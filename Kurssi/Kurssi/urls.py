"""
URL configuration for Kurssi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

admin.site.site_header = 'Simon S-Rauta admin sivut'
admin.site.site_title = 'Toimittajat'
admin.site.index_title = 'Admin sivu'

urlpatterns = [
    path('admin/', admin.site.urls), # Päätasolta jos kirjoitetaan admin niin ohjaa adminiin
    path ('', include('app.urls')) # Path: '' <-- tarkoittaa että jos mennään sovelluksen juureen, niin etsitäänkin 'app' kansion urleista lisää tiedosto polkuja (Eli kun kirjoitetaan vaan sovelluksen osoite tämä etsii urlit tässä mitkä on esitelty "app.urls")
]
