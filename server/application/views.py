from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers

from .models import Server, Person, Message

import base64
from ast import literal_eval
import json

# Create your views here.
def worm(request):
    return HttpResponse("Hello, world. You're at the worm index.")


@csrf_exempt 
def servers(request):
    if request.method == 'GET':
        data = serializers.serialize('json', Server.objects.all(), fields=('name','code'))
        return HttpResponse(data)
    else:
        return HttpResponse("KO")


@csrf_exempt 
def server(request):    
    if request.method == 'POST':
        name = request.POST.get('name')
        code =request.POST.get('code')

        try:
            serv = Server.objects.get(code=code)
        except Server.DoesNotExist:
            serv = None

        if serv:    # Update the name
            serv.name = name
            serv.save()
        else:       # Create a new Server
            serv = Server(name=name, code=code)
            serv.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("KO")

#############################

@csrf_exempt 
def persons(request):
    if request.method == 'GET':
        data = serializers.serialize('json', Person.objects.all(), fields=('username', 'code', 'server'))
        return HttpResponse(data)        

    else:
        return HttpResponse("KO")

@csrf_exempt 
def person(request):   
    if request.method == 'POST':
        base64_message = request.POST.get('encoded')
        base64_bytes = base64_message.encode('utf-8')
        message_bytes = base64.b64decode(base64_bytes)
        data = message_bytes.decode('utf-8')
        members = json.loads(data.replace("'", "\"").replace("\\\"", "'").replace("\\", ""))        
        members = members["members"]

        for member in members:
            print(member)
            if member != {}:
                username = member['username']
                code = member['id']
                servername = member['server']

                try:
                    server = Server.objects.get(name=servername)    
                except Server.DoesNotExist:
                    server = None
                    return HttpResponse("KO")

                try:
                    man = Person.objects.get(code=code)
                except Person.DoesNotExist:
                    man = None

                if man:     # Update the name
                    man.username = username
                    man.server.add(server)
                    man.save()
                else:       # Create a new Person
                    man = Person(username=username, code=code)
                    man.save()
                    man.server.add(server)
                    man.save()        
        return HttpResponse("OK")
    return HttpResponse("KO")