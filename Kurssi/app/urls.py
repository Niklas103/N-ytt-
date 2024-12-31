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
from django.urls import path

from .views import tuotelistaview, toimittajalistaview, tuotteet_filtered
from .views import lisäätoimittaja, lisäätuote, tuotepoisto, vahvistatuotepoisto
from .views import edit_tuote_get, edit_tuote_post, etsitoimittaja, etsi_tuote
from .views import loginview, login_action, logout_action
from .views import toimittajapoisto, vahvistatoimittajapoisto, edit_toimittaja_post, edit_toimittaja_get
from .views import varastolistaview

# syntaksi: Mikä osoite polku: '' sovelluksen juuri: landingview (renderöidään landingview). App kansion sisältä, view tiedostosta importataan landingview
urlpatterns = [
  
    # Login & logout
    # Annetaan nimi ("name") näkymille joihin voi viitata helposti.
    path('', loginview, name='loginpage'),  # Kirjautumissivu
    path('login/', login_action, name='login_action'),  # Kirjautumistoiminto
    path('logout/', logout_action, name='logout_action'),  # Uloskirjautumistoiminto

     # Tuote url´s
    path('tuotteet/', tuotelistaview),
    path('lisää-tuote/', lisäätuote),
    path('poista-tuote/<int:id>/', tuotepoisto),
    path('vahvista-tuote-poisto/<int:id>/', vahvistatuotepoisto),
    path('edit-tuote-get/<int:id>/', edit_tuote_get),
    path('edit-tuote-post/<int:id>/', edit_tuote_post),
    path('tuote-toimittajan-mukaan/<int:id>/', tuotteet_filtered, name='tuotteet_filtered'),
    path('etsi-tuote/', etsi_tuote, name='etsi_tuote'),

    # Toimittaja url´s
    path('toimittajat/', toimittajalistaview),
    path('lisää-toimittaja/', lisäätoimittaja),
    path('etsi-toimittaja/', etsitoimittaja),
    path('poista-toimittaja/<int:id>/', toimittajapoisto),
    path('vahvista-toimittaja-poisto/<int:id>/', vahvistatoimittajapoisto),
    path('edit-toimittaja-post/<int:id>/', edit_toimittaja_post, name='edit_toimittaja_post'),
    path('edit-toimittaja-get/<int:id>/', edit_toimittaja_get, name='edit_toimittaja_get'),

    # Varasto url's
    path('varasto/', varastolistaview, name='varasto'),

]