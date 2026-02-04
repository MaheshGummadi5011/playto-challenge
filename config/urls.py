from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Quick function to show a welcome message on the home page
def home(request):
    return JsonResponse({
        "message": "Playto Challenge API is Live 🚀",
        "endpoints": {
            "feed": "/api/posts/",
            "leaderboard": "/api/leaderboard/",
            "admin": "/admin/"
        }
    })

urlpatterns = [
    path('', home),  # <--- This fixes the 404 error!
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
]