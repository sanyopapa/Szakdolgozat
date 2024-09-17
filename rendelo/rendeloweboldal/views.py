from django.shortcuts import render

def kezdooldal(request):
    return render(request, 'kezdooldal.html')

def idopontfoglalas(request):
    return render(request, 'idopontfoglalas.html')

def admin_view(request):
    return render(request, 'admin.html')