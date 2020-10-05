from django.urls import path
from . import views
urlpatterns = [
    # path('', views.index, name='index'),
    path('face/', views.face, name='face'),
    path('face/upload', views.detect, name='detect'),
    path('', views.upload, name='upload'),
    path('display/', views.display, name='display'),
]
