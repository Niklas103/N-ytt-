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

from .views import tuotelistaview, toimittajalistaview, products_filtered
from .views import addsupplier, addproduct, deleteproduct, confirmdeleteproduct
from .views import edit_product_post, edit_product_get, searchsuppliers
from .views import loginview, login_action, logout_action

# syntaksi: Mikä osoite polku: '' sovelluksen juuri: landingview (renderöidään landingview). App kansion sisältä, view tiedostosta importataan landingview
urlpatterns = [
    # path('', landingview),


  
    # Login & logout
    path('', loginview),
    path('login/', login_action),
    path('logout/', logout_action),

     # Products url´s
    path('tuotteet/', tuotelistaview),
    path('add-product/', addproduct),
    path('delete-product/<int:id>/', deleteproduct),
    path('confirm-delete-product/<int:id>/', confirmdeleteproduct),
    path('edit-product-get/<int:id>/', edit_product_get),
    path('edit-product-post/<int:id>/', edit_product_post),
    path('products-by-supplier/<int:id>/', products_filtered),

    # Supplier url´s
    path('toimittajat/', toimittajalistaview),
    path('add-supplier/', addsupplier),
    path('search-suppliers/', searchsuppliers),

]