from django.contrib import admin
from common.models import Country, Address


class CountryAdmin(admin.ModelAdmin):
    pass

class AddressAdmin(admin.ModelAdmin):
    pass

admin.site.register(Address, AddressAdmin)
admin.site.register(Country, CountryAdmin)

  