from django.contrib import admin
from django.urls import path,include
from .views import homePage,about,profile
urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/',include('Authentication.urls')),
    path('register/',include('Institute.urls')),
    path("",homePage),
    path("profile/",profile),
    path("about/",about),
]
