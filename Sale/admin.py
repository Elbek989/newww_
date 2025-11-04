from django.contrib import admin
from Sale.models import *
from user.models import *
from products.models import *

admin.site.register([
    Sale,

    SaleItem,

])
