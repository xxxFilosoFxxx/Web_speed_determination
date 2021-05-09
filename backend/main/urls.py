from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('load_video/', views.LoadFileVideo.as_view(), name='load_video')
]
