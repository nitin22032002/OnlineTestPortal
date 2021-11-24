from django.urls import path
from .views import paper,viewPapers,deletePapers
urlpatterns=[
    path('paper/',paper.as_view()),
    path('add/paper',paper.as_view()),
    path('view/papers/',viewPapers),
    path('delete/paper/',deletePapers),
]