# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from backs.filter import *

# Create your views here.

@authenticated
def project(request):
	return HttpResponse("test")