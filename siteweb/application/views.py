from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .models import Server, Person, Message

# Create your views here.
def worm(request):
    return HttpResponse("Hello, world. You're at the worm index.")


@csrf_exempt 
def servers(request):
    if request.method == 'GET':
        server_list = Server.objects.order_by('name')
        return HttpResponse(server_list)
    else:
        return HttpResponse("KO")


@csrf_exempt 
def server(request):    
    if request.method == 'POST':
        name = request.POST.get('name')
        code =request.POST.get('code')

        serv = Server.objetcs.get(code=code)
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
        allpersons = Person.objects.order_by('username')
        persons = []
        for p in allpersons:
            persons.append(p)
            persons.append(' ')
        return HttpResponse(persons)        

    else:
        return HttpResponse("KO")

@csrf_exempt 
def person(request):   
    if request.method == 'POST':
        username = request.POST.get('username')
        code = request.POST.get('code')
        servername = request.POST.get('servername')

        
        try:
            server = Server.objects.get(name=servername)    
        except Server.DoesNotExist:
            server = None

        try:
            man = Person.objects.get(code=code)
        except Person.DoesNotExist:
            man = None

        if man:     # Update the name
            man.username = username
            man.server.add(server)
            man.save()
        else:       # Create a new Server
            man = Person(username=username, code=code)
            man.save()
            man.server.add(server)
            man.save()
        
        return HttpResponse("OK")
    else:
        return HttpResponse("KO")