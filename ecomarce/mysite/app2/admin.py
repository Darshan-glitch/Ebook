
from django.contrib import admin
from .models import Videos
# Register your models here.
from .models import *
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Videos)
admin.site.register(Payment)
