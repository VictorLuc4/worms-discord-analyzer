from django.contrib import admin
from .models import Server, Person, Message

# Register your models here.

admin.site.register(Server)
admin.site.register(Person)
admin.site.register(Message)