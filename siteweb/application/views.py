from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .models import Person, Server, Message

# Create your views here.
def worm(request):
    return HttpResponse("Hello, world. You're at the worm index.")


@csrf_exempt 
def servers(request):
    if request.method == 'GET':
        server_list = Server.objects.order_by('name')
        print(server_list[0])
        return HttpResponse(server_list)
    else:
        return HttpResponse("KO")


@csrf_exempt 
def server(request):    
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        code =request.POST.get('code')
        tmp_srv = Server(name=name, code=code)
        tmp_srv.save()
        return HttpResponse("Server %s saved in DB", name)
    else:
        return HttpResponse("KO")
        
