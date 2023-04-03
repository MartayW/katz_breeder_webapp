from django.contrib import admin
from .models import Breeder
from .models import Customer
from .models import Cat
from .models import CatTest
from .models import Transaction
# Register your models here.
admin.site.register(Breeder)
admin.site.register(Customer)
admin.site.register(Cat)
admin.site.register(CatTest) #CatTest is temporary only for demonstration purposes.
admin.site.register(Transaction)