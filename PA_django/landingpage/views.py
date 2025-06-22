from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def discord(request):
    return render(request, 'discord.html')

def socials(request):
    return render(request, 'socials.html')