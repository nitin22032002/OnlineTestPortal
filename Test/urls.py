from django.urls import path
from .views import paper,viewPapers,deletePapers,userPaper
urlpatterns=[
    path('paper/',paper.as_view()),
    path('add/paper',paper.as_view()),
    path('view/papers/',viewPapers),
    path('delete/paper/',deletePapers),
    path('check/user/status/paper/',userPaper),
]