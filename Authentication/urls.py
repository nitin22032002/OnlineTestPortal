from .views import Login,SignUp,Logout
from django.urls import path
urlpatterns=[
    path("login/",Login.as_view()),
    path("auth/login",Login.as_view()),
    path("signup/",SignUp.as_view()),
    path("auth/signup",SignUp.as_view()),
    path("logout/",Logout.as_view()),
]