from django.contrib import admin

# Register your models here.
from people.models import Person

admin.site.register(Person)