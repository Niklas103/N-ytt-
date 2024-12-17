# Jos rekisteröi tällä tavalla adminille oman appin
# modelit, voi myös admin sivuilta muokata näitä tietoja.

from django.contrib import admin

from app.models import Toimittaja, Tuote

@admin.register(Tuote)
class TuoteAdmin(admin.ModelAdmin):
    pass

@admin.register(Toimittaja)
class ToimittajaAdmin(admin.ModelAdmin):
    pass