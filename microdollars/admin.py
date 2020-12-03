from django.contrib import admin

# Register your models here.
#test
from .models import OrganizationModel as O
from .models import Donation as D
#import Organization Model into admin
admin.site.register(O)
admin.site.register(D)
