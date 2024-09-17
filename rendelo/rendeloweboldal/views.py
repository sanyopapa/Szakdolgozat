from django.shortcuts import render

def kezdooldal(request):
    return render(request, 'kezdooldal.html')