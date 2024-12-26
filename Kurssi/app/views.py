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
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request,'index.html')
        else:
            return render(request, 'loginerror.html')  # Jos kirjautuminen epäonnistuu, vie virhesivulle
    else:
        return render(request, 'loginpage.html')



# Logout action
def logout_action(request):
    logout(request)
    return redirect('loginpage')  # redirect to login page after logout

# 'Request' on views näkymä funktioiden ensimmäinen parametri minkä ottavat vastaan

# Tuote views
def tuotelistaview(request):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        tuotelista = Tuote.objects.all()
        toimittajalista = Toimittaja.objects.all()
        context = {'tuotteet': tuotelista, 'toimittajat': toimittajalista}
        return render (request,"tuotelista.html",context)


def lisäätuote(request):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        a = request.POST['tuotenimi']
        b = request.POST['painoperkappale']
        c = request.POST['kappalehinta'].replace(',', '.')  # Muunna pilkku pisteeksi
        d = request.POST['tuotteitavarastossa']
        e = request.POST['toimittaja']
    
        Tuote(tuotenimi = a, painoperkappale = b, kappalehinta = c, tuotteitavarastossa = d, toimittaja = Toimittaja.objects.get(id = e)).save()
        return redirect(request.META['HTTP_REFERER'])

def vahvistatuotepoisto(request, id):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        tuote = Tuote.objects.get(id = id)
        context = {'tuote': tuote}
        return render (request,"tuotepoisto.html",context)


def tuotepoisto(request, id):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        Tuote.objects.get(id = id).delete()
        return redirect(tuotelistaview)


def edit_tuote_get(request, id):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        tuote = Tuote.objects.get(id = id)
        context = {'tuote': tuote}
        return render (request,"edit_tuote.html",context)


def edit_tuote_post(request, id):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        item = Tuote.objects.get(id = id)
        item.kappalehinta = request.POST['kappalehinta']
        item.tuotteitavarastossa = request.POST['tuotteitavarastossa']
        item.save()
        return redirect(tuotelistaview)


def tuotteet_filtered(request, id):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        tuotelista = Tuote.objects.all()
        filteredtuotteet = tuotelista.filter(toimittaja = id)
        context = {'tuotteet': tuotteet_filtered}
        return render (request,"tuotelista.html",context)



# Toimittaja views
def toimittajalistaview(request):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        toimittajalista = Toimittaja.objects.all()
        context = {'toimittajat': toimittajalista}
        return render (request,"toimittajalista.html",context)


def lisäätoimittaja(request):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        a = request.POST['yritysnimi']
        b = request.POST['yhteyshenkilö']
        c = request.POST['osoite']
        d = request.POST['puhelin']
        e = request.POST['sähköposti']
        f = request.POST['maa']
        Toimittaja(yritysnimi = a, yhteyshenkilö = b, osoite = c, puhelin = d, sähköposti = e, maa = f).save()
        return redirect(request.META['HTTP_REFERER'])


def etsitoimittaja(request):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        search = request.POST['search']
        filtered = Toimittaja.objects.filter(yritysnimi__icontains=search)
        context = {'toimittajat': filtered}
        return render (request,"toimittajalista.html",context)
    
def vahvistatoimittajapoisto(request, id):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        toimittaja = Toimittaja.objects.get(id = id)
        context = {'toimittaja': toimittaja}
        return render (request,"toimittajapoisto.html",context)


def toimittajapoisto(request, id):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        try:
            toimittaja = Toimittaja.objects.get(id=id)  # Hae toimittaja id:n mukaan
            toimittaja.delete()  # Poista toimittaja
            return redirect(toimittajalistaview)  # Ohjaa takaisin toimittajalistaan
        except Toimittaja.DoesNotExist:
            # Jos toimittajaa ei löydy, ohjataan virhesivulle tai näyttää viestin
            return render(request, 'error.html', {'message': 'Toimittajaa ei löytynyt!'})

def edit_toimittaja_post(request, id):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        item = Toimittaja.objects.get(id=id)
        item.yritysnimi = request.POST['yritysnimi']
        item.yhteyshenkilö = request.POST['yhteyshenkilö']
        item.osoite = request.POST['osoite']
        item.puhelin = request.POST['puhelin']
        item.sähköposti = request.POST['sähköposti']
        item.maa = request.POST['maa']
        item.save()
        return redirect(toimittajalistaview)  # Suora funktioviittaus
    
def edit_toimittaja_get(request, id):
        if not request.user.is_authenticated:
            return render(request, 'loginpage.html')
        try:
            toimittaja = Toimittaja.objects.get(id=id)  # Haetaan toimittajan tiedot ID:n perusteella
            return render(request, 'edit_toimittaja.html', {'toimittaja': toimittaja})  # Lähetetään tiedot lomakkeelle
        except Toimittaja.DoesNotExist:
            return render(request, 'error.html', {'message': 'Toimittajaa ei löytynyt!'})  # Jos toimittajaa ei löydy
