from django.shortcuts import render
# Create your views here.

# 'Request' on views näkymä funktioiden ensimmäinen parametri minkä ottavat vastaan
def landingview(request):
    return render(request, 'landingpage.html')

def productlistview(request):
    return render(request, 'productlist.html')

def supplierlistview(request):
    return render(request, 'supplierlist.html')