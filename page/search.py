# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response,render


# 表单
def search_form(request):
    ctx = {}
    if request.POST:
        ctx['rlt'] = request.POST['q']
    return render(request, "search_form.html", ctx)

def js(request):
    return  render_to_response('../static/js/../templates/pk.js')

# 接收请求数据
def search(request):
    request.encoding = 'utf-8'
    message = request.GET
    Title = {}
    Keyword = {}
    Author = {}

    return message
