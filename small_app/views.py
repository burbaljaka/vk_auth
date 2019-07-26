from django.shortcuts import render

def index(request):
    return render(request, 'small_app/index.html')
