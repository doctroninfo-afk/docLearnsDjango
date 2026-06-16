from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# request -> response
# request handler

def say_hello(request):
    #Pull data from DB
    #Transofmr Data
    #Send email 
    return HttpResponse('Hello World')