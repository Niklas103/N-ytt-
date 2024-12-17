# Render = Renderöidään tietty html templates kansiosta
# Redirect = Ohjataan ohjelman suoritus johonkin toiseen view functioon
from django.shortcuts import render, redirect
from .models import Toimittaja, Tuote
from django.contrib.auth import authenticate, login, logout
# Create your views here.

# Loginpage
def loginview(request):
    return render (request, "loginpage.html")


# Login action
def login_action(request):
    user = request.POST['username']
    passw = request.POST['password']
    # Löytyykö kyseistä käyttäjää?
    user = authenticate(username = user, password = passw)
    #Jos löytyy:
    if user:
        # Kirjataan sisään
        login(request, user)
        # Tervehdystä varten context
        context = {'name': user.first_name}
        # Kutsutaan suoraan landingview.html
        return render(request,'paasivu.html',context)
    # Jos ei kyseistä käyttäjää löydy
    else:
        return render(request, 'loginerror.html')


# Logout action
def logout_action(request):
    logout(request)
    return render(request, 'loginpage.html')

# 'Request' on views näkymä funktioiden ensimmäinen parametri minkä ottavat vastaan
# def landingview(request):
#     return render(request, 'landingpage.html')

# Tuote views
def tuotelistaview(request):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        tuotelista = Tuote.objects.all()
        toimittajalista = Toimittaja.objects.all()
        context = {'tuotteet': tuotelista, 'toimittajat': toimittajalista}
        return render (request,"tuotelista.html",context)


def addproduct(request):
    a = request.POST['productname']
    b = request.POST['packagesize']
    c = request.POST['unitprice']
    d = request.POST['unitsinstock']
    e = request.POST['supplier']
    
    Tuote(productname = a, packagesize = b, unitprice = c, unitsinstock = d, supplier = Toimittaja.objects.get(id = e)).save()
    return redirect(request.META['HTTP_REFERER'])

def confirmdeleteproduct(request, id):
    product = Tuote.objects.get(id = id)
    context = {'product': product}
    return render (request,"confirmdelprod.html",context)


def deleteproduct(request, id):
    Tuote.objects.get(id = id).delete()
    return redirect(tuotelistaview)


def edit_product_get(request, id):
        product = Tuote.objects.get(id = id)
        context = {'product': product}
        return render (request,"edit_product.html",context)


def edit_product_post(request, id):
        item = Tuote.objects.get(id = id)
        item.kappalehinta = request.POST['unitprice']
        item.tuotteitavarastossa = request.POST['unitsinstock']
        item.save()
        return redirect(tuotelistaview)


def products_filtered(request, id):
    tuotelista = Tuote.objects.all()
    filteredproducts = tuotelista.filter(supplier = id)
    context = {'tuotteet': filteredproducts}
    return render (request,"tuotelista.html",context)



# Supplier views
def toimittajalistaview(request):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        toimittajalista = Toimittaja.objects.all()
        context = {'toimittajat': toimittajalista}
        return render (request,"toimittajalista.html",context)


def addsupplier(request):
    a = request.POST['companyname']
    b = request.POST['contactname']
    c = request.POST['address']
    d = request.POST['phone']
    e = request.POST['email']
    f = request.POST['country']
    Toimittaja(companyname = a, contactname = b, address = c, phone = d, email = e, country = f).save()
    return redirect(request.META['HTTP_REFERER'])


def searchsuppliers(request):
    search = request.POST['search']
    filtered = Toimittaja.objects.filter(companyname__icontains=search)
    context = {'toimittajat': filtered}
    return render (request,"toimittajalista.html",context)