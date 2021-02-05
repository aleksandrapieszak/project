from django.contrib import admin

# Register your models here.
from project.models import Client, Contract, Case, CashRegister, ContactPerson, Debtor,LeadingPerson

admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Case)
admin.site.register(CashRegister)
admin.site.register(ContactPerson)
admin.site.register(Debtor)
admin.site.register(LeadingPerson)