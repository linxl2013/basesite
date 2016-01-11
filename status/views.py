# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from backs.filter import *


# 状态设置
@authenticated
def status(request, statustype):
    return render(request, 'status.html', {'page_id': 'status', 'statustype': statustype})


@authenticated
def list(request, statustype):
    ret = '''
   {"total":28,"rows":[
   {"id":"1","name":"Koi","code":"Large"},
   {"id":"2","name":"Dalmation","code":"Spotted Adult Female"},
   {"id":"3","name":"Rattlesnake","code":"Venomless"},
   {"id":"4","name":"Rattlesnake","code":"Rattleless"},
   {"id":"5","name":"Iguana","code":"Green Adult"},
   {"id":"6","name":"Manx","code":"Tailless"},
   {"id":"7","name":"Manx","code":"With tail"},
   {"id":"8","name":"Persian","code":"Adult Female"},
   {"id":"9","name":"Persian","code":"Adult Male"},
   {"id":"10","name":"Amazon Parrot","code":"Adult Male"}
   ]}
   '''
    return HttpResponse(ret, content_type='application/json')
