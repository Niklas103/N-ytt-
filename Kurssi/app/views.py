# Render = Renderöidään tietty html templates kansiosta
# Redirect = Ohjataan ohjelman suoritus johonkin toiseen view functioon
from django.shortcuts import render, redirect # Näkymien käsittelyyn
from .models import Toimittaja, Tuote, Varasto # Mallit tietokantakyselyihin
from django.contrib.auth import authenticate, login, logout # Käyttäjäautentikointi
# Create your views here.

# Login-sivun näkymä
def loginview(request):
    return render (request, "loginpage.html") # Näyttää kirjautumissivun HTML-mallin


# Kirjautumisprosessi
def login_action(request):
    if request.method == "POST": # Tarkistaa, onko pyyntö POST-tyyppiä
        username = request.POST['username'] # Hakee käyttäjänimen syötteestä
        password = request.POST['password'] # Hakee salasanan syötteestä
        user = authenticate(username=username, password=password) # Tarkistaa, vastaako käyttäjänimi ja salasana tietoja

        if user is not None: # Jos käyttäjä on olemassa
            login(request, user) # Kirjaa käyttäjän sisään
            return render(request,'index.html') # Vie käyttäjä etusivulle
        else:
            return render(request, 'loginerror.html')  # Jos kirjautuminen epäonnistuu, vie virhesivulle
    else:
        return render(request, 'loginpage.html') # Näyttää kirjautumissivun, jos pyyntö ei ole POST



# Kirjautumisen uloskirjautuminen
def logout_action(request):
    logout(request) # Kirjaa käyttäjän ulos
    return redirect('loginpage')  # Ohjaa käyttäjän takaisin kirjautumissivulle

# 'Request' on views näkymä funktioiden ensimmäinen parametri minkä ottavat vastaan

# Tuote views
def tuotelistaview(request):
    if not request.user.is_authenticated: # Tarkistaa, onko käyttäjä kirjautunut sisään
        return render(request, 'loginpage.html') # Vie kirjautumissivulle, jos käyttäjä ei ole kirjautunut
    else:
        tuotelista = Tuote.objects.all() # Hakee kaikki Tuote-taulun tiedot tietokannasta
        toimittajalista = Toimittaja.objects.all() # Hakee kaikki Toimittaja-taulun tiedot
        context = {'tuotteet': tuotelista, 'toimittajat': toimittajalista} # Lisää tiedot kontekstiin
        return render (request,"tuotelista.html",context) # Näyttää tuotelistausmallin


def lisäätuote(request):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html') # Vie kirjautumissivulle, jos käyttäjä ei ole kirjautunut
    else:
        a = request.POST['tuotenimi'] # Hakee tuotteen nimen lomakesyötteestä
        b = request.POST['painoperkappale'] # Hakee tuotteen painon syötteestä
        c = request.POST['kappalehinta'].replace(',', '.')  # Muunna pilkku pisteeksi
        d = request.POST['tuotteitavarastossa'] # Hakee kappalemäärän syötteestä
        e = request.POST['toimittaja'] # Hakee toimittajan id:n syötteestä
    
        # Luo uuden Tuote-objektin ja tallentaa sen tietokantaan
        Tuote(tuotenimi = a, painoperkappale = b, kappalehinta = c, tuotteitavarastossa = d, toimittaja = Toimittaja.objects.get(id = e)).save() # Hakee toimittajan id:n perusteella
        return redirect(request.META['HTTP_REFERER']) # Ohjaa käyttäjän takaisin edelliselle sivulle

def vahvistatuotepoisto(request, id):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        tuote = Tuote.objects.get(id = id) # Hakee tuotteen id:n perusteella
        context = {'tuote': tuote}  # Lisää tuotteen tiedot kontekstiin
        return render (request,"tuotepoisto.html",context) # Näyttää poiston vahvistusmallin


def tuotepoisto(request, id):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        Tuote.objects.get(id = id).delete() # Poistaa tuotteen id:n perusteella
        return redirect(tuotelistaview) # Ohjaa käyttäjän takaisin tuotelistaan


def edit_tuote_get(request, id):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        tuote = Tuote.objects.get(id = id) # Hakee muokattavan tuotteen
        context = {'tuote': tuote} # Lisää tiedot kontekstiin
        return render (request,"edit_tuote.html",context) # Näyttää tuotteen muokkauslomakkeen


def edit_tuote_post(request, id):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        item = Tuote.objects.get(id = id) # Hakee tuotteen id:n perusteella
        item.kappalehinta = request.POST['kappalehinta']
        item.tuotteitavarastossa = request.POST['tuotteitavarastossa']
        item.save() # Tallentaa muutokset tietokantaan
        return redirect(tuotelistaview) # Ohjaa takaisin tuotelistaukseen

def tuotteet_filtered(request, id):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        filteredtuotteet = Tuote.objects.filter(toimittaja_id=id)
        context = {'tuotteet': filteredtuotteet}
        return render(request, "tuotelista.html", context)

def etsi_tuote(request):
    if not request.user.is_authenticated:
        return render(request, 'loginpage.html')
    else:
        search = request.POST.get('search', '')  # Hae hakutermi POST-data
        filtered = Tuote.objects.filter(tuotenimi__icontains=search)  # Suodata tuotteet
        context = {'tuotteet': filtered}  # Lisää suodatetut tuotteet kontekstiin
        return render(request, "tuotelista.html", context)


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


# Varasto views
def varastolistaview(request):
    varastot = Varasto.objects.all()
    return render(request, 'varastolista.html', {'varastot': varastot})