from django.contrib import admin
from .models import Cat
from .models import CatTest
from .models import User



# Register your models here.
admin.site.register(User)
admin.site.register(Cat)
admin.site.register(CatTest) #CatTest is temporary only for demonstration purposes.